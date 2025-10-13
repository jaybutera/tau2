#!/usr/bin/env python3
from . import storage, util, task

def take_snapshot(sprint_id):
    """Take a daily burndown snapshot"""
    tasks = task.get_tasks_for_sprint(sprint_id)

    remaining = 0
    completed = 0

    for t in tasks:
        if t["committed_to_sprint"]:
            if t["status"] == "done":
                completed += t["estimated_hours"]
            else:
                remaining += t["remaining_hours"]

    burndown = storage.load_burndown()
    snapshot = {
        "sprint_id": sprint_id,
        "date": util.today(),
        "remaining_hours": remaining,
        "completed_hours": completed
    }

    # Replace existing snapshot for today if exists
    burndown = [s for s in burndown if not (s["sprint_id"] == sprint_id and s["date"] == util.today())]
    burndown.append(snapshot)

    storage.save_burndown(burndown)
    return snapshot

def get_burndown_for_sprint(sprint_id):
    burndown = storage.load_burndown()
    return [s for s in burndown if s["sprint_id"] == sprint_id]
