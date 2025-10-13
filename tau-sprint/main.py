#!/usr/bin/env python3
import sys
from lib import sprint, task, burndown, util, storage
from tabulate import tabulate
from colorama import Fore, Style

def cmd_create(args):
    """Create new sprint: tau-sprint create <name> --start <date> --end <date> --capacity <hours>"""
    if len(args) < 7:
        print("Usage: tau-sprint create <name> --start <date> --end <date> --capacity <hours>")
        return -1

    name = args[0]
    start = None
    end = None
    capacity = None
    goal = ""

    i = 1
    while i < len(args):
        if args[i] == "--start" and i + 1 < len(args):
            start = args[i + 1]
            i += 2
        elif args[i] == "--end" and i + 1 < len(args):
            end = args[i + 1]
            i += 2
        elif args[i] == "--capacity" and i + 1 < len(args):
            capacity = int(args[i + 1])
            i += 2
        elif args[i] == "--goal" and i + 1 < len(args):
            goal = args[i + 1]
            i += 2
        else:
            i += 1

    if not start or not end or not capacity:
        print("Error: --start, --end, and --capacity are required")
        return -1

    sprint_id = sprint.create_sprint(name, start, end, capacity, goal)
    print(f"Created sprint {sprint_id}")
    return 0

def cmd_list(args):
    """List all sprints"""
    sprints = sprint.list_sprints()
    if not sprints:
        print("No sprints found")
        return 0

    headers = ["ID", "Name", "Status", "Start", "End", "Capacity"]
    rows = []
    for s in sprints:
        rows.append([
            s["id"],
            s["name"],
            s["status"],
            s["start_date"],
            s["end_date"],
            f"{s['capacity_hours']}h"
        ])
    print(tabulate(rows, headers=headers))
    return 0

def cmd_show(sprint_id):
    """Show sprint details"""
    s = sprint.get_sprint(sprint_id)
    if not s:
        print(f"Sprint {sprint_id} not found")
        return -1

    print(f"\nSprint {s['id']}: {s['name']} ({s['status'].upper()})")
    if s['goal']:
        print(f"Goal: {s['goal']}")
    print(f"Start: {s['start_date']} | End: {s['end_date']}")
    print(f"Capacity: {s['capacity_hours']}h")
    print(f"Stories: {', '.join(map(str, s['committed_items']))}")
    return 0

def cmd_activate(sprint_id):
    """Activate a sprint"""
    sprint.activate_sprint(sprint_id)
    print(f"Activated sprint {sprint_id}")
    return 0

def cmd_complete(sprint_id):
    """Complete a sprint"""
    sprint.complete_sprint(sprint_id)
    print(f"Completed sprint {sprint_id}")
    return 0

def cmd_add_story(sprint_id, task_ids):
    """Add stories to sprint"""
    for task_id in task_ids:
        sprint.add_story_to_sprint(sprint_id, int(task_id))
    print(f"Added {len(task_ids)} story(ies) to sprint {sprint_id}")
    return 0

def cmd_breakdown(sprint_id, parent_task_id, breakdown_args):
    """Break down a story into subtasks"""
    # Parse pairs of (title, hours)
    if len(breakdown_args) % 2 != 0:
        print("Error: breakdown requires pairs of <title> <hours>")
        return -1

    subtasks = []
    for i in range(0, len(breakdown_args), 2):
        title = breakdown_args[i]
        hours = util.parse_hours(breakdown_args[i + 1])
        subtasks.append((title, hours))

    new_tasks = task.breakdown_story(sprint_id, parent_task_id, subtasks)
    print(f"Created {len(new_tasks)} subtask(s) for story {parent_task_id}")
    for t in new_tasks:
        print(f"  {t['id']}: {t['title']} ({t['estimated_hours']}h)")
    return 0

def cmd_commit(sprint_id, subtask_ids):
    """Commit subtasks to sprint"""
    task.commit_subtasks(sprint_id, subtask_ids)
    print(f"Committed {len(subtask_ids)} subtask(s) to sprint {sprint_id}")
    return 0

def cmd_uncommit(sprint_id, subtask_ids):
    """Uncommit subtasks from sprint"""
    task.uncommit_subtasks(sprint_id, subtask_ids)
    print(f"Uncommitted {len(subtask_ids)} subtask(s) from sprint {sprint_id}")
    return 0

def cmd_order(sprint_id, order):
    """Reorder stories in sprint"""
    sprint.reorder_stories(sprint_id, [int(x) for x in order])
    print(f"Reordered stories in sprint {sprint_id}")
    return 0

def cmd_task_start(sprint_id, task_id):
    """Start working on a subtask"""
    task.update_task_status(task_id, "in_progress")
    print(f"Started task {task_id}")
    return 0

def cmd_task_update(sprint_id, task_id, args):
    """Update task hours"""
    remaining = None
    actual = None

    i = 0
    while i < len(args):
        if args[i] == "--remaining" and i + 1 < len(args):
            remaining = util.parse_hours(args[i + 1])
            i += 2
        elif args[i] == "--actual" and i + 1 < len(args):
            actual = util.parse_hours(args[i + 1])
            i += 2
        else:
            i += 1

    task.update_task_hours(task_id, remaining, actual)
    print(f"Updated task {task_id}")
    return 0

