#!/usr/bin/env python3
"""tau-sprint client API - RPC wrapper"""
from tau_core.rpc_client import RPCClient

# Create RPC client for tau-sprint server (port 7644)
client = RPCClient(port=7644)


# Sprint management

async def create_sprint(name, start_date, end_date, capacity, goal=""):
    return await client.query("create_sprint", [name, start_date, end_date, capacity, goal])


async def list_sprints():
    return await client.query("list_sprints", [])


async def get_sprint(sprint_id):
    return await client.query("get_sprint", [sprint_id])


async def activate_sprint(sprint_id):
    return await client.query("activate_sprint", [sprint_id])


async def complete_sprint(sprint_id):
    return await client.query("complete_sprint", [sprint_id])


async def add_story_to_sprint(sprint_id, task_id):
    return await client.query("add_story_to_sprint", [sprint_id, task_id])


async def reorder_stories(sprint_id, order):
    return await client.query("reorder_stories", [sprint_id, order])


# Task breakdown

async def breakdown_story(sprint_id, parent_task_id, subtasks):
    return await client.query("breakdown_story", [sprint_id, parent_task_id, subtasks])


async def get_tasks_for_sprint(sprint_id):
    return await client.query("get_tasks_for_sprint", [sprint_id])


async def get_tasks_for_story(sprint_id, parent_task_id):
    return await client.query("get_tasks_for_story", [sprint_id, parent_task_id])


async def update_task_status(task_id, status):
    return await client.query("update_task_status", [task_id, status])


async def update_task_hours(task_id, remaining=None, actual=None):
    return await client.query("update_task_hours", [task_id, remaining, actual])


async def assign_task(task_id, assignee):
    return await client.query("assign_task", [task_id, assignee])


async def commit_subtasks(sprint_id, task_ids):
    return await client.query("commit_subtasks", [sprint_id, task_ids])


async def uncommit_subtasks(sprint_id, task_ids):
    return await client.query("uncommit_subtasks", [sprint_id, task_ids])


# Burndown

async def take_snapshot(sprint_id):
    return await client.query("take_snapshot", [sprint_id])


async def get_burndown_for_sprint(sprint_id):
    return await client.query("get_burndown_for_sprint", [sprint_id])
