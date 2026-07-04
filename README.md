# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:


## 🖥️ Sample Output


```
========================================
         Daily Schedule - Today         
========================================

Daily plan for Biscuit (Dog):
  #  Time  Task              Frequency  Priority  Completed
  ---------------------------------------------------------
  1  07:00 Morning walk      daily      High      No
  2  08:00 Feed breakfast    daily      High      No

Daily plan for Whiskers (Cat):
  #  Time  Task              Frequency  Priority  Completed
  ---------------------------------------------------------
  1  18:00 Clean litter box  weekly     Normal    No

----------------------------------------
3 task(s) still pending, 0 already completed, ordered by time.

Summary
-------
Total tasks: 3
Pending: 3
Completed: 0
```


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```


## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting by time | `Scheduler.generate_plan()`, `_safe_parse_time()` | Tasks are sorted by time in chronological order. Invalid times are handled safely. |
| Filtering by pet or completion status | `Owner.get_all_tasks(pet_name, completed)`, `Pet.get_tasks(completed)`, `Scheduler.generate_plan(pet_name, completed)` | The scheduler can show tasks for one pet, only pending tasks, or only completed tasks. |
| Recurring task logic | `Task.mark_complete()`, `Task.is_due(reference_date)`, `Pet.complete_task()` | Completing a daily or weekly task creates a new task for the next due date. |
| Conflict detection | `Scheduler.find_conflicts()` | The scheduler warns when two pending tasks share the same due date and start time. |


## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
