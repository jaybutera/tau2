#!/usr/bin/env python3
"""tau-sprint server - Sprint management RPC server"""
import asyncio
import sys
sys.path.insert(0, '/home/casper/src/tau2/tau-core')

from tau_core.rpc_server import run_rpc_server
import api

if __name__ == "__main__":
    asyncio.run(run_rpc_server("0.0.0.0", 7644, api.call))
