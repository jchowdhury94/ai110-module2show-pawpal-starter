# PawPal+

PawPal+ is a pet care planning assistant. It helps a pet owner track care tasks for one or more pets and generate a daily schedule, ordered by time and flagged for scheduling conflicts.

## 🐾 Scenario

A busy pet owner needs help staying consistent with pet care — tracking tasks like walks, feeding, meds, and grooming, and turning them into a clear daily plan.

## ✨ Features

- Add and manage multiple pets and their care tasks.
- Generate daily schedules sorted by time.
- Filter tasks by pet or completion status (available via the backend API and demonstrated in the CLI demo; not yet exposed in the Streamlit UI).
- Automatically create new occurrences for recurring daily and weekly tasks.
- Detect scheduling conflicts and display warning messages.
- Display schedules in both a command-line demo and a Streamlit interface.

Note: monthly tasks are marked complete but do not currently auto-generate a follow-up occurrence (only daily and weekly tasks recur).

Note: the CLI demo's "Priority" column is a display-only label computed from keyword matching in `main.py` — task priority does not currently affect how the scheduler orders or selects tasks.

## 🧠 Core Algorithms

| Algorithm | Implementation | Description |
|---|---|---|
| Chronological sorting | `Scheduler.generate_plan` / `_time_sort_key` | Separates pending and completed tasks, then sorts each group by time (parsed from `"HH:MM"` into minutes since midnight); tasks with unparseable times sort last. |
| Filtering | `Pet.get_tasks`, `Owner.get_all_tasks` | Returns tasks filtered by completion status at the pet level, and by pet name and/or completion status at the owner level. |
| Recurring task generation | `Task.mark_complete` | On completion, daily tasks spawn a new occurrence due 1 day later and weekly tasks 7 days later; monthly tasks are marked complete but do not currently spawn a follow-up. |
| Conflict detection | `Scheduler.find_conflicts` | Groups pending tasks by `(due_date, time)` and flags any group containing more than one task as a scheduling conflict; tasks with unparseable times are tracked separately and reported rather than silently dropped. |

## 🗂️ Project structure

- `app.py` — Streamlit UI: add pets/tasks and generate a schedule interactively.
- `main.py` — CLI demo script showing sorting, filtering, conflict detection, and recurring tasks.
- `pawpal_system.py` — core classes: `Pet`, `Task`, `Owner`, `Scheduler`.
- `tests/test_pawpal.py` — pytest suite covering the scheduling behaviors above.
- `diagrams/uml_final.mmd` — final UML class diagram (Mermaid) for the completed system.
- `reflection.md` — write-up on design decisions and how the system evolved during implementation.
- `ai_interactions.md` — log of AI-assisted interactions used while building the project.

## 🚀 Getting started

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the app

Launch the Streamlit UI:

```bash
streamlit run app.py
```

Or run the CLI demo:

```bash
python3 main.py
```

## 📸 Demo Walkthrough

1. Enter an owner name and a pet name, then add one or more pets.
2. Select a pet and add care tasks with a time and frequency.
3. Click **Generate schedule** to build the daily plan.
4. The schedule is automatically sorted by time and displayed in a table.
5. If two tasks occur at the same time, the app displays a conflict warning.
6. The CLI demo (`python3 main.py`) also shows filtering, conflict detection, and recurring task completion (completing a task automatically creates its next occurrence).

Sample output from `python3 main.py`:

```text
========================================
         Daily Schedule - Today         
========================================

Daily plan for Biscuit (Dog):
  #  Time  Task                     Frequency  Priority  Completed
  ----------------------------------------------------------------
  1  07:00 Morning walk             daily      High      No
  2  08:00 Feed breakfast           daily      High      No

Daily plan for Whiskers (Cat):
  #  Time  Task                     Frequency  Priority  Completed
  ----------------------------------------------------------------
  1  07:00 Feed Whiskers breakfast  daily      High      No
  2  18:00 Clean litter box         weekly     Normal    No

----------------------------------------
4 task(s) still pending, 0 already completed, ordered by time. Conflict at 07:00: Morning walk (Biscuit), Feed Whiskers breakfast (Whiskers).

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: SCHEDULING CONFLICT(S) DETECTED
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  - Conflict at 07:00: Morning walk (Biscuit), Feed Whiskers breakfast (Whiskers).

Summary
-------
Total tasks: 4
Pending: 4
Completed: 0

Pending Tasks
-------------
  07:00 Morning walk (Biscuit) - daily, Due: 2026-07-05, Completed: No
  08:00 Feed breakfast (Biscuit) - daily, Due: 2026-07-05, Completed: No
  18:00 Clean litter box (Whiskers) - weekly, Due: 2026-07-05, Completed: No
  07:00 Feed Whiskers breakfast (Whiskers) - daily, Due: 2026-07-05, Completed: No

Biscuit's Tasks
---------------
  07:00 Morning walk (Biscuit) - daily, Due: 2026-07-05, Completed: No
  08:00 Feed breakfast (Biscuit) - daily, Due: 2026-07-05, Completed: No

Recurring Task Demo
===================

Biscuit's Tasks (before completing 'Morning walk')
--------------------------------------------------
  07:00 Morning walk (Biscuit) - daily, Due: 2026-07-05, Completed: No
  08:00 Feed breakfast (Biscuit) - daily, Due: 2026-07-05, Completed: No

Biscuit's Tasks (after completing 'Morning walk')
-------------------------------------------------
  07:00 Morning walk (Biscuit) - daily, Due: 2026-07-05, Completed: Yes
  08:00 Feed breakfast (Biscuit) - daily, Due: 2026-07-05, Completed: No
  07:00 Morning walk (Biscuit) - daily, Due: 2026-07-06, Completed: No
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python3 -m pytest
```

The automated tests verify:

- Task completion behavior
- Adding tasks to pets
- Sorting tasks in chronological order
- Recurring task creation for daily tasks
- Conflict detection for tasks scheduled at the same time

Sample test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/jannati/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 5 items

tests/test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.01s ===============================
```

## ⭐ Confidence Level

**Rating: 4/5 stars**

The system passes all 5 automated tests, covering task completion, adding tasks, chronological sorting, daily-recurrence generation, and conflict detection between pets — the behaviors most central to the app's value. Filtering (`Pet.get_tasks`, `Owner.get_all_tasks`), weekly recurrence, monthly tasks, and invalid/unparseable time handling are implemented and demonstrated via the CLI demo, but don't yet have dedicated pytest coverage, which is the main gap keeping this from a higher confidence rating.
