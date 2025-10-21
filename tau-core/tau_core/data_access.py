#!/usr/bin/env python3
"""Data access layer for tau2 tasks"""
import json
from pathlib import Path
from .storage import TAU_DATA_DIR


def load_active():
    """Load active tasks index from tau2"""
    active_file = TAU_DATA_DIR / "active"
    if not active_file.exists():
        return []
    with open(active_file) as f:
        return json.load(f)


def load_task_blob(blob_idx):
    """Load a task blob from tau2"""
    if not blob_idx:
        return None
    blob_prefix = blob_idx[:2]
    blob_file = TAU_DATA_DIR / "blob" / blob_prefix / blob_idx
    if not blob_file.exists():
        return None
    with open(blob_file) as f:
        return json.load(f)


def get_task_by_id(task_id):
    """Get a tau2 task by its ID"""
    try:
        active = load_active()
        if task_id >= len(active):
            return None
        blob_idx = active[task_id]
        if blob_idx is None:
            return None
        return load_task_blob(blob_idx)
    except Exception:
        return None


def capture_task_snapshot(task_id):
    """Capture a snapshot of tau2 task data for historical record"""
    task = get_task_by_id(task_id)
    if not task:
        return None

    # Capture relevant fields for sprint history
    snapshot = {
        "title": task.get("title", ""),
        "desc": task.get("desc", ""),
        "project": task.get("project"),
        "tags": task.get("tags", []),
        "status": task.get("status", "open"),
        "rank": task.get("rank"),
    }
    return snapshot
