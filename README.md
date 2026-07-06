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

Running `python main.py` with two pets (Biscuit and Mochi) and 90 minutes available:

```
======================================================
  Today's Schedule for Jordan (2026-07-06)
======================================================
  08:00  Feeding                  5 min  [high  ]  Mochi
  08:05  Breakfast               10 min  [high  ]  Biscuit
  08:15  Morning walk            30 min  [high  ]  Biscuit
  08:45  Playtime                20 min  [medium]  Mochi
  09:05  Nail trim               10 min  [low   ]  Mochi
  09:15  Brush coat              15 min  [low   ]  Biscuit

  Total: 90 min scheduled
======================================================

Plan for Jordan on 2026-07-06.
Available time: 90 min.
Tasks sorted by priority (high → medium → low), then shortest first.

  08:00  Feeding [high] → Mochi
  08:05  Breakfast [high] → Biscuit
  08:15  Morning walk [high] → Biscuit
  08:45  Playtime [medium] → Mochi
  09:05  Nail trim [low] → Mochi
  09:15  Brush coat [low] → Biscuit
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

### What the tests cover

| Test | Behaviour verified |
|------|--------------------|
| `test_mark_complete_changes_status` | `completed` flips to `True` after `mark_complete()` |
| `test_add_task_increases_pet_task_count` | `Pet.add_task()` grows the task list correctly |
| `test_scheduler_respects_time_budget` | Tasks that exceed the budget land in `skipped_tasks` |
| `test_high_priority_scheduled_before_low` | Priority ordering is respected in the generated plan |
| `test_recurring_daily_task_produces_next_day` | Daily task returns a new task due the following day |
| `test_once_task_returns_none_on_complete` | One-off task returns `None` (no next occurrence) |
| `test_filter_tasks_by_pet_name` | `filter_tasks()` isolates tasks for one pet |
| `test_detect_conflicts_finds_overlap` | Overlapping slots produce a conflict warning |
| `test_detect_conflicts_no_overlap` | Back-to-back slots produce no warnings |
| `test_sort_by_time_returns_chronological_order` | `sort_by_time()` returns slots in HH:MM ascending order |
| `test_pet_with_no_tasks_produces_empty_plan` | A pet with zero tasks generates an empty, valid plan |
| `test_exact_same_start_time_is_a_conflict` | Identical start times are correctly flagged |

### Test run output

```
============================= test session starts ==============================
platform darwin -- Python 3.12.6, pytest-9.0.3
collected 12 items

test_pawpal.py::test_mark_complete_changes_status PASSED                 [  8%]
test_pawpal.py::test_add_task_increases_pet_task_count PASSED            [ 16%]
test_pawpal.py::test_scheduler_respects_time_budget PASSED               [ 25%]
test_pawpal.py::test_high_priority_scheduled_before_low PASSED           [ 33%]
test_pawpal.py::test_recurring_daily_task_produces_next_day PASSED       [ 41%]
test_pawpal.py::test_once_task_returns_none_on_complete PASSED           [ 50%]
test_pawpal.py::test_filter_tasks_by_pet_name PASSED                     [ 58%]
test_pawpal.py::test_detect_conflicts_finds_overlap PASSED               [ 66%]
test_pawpal.py::test_detect_conflicts_no_overlap PASSED                  [ 75%]
test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED     [ 83%]
test_pawpal.py::test_pet_with_no_tasks_produces_empty_plan PASSED        [ 91%]
test_pawpal.py::test_exact_same_start_time_is_a_conflict PASSED          [100%]

============================== 12 passed in 0.02s ===============================
```

### Confidence level: ⭐⭐⭐⭐ (4/5)

The suite covers all core behaviors — priority sorting, time budget, recurrence, filtering, conflict detection — and explicitly tests both happy paths and edge cases (zero tasks, identical start times). One star withheld because conflict detection only checks exact time overlap and does not account for buffer time or logical incompatibilities between task types.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority + duration sort | `Scheduler.generate_plan()` | Tasks sorted high→medium→low, then shortest first within each tier |
| Sort by start time | `Scheduler.sort_by_time()` | Returns slots in HH:MM order; HH:MM strings sort correctly as plain strings |
| Filter by pet / status | `Scheduler.filter_tasks(pet_name, completed)` | Returns `(Pet, Task)` pairs; both filters are optional and combinable |
| Conflict detection | `Scheduler.detect_conflicts()` | Pairwise overlap check; returns warning strings, never crashes |
| Recurring tasks | `Task.mark_complete(today)` | Returns a new `Task` for the next occurrence (`+1 day` daily, `+7 days` weekly); returns `None` for one-off tasks |

## ✨ Features

| Feature | Description |
|---------|-------------|
| Owner + pet management | Add an owner with a daily time budget, then add multiple pets to their household |
| Task creation | Assign tasks to specific pets with name, duration, priority, category, and frequency (daily / weekly / once) |
| Smart scheduling | Tasks are sorted by priority (high → medium → low) then by duration (shortest first); greedy assignment fills the time budget |
| Conflict detection | After scheduling, the app checks every pair of slots for time overlap and displays a warning for each conflict |
| Sort by start time | Toggle to redisplay the schedule sorted chronologically rather than by priority |
| Task filtering | Filter the task list by pet name and/or completion status |
| Recurring tasks | Completing a daily or weekly task returns a new task instance with the next due date pre-filled |
| Reasoning display | An expandable "Why this order?" section explains every scheduling decision in plain language |

## 📸 Demo Walkthrough

### UI workflow (Streamlit — `streamlit run app.py`)

1. **Enter owner info** — type your name and how many minutes you have free today, then click "Save owner info." The app stores this in session state so it persists across button clicks.
2. **Add pets** — fill in a pet name, breed, and species, then click "Add pet." Repeat for each pet. Each pet appears in the sidebar summary immediately.
3. **Add tasks** — choose which pet the task belongs to, enter a name, duration, priority, category, and frequency, then click "Add task." Tasks accumulate and are visible in the Task Overview.
4. **Filter tasks** — use the "Filter by pet" and "Filter by status" dropdowns in the Task Overview to zero in on incomplete high-priority tasks, or all tasks for one pet.
5. **Generate schedule** — set a start time (default 08:00), optionally tick "Sort display by start time," and click "Generate schedule." The app calls `Scheduler.generate_plan()`, shows the sorted schedule as a table, flags any conflicts in amber warnings, and lists skipped tasks in an expander.
6. **Read the reasoning** — expand "Why this order?" to see `Scheduler.explain_plan()` output: which tasks were chosen, in what order, and why.

### CLI workflow (`python main.py`)

```
========================================================
  Today's Schedule for Jordan (2026-07-06)
========================================================
  08:00  Feeding                  5 min  [high  ]  Mochi
  08:05  Breakfast               10 min  [high  ]  Biscuit
  08:15  Morning walk            30 min  [high  ]  Biscuit
  08:45  Playtime                20 min  [medium]  Mochi
  09:05  Nail trim               10 min  [low   ]  Mochi
  09:15  Brush coat              15 min  [low   ]  Biscuit

  Total: 90 min scheduled
========================================================

--- Recurring task completed ---
  'Morning walk' marked done for 2026-07-06.
  Next occurrence created: 'Morning walk' due 2026-07-07

--- Conflict detection demo ---
  ⚠ Conflict: 'Vet appointment' (Biscuit, 09:00–09:45) overlaps 'Training session' (Biscuit, 09:15–09:45)
```
