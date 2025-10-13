#!/usr/bin/env python3
from . import storage, util

def create_sprint(name, start_date, end_date, capacity, goal=""):
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

def get_sprint(sprint_id):
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            return sprint
    return None

def list_sprints():
    return storage.load_sprints()

def activate_sprint(sprint_id):
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            sprint["status"] = "active"
        elif sprint["status"] == "active":
            sprint["status"] = "planning"
    storage.save_sprints(sprints)

def complete_sprint(sprint_id):
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            sprint["status"] = "completed"
    storage.save_sprints(sprints)

def add_story_to_sprint(sprint_id, task_id):
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            if task_id not in sprint["committed_items"]:
                sprint["committed_items"].append(task_id)
                sprint["order"].append(task_id)
    storage.save_sprints(sprints)

def reorder_stories(sprint_id, order):
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            sprint["order"] = order
    storage.save_sprints(sprints)
