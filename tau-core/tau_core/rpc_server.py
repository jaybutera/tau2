#!/usr/bin/env python3
"""RPC server framework for tau services"""
import asyncio
import json

from .net import Channel


async def handle_rpc_connection(reader, writer, api_handler):
    """
    Handle a single RPC connection

    Args:
        reader: asyncio StreamReader
        writer: asyncio StreamWriter
        api_handler: Async function that processes requests and returns responses
    """
    try:
        addr = writer.get_extra_info("peername")
        print(f"Received connection from {addr}")
        channel = Channel(reader, writer)

        while True:
            request = await channel.receive()
            if request is None:
                print("Channel closed")
                return

            print("request:")
            print(json.dumps(request, indent=2))

            response = await api_handler(request)
            print("response:")
            print(json.dumps(response, indent=2))

            await channel.send(response)

    except Exception:
        import traceback
        traceback.print_exc()


async def run_rpc_server(host, port, api_handler):
    """
    Start an RPC server

    Args:
        host: Host address to bind to
        port: Port number to listen on
        api_handler: Async function that processes requests and returns responses
    """
    print(f"Server starting on {host}:{port}")

    async def connection_handler(reader, writer):
        await handle_rpc_connection(reader, writer, api_handler)

    server = await asyncio.start_server(connection_handler, host, port)
    async with server:
        await server.serve_forever()
