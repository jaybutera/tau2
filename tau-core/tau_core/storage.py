#!/usr/bin/env python3
"""Unified storage abstraction for tau tools"""
import json
from pathlib import Path


class JSONStorage:
    """Generic JSON file storage"""

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir).expanduser()

    def ensure_dir(self):
        """Ensure storage directory exists"""
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def load(self, filename):
        """Load JSON data from file"""
        self.ensure_dir()
        path = self.base_dir / filename
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return None

    def save(self, filename, data):
        """Save JSON data to file"""
        self.ensure_dir()
        path = self.base_dir / filename
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load_list(self, filename, default=None):
        """Load JSON list with default empty list"""
        if default is None:
            default = []
        result = self.load(filename)
        return result if result is not None else default

    # Sprint-specific storage methods
    def load_sprints(self):
        """Load sprints data"""
        return self.load_list("sprints.json")

    def save_sprints(self, sprints):
        """Save sprints data"""
        self.save("sprints.json", sprints)

    def load_tasks(self):
        """Load sprint tasks data"""
        return self.load_list("sprint_tasks.json")

    def save_tasks(self, tasks):
        """Save sprint tasks data"""
        self.save("sprint_tasks.json", tasks)

    def load_burndown(self):
        """Load burndown data"""
        return self.load_list("burndown.json")

    def save_burndown(self, burndown):
        """Save burndown data"""
        self.save("burndown.json", burndown)

    def load_stories(self):
        """Load stories data"""
        return self.load_list("stories.json")

    def save_stories(self, stories):
        """Save stories data"""
        self.save("stories.json", stories)


# Common storage locations
TAU_DATA_DIR = Path.home() / ".config" / "tau" / "data"
TAU_SPRINT_DIR = Path.home() / ".config" / "tau" / "sprint"


def get_tau_storage():
    """Get storage instance for tau2 data"""
    return JSONStorage(TAU_DATA_DIR)


def get_sprint_storage():
    """Get storage instance for tau-sprint data"""
    return JSONStorage(TAU_SPRINT_DIR)
