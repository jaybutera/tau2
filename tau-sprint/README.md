# tau-sprint

Sprint management layer built on top of tau2.

## Installation

```bash
cd tau-sprint
poetry install
```

Or add an alias to your `~/.bashrc`:

```bash
alias tau-sprint="python3 ~/src/tau2/tau-sprint/main.py"
```

## Quick Start

```bash
# Create a sprint
tau-sprint create "Sprint 1" --start 2025-01-13 --end 2025-01-27 --capacity 160

# Add stories from tau2
tau-sprint 1 add-story 5 8

# Break down story into subtasks
tau-sprint 1 story 5 breakdown "Design API" 4h "Implement OAuth" 8h "Write tests" 3h

# View sprint board
tau-sprint 1 board

# Start working on a subtask
tau-sprint 1 task s1-t1 start

# Update progress
tau-sprint 1 task s1-t1 update --remaining 2 --actual 2

# Mark done
tau-sprint 1 task s1-t1 done

# Take daily snapshot
tau-sprint 1 snapshot

# View burndown
tau-sprint 1 burndown
```

For complete documentation, see tau-sprint.md
