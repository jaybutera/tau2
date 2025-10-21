#!/usr/bin/env python3
"""tau-sprint server API"""
import json
import sys
import tau_core.util
import tau_core.data_access
import tau_core.storage

# Get storage instance for sprints
storage = tau_core.storage.get_sprint_storage()

PROTOCOL_VERSION = 1


class Error:
    """RPC error response"""

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def as_response(self, request):
        return {
            "id": request["id"],
            "result": None,
            "error": {
                "code": self.code,
                "message": self.msg
            }
        }


# Sprint management methods

async def create_sprint(name, start_date, end_date, capacity, goal=""):
    """Create a new sprint"""
    sprints = storage.load_sprints()
    sprint_id = len(sprints) + 1 if sprints else 1

    sprint = {
        "id": sprint_id,
        "name": name,
        "goal": goal,
        "start_date": start_date,
        "end_date": end_date,
        "status": "planning",
        "capacity_hours": capacity,
        "committed_items": [],
        "order": []
    }

    sprints.append(sprint)
    storage.save_sprints(sprints)
    return sprint_id


async def list_sprints():
    """List all sprints"""
    return storage.load_sprints()


async def get_sprint(sprint_id):
    """Get sprint by ID"""
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            return sprint
    return Error(404, f"Sprint {sprint_id} not found")


async def activate_sprint(sprint_id):
    """Activate a sprint"""
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            sprint["status"] = "active"
        elif sprint["status"] == "active":
            sprint["status"] = "planning"
    storage.save_sprints(sprints)
    return True


async def complete_sprint(sprint_id):
    """Complete a sprint"""
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            sprint["status"] = "completed"
    storage.save_sprints(sprints)
    return True


async def add_story_to_sprint(sprint_id, task_id):
    """Add a tau2 story to a sprint"""
    # First verify the task exists in tau2
    snapshot = tau_core.data_access.capture_task_snapshot(task_id)
    if not snapshot:
        return Error(404, f"Task {task_id} not found in tau2")

    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            if task_id not in sprint["committed_items"]:
                sprint["committed_items"].append(task_id)
                sprint["order"].append(task_id)
    storage.save_sprints(sprints)

    # Capture snapshot of tau2 task for historical record
    stories = storage.load_stories()
    # Check if story already captured
    if not any(s["story_id"] == task_id and s["sprint_id"] == sprint_id for s in stories):
        story = {
            "story_id": task_id,
            "sprint_id": sprint_id,
            "tau2_snapshot": snapshot,
            "captured_at": tau_core.util.today()
        }
        stories.append(story)
        storage.save_stories(stories)
    return snapshot


async def reorder_stories(sprint_id, order):
    """Reorder stories in a sprint"""
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            sprint["order"] = order
    storage.save_sprints(sprints)
    return True


# Task breakdown methods

async def breakdown_story(sprint_id, parent_task_id, subtasks):
    """Break down a story into subtasks

    Args:
        sprint_id: Sprint ID
        parent_task_id: Parent tau2 task ID
        subtasks: List of [title, estimated_hours] pairs
    """
    tasks = storage.load_tasks()

    # Find max existing subtask ID for this sprint
    max_id = 0
    for task in tasks:
        if task["sprint_id"] == sprint_id:
            task_num = int(task["id"].split("-t")[1])
            max_id = max(max_id, task_num)

    new_tasks = []
    for i, (title, estimated_hours) in enumerate(subtasks):
        task_id = f"s{sprint_id}-t{max_id + i + 1}"
        task = {
            "id": task_id,
            "sprint_id": sprint_id,
            "parent_task_id": parent_task_id,
            "title": title,
            "estimated_hours": estimated_hours,
            "remaining_hours": estimated_hours,
            "actual_hours": 0,
            "assigned": None,
            "status": "todo",
            "order": len(tasks) + i,
            "committed_to_sprint": True
        }
        new_tasks.append(task)

    tasks.extend(new_tasks)
    storage.save_tasks(tasks)
    return new_tasks


async def get_tasks_for_sprint(sprint_id):
    """Get all tasks for a sprint"""
    tasks = storage.load_tasks()
    return [t for t in tasks if t["sprint_id"] == sprint_id]


async def get_tasks_for_story(sprint_id, parent_task_id):
    """Get subtasks for a specific story"""
    tasks = storage.load_tasks()
    return [t for t in tasks if t["sprint_id"] == sprint_id and t["parent_task_id"] == parent_task_id]