def cmd_task_done(sprint_id, task_id):
    """Mark task as done"""
    task.update_task_status(task_id, "done")
    t = task.get_task(task_id)
    if t:
        task.update_task_hours(task_id, remaining=0)
    print(f"Completed task {task_id}")
    return 0

def cmd_task_assign(sprint_id, task_id, assignee):
    """Assign task to someone"""
    task.assign_task(task_id, assignee)
    print(f"Assigned task {task_id} to {assignee}")
    return 0

def cmd_board(sprint_id):
    """Show sprint board"""
    s = sprint.get_sprint(sprint_id)
    if not s:
        print(f"Sprint {sprint_id} not found")
        return -1

    print(f"\nSprint {s['id']}: {s['name']} ({s['status'].upper()})")
    if s['goal']:
        print(f"Goal: {s['goal']}")
    print(f"Start: {s['start_date']} | End: {s['end_date']}")

    # Calculate committed hours
    tasks = task.get_tasks_for_sprint(sprint_id)
    committed = sum(t["estimated_hours"] for t in tasks if t["committed_to_sprint"])
    remaining_capacity = s["capacity_hours"] - committed

    print(f"Capacity: {s['capacity_hours']}h | Committed: {committed}h | Remaining: {remaining_capacity}h\n")

    # Group tasks by parent story
    stories = {}
    for t in tasks:
        parent = t["parent_task_id"]
        if parent not in stories:
            stories[parent] = []
        stories[parent].append(t)

    # Display stories in order
    order = s["order"] if s["order"] else s["committed_items"]
    for story_id in order:
        if story_id not in stories:
            print(f"Story #{story_id}: (no subtasks)")
            continue

        story_tasks = stories[story_id]
        total_est = sum(t["estimated_hours"] for t in story_tasks)
        committed_est = sum(t["estimated_hours"] for t in story_tasks if t["committed_to_sprint"])

        print(f"Story #{story_id}: ({committed_est}h committed / {total_est}h total)")

        for t in story_tasks:
            status_label = "IN SPRINT" if t["committed_to_sprint"] else "FUTURE"
            status_color = {
                "todo": "",
                "in_progress": Fore.YELLOW,
                "done": Fore.GREEN
            }.get(t["status"], "")

            status_text = t["status"].upper().replace("_", " ")
            assigned = f" {t['assigned']}" if t["assigned"] else ""

            line = f"  \u251c\u2500 [{status_label}, {status_color}{status_text}{Style.RESET_ALL}] {t['id']}: {t['title']}"
            line += f" ({t['estimated_hours']}h est, {t['remaining_hours']}h rem"
            if t['actual_hours'] > 0:
                line += f", {t['actual_hours']}h actual"
            line += f"){assigned}"
            print(line)
        print()

    return 0

def cmd_capacity(sprint_id):
    """Show capacity vs committed"""
    s = sprint.get_sprint(sprint_id)
    if not s:
        print(f"Sprint {sprint_id} not found")
        return -1

    tasks = task.get_tasks_for_sprint(sprint_id)
    committed = sum(t["estimated_hours"] for t in tasks if t["committed_to_sprint"])
    remaining_capacity = s["capacity_hours"] - committed

    print(f"\nSprint {sprint_id}: {s['name']}")
    print(f"Capacity: {s['capacity_hours']}h")
    print(f"Committed: {committed}h")
    print(f"Remaining: {remaining_capacity}h")
    print(f"Utilization: {100 * committed / s['capacity_hours']:.1f}%")
    return 0

def cmd_snapshot(sprint_id):
    """Take daily burndown snapshot"""
    snapshot = burndown.take_snapshot(sprint_id)
    print(f"Snapshot for sprint {sprint_id} on {snapshot['date']}")
    print(f"  Remaining: {snapshot['remaining_hours']}h")
    print(f"  Completed: {snapshot['completed_hours']}h")
    return 0

def cmd_burndown(sprint_id):
    """View burndown chart"""
    s = sprint.get_sprint(sprint_id)
    if not s:
        print(f"Sprint {sprint_id} not found")
        return -1

    snapshots = burndown.get_burndown_for_sprint(sprint_id)
    if not snapshots:
        print("No burndown data available")
        return 0

    print(f"\nBurndown for Sprint {sprint_id}: {s['name']}\n")
    headers = ["Date", "Remaining", "Completed", "Total"]
    rows = []
    for snap in sorted(snapshots, key=lambda x: x["date"]):
        total = snap["remaining_hours"] + snap["completed_hours"]
        rows.append([
            snap["date"],
            f"{snap['remaining_hours']}h",
            f"{snap['completed_hours']}h",
            f"{total}h"
        ])
    print(tabulate(rows, headers=headers))
    return 0

