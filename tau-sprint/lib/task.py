#!/usr/bin/env python3
from . import storage, util

def breakdown_story(sprint_id, parent_task_id, subtasks):
    """
    subtasks: list of (title, estimated_hours) tuples
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

def get_tasks_for_sprint(sprint_id):
    tasks = storage.load_tasks()
    return [t for t in tasks if t["sprint_id"] == sprint_id]

def get_tasks_for_story(sprint_id, parent_task_id):
    tasks = storage.load_tasks()
    return [t for t in tasks if t["sprint_id"] == sprint_id and t["parent_task_id"] == parent_task_id]

def get_task(task_id):
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def update_task_status(task_id, status):
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
    storage.save_tasks(tasks)

def update_task_hours(task_id, remaining=None, actual=None):
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if remaining is not None:
                task["remaining_hours"] = remaining
            if actual is not None:
                task["actual_hours"] = actual
    storage.save_tasks(tasks)

def assign_task(task_id, assignee):
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["assigned"] = assignee
    storage.save_tasks(tasks)

def commit_subtasks(sprint_id, task_ids):
    tasks = storage.load_tasks()
    for task in tasks:
        if task["sprint_id"] == sprint_id and task["id"] in task_ids:
            task["committed_to_sprint"] = True
    storage.save_tasks(tasks)

def uncommit_subtasks(sprint_id, task_ids):
    tasks = storage.load_tasks()
    for task in tasks:
        if task["sprint_id"] == sprint_id and task["id"] in task_ids:
            task["committed_to_sprint"] = False
    storage.save_tasks(tasks)
