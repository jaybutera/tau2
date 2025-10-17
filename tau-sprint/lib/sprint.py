#!/usr/bin/env python3
from . import storage, util, tau2_reader

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
    # First verify the task exists in tau2
    snapshot = tau2_reader.capture_task_snapshot(task_id)
    if not snapshot:
        return None  # Task not found

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
            "captured_at": util.today()
        }
        stories.append(story)
        storage.save_stories(stories)
    return snapshot

def get_story_snapshot(sprint_id, story_id):
    """Get the captured tau2 snapshot for a story"""
    stories = storage.load_stories()
    for story in stories:
        if story["story_id"] == story_id and story["sprint_id"] == sprint_id:
            return story["tau2_snapshot"]
    return None

def reorder_stories(sprint_id, order):
    sprints = storage.load_sprints()
    for sprint in sprints:
        if sprint["id"] == sprint_id:
            sprint["order"] = order
    storage.save_sprints(sprints)