def cmd_velocity():
    """Calculate velocity from completed sprints"""
    sprints = sprint.list_sprints()
    completed = [s for s in sprints if s["status"] == "completed"]

    if not completed:
        print("No completed sprints found")
        return 0

    print("\nVelocity Report\n")
    headers = ["Sprint", "Completed Hours"]
    rows = []
    total = 0
    for s in completed:
        tasks = task.get_tasks_for_sprint(s["id"])
        completed_hours = sum(t["actual_hours"] for t in tasks if t["status"] == "done")
        rows.append([f"{s['id']}: {s['name']}", f"{completed_hours}h"])
        total += completed_hours

    print(tabulate(rows, headers=headers))
    if completed:
        avg = total / len(completed)
        print(f"\nAverage velocity: {avg:.1f}h per sprint")
    return 0

def print_usage():
    print("""tau-sprint - Sprint management layer for tau2

USAGE:
    tau-sprint <command> [arguments]

COMMANDS:
    create <name> --start <date> --end <date> --capacity <hours> [--goal <goal>]
    list
    show <sprint-id>
    activate <sprint-id>
    complete <sprint-id>

    <sprint-id> add-story <task-id>...
    <sprint-id> story <task-id> breakdown <title> <hours> [<title> <hours>...]
    <sprint-id> commit <subtask-id>...
    <sprint-id> uncommit <subtask-id>...
    <sprint-id> order <task-id>...

    <sprint-id> task <subtask-id> start
    <sprint-id> task <subtask-id> update --remaining <hours> --actual <hours>
    <sprint-id> task <subtask-id> done
    <sprint-id> task <subtask-id> assign <@username>

    <sprint-id> board
    <sprint-id> capacity
    <sprint-id> snapshot
    <sprint-id> burndown

    velocity

EXAMPLES:
    tau-sprint create "Sprint 1" --start 2025-01-13 --end 2025-01-27 --capacity 160
    tau-sprint 1 add-story 5 8 12
    tau-sprint 1 story 5 breakdown "Design API" 4h "Implement" 8h
    tau-sprint 1 board
""")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return 0

    cmd = sys.argv[1]

    if cmd in ["-h", "--help", "help"]:
        print_usage()
        return 0
    elif cmd == "create":
        return cmd_create(sys.argv[2:])
    elif cmd == "list":
        return cmd_list(sys.argv[2:])
    elif cmd == "velocity":
        return cmd_velocity()
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: tau-sprint show <sprint-id>")
            return -1
        return cmd_show(int(sys.argv[2]))
    elif cmd == "activate":
        if len(sys.argv) < 3:
            print("Usage: tau-sprint activate <sprint-id>")
            return -1
        return cmd_activate(int(sys.argv[2]))
    elif cmd == "complete":
        if len(sys.argv) < 3:
            print("Usage: tau-sprint complete <sprint-id>")
            return -1
        return cmd_complete(int(sys.argv[2]))

    # Commands that start with sprint ID
    try:
        sprint_id = int(cmd)
    except ValueError:
        print(f"Error: unknown command '{cmd}'")
        print_usage()
        return -1

    if len(sys.argv) < 3:
        # Just show the sprint
        return cmd_show(sprint_id)

    subcmd = sys.argv[2]
    args = sys.argv[3:]

    if subcmd == "add-story":
        return cmd_add_story(sprint_id, args)
    elif subcmd == "story":
        if len(args) < 2:
            print("Usage: tau-sprint <sprint-id> story <task-id> breakdown ...")
            return -1
        story_id = int(args[0])
        story_cmd = args[1]
        if story_cmd == "breakdown":
            return cmd_breakdown(sprint_id, story_id, args[2:])
        else:
            print(f"Error: unknown story command '{story_cmd}'")
            return -1
    elif subcmd == "commit":
        return cmd_commit(sprint_id, args)
    elif subcmd == "uncommit":
        return cmd_uncommit(sprint_id, args)
    elif subcmd == "order":
        return cmd_order(sprint_id, args)
    elif subcmd == "task":
        if len(args) < 2:
            print("Usage: tau-sprint <sprint-id> task <subtask-id> <command>")
            return -1
        task_id = args[0]
        task_cmd = args[1]
        task_args = args[2:]

        if task_cmd == "start":
            return cmd_task_start(sprint_id, task_id)
        elif task_cmd == "update":
            return cmd_task_update(sprint_id, task_id, task_args)
        elif task_cmd == "done":
            return cmd_task_done(sprint_id, task_id)
        elif task_cmd == "assign":
            if not task_args:
                print("Usage: tau-sprint <sprint-id> task <subtask-id> assign <@username>")
                return -1
            return cmd_task_assign(sprint_id, task_id, task_args[0])
        else:
            print(f"Error: unknown task command '{task_cmd}'")
            return -1
    elif subcmd == "board":
        return cmd_board(sprint_id)
    elif subcmd == "capacity":
        return cmd_capacity(sprint_id)
    elif subcmd == "snapshot":
        return cmd_snapshot(sprint_id)
    elif subcmd == "burndown":
        return cmd_burndown(sprint_id)
    else:
        print(f"Error: unknown command '{subcmd}'")
        return -1

if __name__ == "__main__":
    sys.exit(main())