async def update_task_status(task_id, status):
    """Update task status (can transition from any state to any state)"""
    tasks = storage.load_tasks()
    found = False
    sprint_id = None
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            sprint_id = task["sprint_id"]
            found = True
            break
    if not found:
        return Error(404, f"Task {task_id} not found")
    storage.save_tasks(tasks)

    # Auto-snapshot after status change
    if sprint_id:
        await take_snapshot(sprint_id)

    return True


async def update_task_hours(task_id, remaining=None, actual=None):
    """Update task hours"""
    tasks = storage.load_tasks()
    sprint_id = None
    for task in tasks:
        if task["id"] == task_id:
            if remaining is not None:
                task["remaining_hours"] = remaining
            if actual is not None:
                task["actual_hours"] = actual
            sprint_id = task["sprint_id"]
            break
    storage.save_tasks(tasks)

    # Auto-snapshot after hours change
    if sprint_id:
        await take_snapshot(sprint_id)

    return True


async def assign_task(task_id, assignee):
    """Assign task to someone"""
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["assigned"] = assignee
    storage.save_tasks(tasks)
    return True


async def commit_subtasks(sprint_id, task_ids):
    """Commit subtasks to sprint"""
    tasks = storage.load_tasks()
    for task in tasks:
        if task["sprint_id"] == sprint_id and task["id"] in task_ids:
            task["committed_to_sprint"] = True
    storage.save_tasks(tasks)
    return True


async def uncommit_subtasks(sprint_id, task_ids):
    """Uncommit subtasks from sprint"""
    tasks = storage.load_tasks()
    for task in tasks:
        if task["sprint_id"] == sprint_id and task["id"] in task_ids:
            task["committed_to_sprint"] = False
    storage.save_tasks(tasks)
    return True


# Burndown methods

async def take_snapshot(sprint_id):
    """Take a burndown snapshot (can be called multiple times per day)"""
    tasks = storage.load_tasks()
    sprint_tasks = [t for t in tasks if t["sprint_id"] == sprint_id]

    remaining = 0
    completed = 0

    for t in sprint_tasks:
        if t["committed_to_sprint"]:
            if t["status"] == "done":
                completed += t["estimated_hours"]
            else:
                remaining += t["remaining_hours"]

    burndown = storage.load_burndown()
    snapshot = {
        "sprint_id": sprint_id,
        "date": tau_core.util.today(),
        "timestamp": tau_core.util.now(),
        "remaining_hours": remaining,
        "completed_hours": completed
    }

    # Append snapshot (multiple snapshots per day allowed)
    burndown.append(snapshot)

    storage.save_burndown(burndown)
    return snapshot


async def get_burndown_for_sprint(sprint_id):
    """Get burndown data for a sprint"""
    burndown = storage.load_burndown()
    return [s for s in burndown if s["sprint_id"] == sprint_id]


# API dispatch table

api_table = {
    # Sprint management
    "create_sprint": create_sprint,
    "list_sprints": list_sprints,
    "get_sprint": get_sprint,
    "activate_sprint": activate_sprint,
    "complete_sprint": complete_sprint,
    "add_story_to_sprint": add_story_to_sprint,
    "reorder_stories": reorder_stories,
    # Task breakdown
    "breakdown_story": breakdown_story,
    "get_tasks_for_sprint": get_tasks_for_sprint,
    "get_tasks_for_story": get_tasks_for_story,
    "update_task_status": update_task_status,
    "update_task_hours": update_task_hours,
    "assign_task": assign_task,
    "commit_subtasks": commit_subtasks,
    "uncommit_subtasks": uncommit_subtasks,
    # Burndown
    "take_snapshot": take_snapshot,
    "get_burndown_for_sprint": get_burndown_for_sprint,
}


async def call(request):
    """Handle RPC call"""
    if request["protocol_version"] != PROTOCOL_VERSION:
        error = Error(52, "wrong protocol version. Please git pull")
        return error.as_response(request)

    method = request["method"]
    params = request["params"]

    if method not in api_table:
        error = Error(404, f"unknown method: {method}")
        return error.as_response(request)

    func = api_table[method]
    result = await func(*params)

    if isinstance(result, Error):
        return result.as_response(request)

    # Normal reply
    response = {
        "id": request["id"],
        "result": result,
    }
    return response
