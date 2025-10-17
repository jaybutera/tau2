#!/usr/bin/env python3
import json
import os
from pathlib import Path

SPRINT_DIR = Path.home() / ".config" / "tau" / "sprint"

def ensure_dir():
    SPRINT_DIR.mkdir(parents=True, exist_ok=True)

def load_sprints():
    ensure_dir()
    path = SPRINT_DIR / "sprints.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []

def save_sprints(sprints):
    ensure_dir()
    path = SPRINT_DIR / "sprints.json"
    with open(path, "w") as f:
        json.dump(sprints, f, indent=2)

def load_tasks():
    ensure_dir()
    path = SPRINT_DIR / "sprint_tasks.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    ensure_dir()
    path = SPRINT_DIR / "sprint_tasks.json"
    with open(path, "w") as f:
        json.dump(tasks, f, indent=2)

def load_burndown():
    ensure_dir()
    path = SPRINT_DIR / "burndown.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []

def save_burndown(burndown):
    ensure_dir()
    path = SPRINT_DIR / "burndown.json"
    with open(path, "w") as f:
        json.dump(burndown, f, indent=2)

def load_stories():
    ensure_dir()
    path = SPRINT_DIR / "stories.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []

def save_stories(stories):
    ensure_dir()
    path = SPRINT_DIR / "stories.json"
    with open(path, "w") as f:
        json.dump(stories, f, indent=2)
