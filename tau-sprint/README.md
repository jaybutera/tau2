# tau-sprint

Sprint management layer built on top of tau2.

## Installation

Install dependencies:

```bash
cd ~/src/tau2/tau-sprint
poetry install
```

Add an alias to your `~/.bashrc`:

```bash
alias tau-sprint="cd ~/src/tau2/tau-sprint && poetry run python client/main.py"
```

Start the tau-sprint server:

```bash
cd ~/src/tau2/tau-sprint
poetry run python server/main.py
```

## Quick Start

```bash
# Create a sprint (dates in DDMM format)
tau-sprint create "Sprint 1" --start 1301 --end 2701 --capacity 160

# Add stories from tau2
tau-sprint 1 add-story 5 8

# Break down story into subtasks
tau-sprint 1 story 5 breakdown "Design API" 4h "Implement OAuth" 8h "Write tests" 3h

# View sprint board (default view)
tau-sprint 1

# Start working on a subtask
tau-sprint 1 task s1-t1 start

# Update progress
tau-sprint 1 task s1-t1 update --remaining 2h --actual 2h

# Mark done (works from any status)
tau-sprint 1 task s1-t1 done

# View burndown chart (snapshots are automatic)
tau-sprint 1 burndown
```
