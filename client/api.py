#!/usr/bin/env python3
"""tau2 client API - RPC wrapper"""
from tau_core.rpc_client import RPCClient

# Create RPC client for tau2 server
client = RPCClient(port=7643)


async def get_info():
    return await client.query("get_info", [])


async def add_task(who, task):
    return await client.query("add_task", [who, task])


async def fetch_active_tasks():
    return await client.query("fetch_active_tasks", [])


async def fetch_deactive_tasks(month):
    return await client.query("fetch_deactive_tasks", [month])


async def fetch_task(task_id):
    return await client.query("fetch_task", [task_id])


async def fetch_archive_task(task_id, month):
    return await client.query("fetch_archive_task", [task_id, month])


async def modify_task(who, id, changes):
    return await client.query("modify_task", [who, id, changes])


async def change_task_status(who, id, status):
    await client.query("change_task_status", [who, id, status])
    return True


async def add_task_comment(who, id, comment):
    await client.query("add_task_comment", [who, id, comment])
    return True
