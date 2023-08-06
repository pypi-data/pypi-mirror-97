#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python Team Awareness Kit (PyTAK) Module Class Definitions."""

import aiohttp
import asyncio
import logging
import os
import queue
import random
import urllib

import pycot
import websockets

from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

import pytak

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2020 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


class Worker:  # pylint: disable=too-few-public-methods

    """Meta class for all other Worker Classes."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False
    logging.getLogger("asyncio").setLevel(pytak.LOG_LEVEL)

    def __init__(self, event_queue: asyncio.Queue) -> None:
        self.event_queue: asyncio.Queue = event_queue

    async def run(self) -> None:
        """Placeholder Run Method for this Class."""
        self._logger.warning("Overwrite this method!")


class EventWorker(Worker):  # pylint: disable=too-few-public-methods

    """
    EventWorker handles getting Cursor on Target Events from a queue, and
    passing them off to a transport worker.

    You should create an EventWorker Instance using the
    `pytak.eventworker_factory` Function.

    CoT Events are put onto the CoT Event Queue using `pytak.MessageWorker`
    Class.
    """

    def __init__(self, event_queue: asyncio.Queue, writer) -> None:
        super().__init__(event_queue)
        self.writer = writer

    async def run(self):
        """Runs this Thread, reads in Message Queue & sends out CoT."""
        self._logger.info('Running EventWorker')

        while 1:
            event = await self.event_queue.get()
            if not event:
                continue
            self._logger.debug("event='%s'", event)

            if isinstance(event, pycot.Event):
                _event = event.render(encoding='UTF-8', standalone=True)
            else:
                _event = event

            if hasattr(self.writer, "send"):
                await self.writer.send(_event)
            else:
                self.writer.write(_event)
                await self.writer.drain()

            if not os.environ.get('DISABLE_RANDOM_SLEEP'):
                await asyncio.sleep(pytak.DEFAULT_SLEEP * random.random())


class MessageWorker(Worker):  # pylint: disable=too-few-public-methods

    """
    MessageWorker handles getting non-CoT messages from a non-CoT Input,
    encoding them as CoT, and putting them onto a CoT Event Queue.

    The CoT Event Queue is handled by the `pytak.EventWorker` Class.
    """

    def __init__(self, event_queue: asyncio.Queue,
                 cot_stale: int = None) -> None:
        super().__init__(event_queue)
        self.cot_stale = cot_stale or pytak.DEFAULT_COT_STALE

    async def _put_event_queue(self, event: pycot.Event) -> None:
        """Puts Event onto the CoT Event Queue."""
        try:
            await self.event_queue.put(event)
        except queue.Full:
            self._logger.warning(
                "Lost CoT Event (queue full): '%s'", event)


class EventTransmitter(Worker):  # pylint: disable=too-few-public-methods

    """
    EventWorker handles getting Cursor on Target Events from a queue, and
    passing them off to a transport worker.

    You should create an EventWorker Instance using the
    `pytak.eventworker_factory` Function.

    CoT Events are put onto the CoT Event Queue using `pytak.MessageWorker`
    Class.
    """

    def __init__(self, tx_queue: asyncio.Queue, writer) -> None:
        super().__init__(tx_queue)
        self.writer = writer

    async def run(self):
        """Runs this Thread, reads in Message Queue & sends out CoT."""
        self._logger.info("Running EventTransmitter")

        while 1:
            tx_event = await self.event_queue.get()
            if not tx_event:
                continue
            self._logger.debug("tx_event='%s'", tx_event)

            if isinstance(tx_event, pycot.Event):
                _event = tx_event.render(encoding='UTF-8', standalone=True)
            else:
                _event = tx_event

            if hasattr(self.writer, "send"):
                await self.writer.send(_event)
            else:
                self.writer.write(_event)
                await self.writer.drain()

            if not os.environ.get('DISABLE_RANDOM_SLEEP'):
                await asyncio.sleep(pytak.DEFAULT_SLEEP * random.random())


class EventReceiver(Worker):  # pylint: disable=too-few-public-methods

    def __init__(self, rx_queue: asyncio.Queue, reader) -> None:
        super().__init__(rx_queue)
        self.reader = reader

    async def run(self):
        self._logger.info("Running EventReceiver")

        while 1:
            rx_event = await self.event_queue.get()
            self._logger.debug("rx_event='%s'", rx_event)


class TCClient:

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False
    # logging.getLogger("asyncio").setLevel(pytak.LOG_LEVEL)
    logging.getLogger("websockets").setLevel(logging.DEBUG) # pytak.LOG_LEVEL)

    def __init__(self, url, timeout=3):
        self.url = url
        self.wss_url = self.url.geturl().replace("http", "ws")
        self.access_token = None
        self.client = self.get_websocket_connection()
        self.timeout = timeout
        self._flag_closed = False

    @property
    def closed(self):
        return self._flag_closed

    async def create(self, timeout=3):
        await self.client.asend(None)
        return self

    async def get_websocket_connection(self):
        while not self.closed:
            try:
                await self.auth()
                headers = websockets.http.Headers(
                    {("Authorization", f"Bearer {self.access_token}")})
                print("Create New Connection...")
                async with websockets.connect(
            self.wss_url, extra_headers=headers, ping_timeout=120,
            ping_interval=5) as ws:
                    self._websocket_connection = ws
                    data = yield

                    while 1:
                        await ws.send(data)
                        data = yield await asyncio.wait_for(ws.recv(), self.timeout)

            except (asyncio.TimeoutError, ConnectionClosedOK, ConnectionClosedError):
                pass

    async def send(self, data):
        if self.closed:
            await self._websocket_connection.ping()

        r = await self.client.asend(data)
        if (r) :
            return r
        else:
            # timeout retry
            return await self.client.asend(data)

    async def close(self):
        if not self.closed:
            self._flag_closed = True
            await self._websocket_connection.close()
            print("Connection closed.")

    async def auth(self):
        self._logger.debug("Logging into TC")
        auth_url = "https://app-api.parteamconnect.com/api/v1/auth/token"
        team_url = self.url.geturl()
        scope = f"{team_url}/.bridge-both"
        payload = {
            "url": team_url,
            "grant_type": "client_credentials",
            "client_id": os.environ.get("TC_ACCESS_KEY_ID"),
            "client_secret": os.environ.get("TC_SECRET_KEY"),
            "scope": scope
        }
        self._logger.debug("payload='%s'", payload)

        async with aiohttp.ClientSession() as session:
            resp = await session.request(
                method="POST", url=auth_url, data=payload)
            resp.raise_for_status()

            json_resp = await resp.json()
            access_token = json_resp.get("access_token")
            assert access_token

            self._logger.debug("Received TC Access Token")
            self.access_token = access_token

            return self.access_token

    async def run(self) -> None:
        loop = asyncio.get_event_loop()
        self._logger.info("Running TCClient for %s", self.url)

        await self.auth()
        headers = websockets.http.Headers(
            {("Authorization", f"Bearer {self.access_token}")})
        return await websockets.connect(
            self.wss_url, extra_headers=headers, ping_timeout=120,
            ping_interval=5)
