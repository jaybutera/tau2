#!/usr/bin/env python3
"""RPC client for tau services"""
import asyncio
import random
import sys

from .net import Channel
from . import config


class RPCClient:
    """Generic RPC client for making requests to tau servers"""

    def __init__(self, server=None, port=7643, protocol_version=1):
        """
        Initialize RPC client

        Args:
            server: Server hostname (defaults to 'server' config or 'localhost')
            port: Server port number
            protocol_version: RPC protocol version
        """
        if server is None:
            server = config.get("server", "localhost")
        self.server = server
        self.port = port
        self.protocol_version = protocol_version

    async def create_channel(self):
        """Create an encrypted channel to the server"""
        reader, writer = await asyncio.open_connection(self.server, self.port)
        channel = Channel(reader, writer)
        return channel

    def random_id(self):
        """Generate random request ID"""
        return random.randint(0, 2**32)

    async def query(self, method, params):
        """
        Make an RPC call to the server

        Args:
            method: Method name to call
            params: List of parameters to pass

        Returns:
            Result from the server

        Raises:
            SystemExit: If connection fails or server returns error
        """
        channel = await self.create_channel()
        request = {
            "id": self.random_id(),
            "method": method,
            "params": params,
            "protocol_version": self.protocol_version,
        }
        await channel.send(request)

        response = await channel.receive()
        # Closed connection returns None
        if response is None:
            print("error: connection with server was closed", file=sys.stderr)
            sys.exit(-1)

        if "error" in response:
            error = response["error"]
            errcode, errmsg = error["code"], error["message"]
            print(f"error: {errcode} - {errmsg}", file=sys.stderr)
            sys.exit(-1)

        return response["result"]
