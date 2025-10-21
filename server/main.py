#!/usr/bin/env python3
"""tau2 server - Task management RPC server"""
import asyncio
from tau_core.rpc_server import run_rpc_server
import api

if __name__ == "__main__":
    asyncio.run(run_rpc_server("0.0.0.0", 7643, api.call))
