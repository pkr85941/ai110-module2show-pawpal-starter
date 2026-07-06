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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.12.6, pytest-9.0.3
collected 9 items

test_pawpal.py::test_mark_complete_changes_status PASSED                 [ 11%]
test_pawpal.py::test_add_task_increases_pet_task_count PASSED            [ 22%]
test_pawpal.py::test_scheduler_respects_time_budget PASSED               [ 33%]
test_pawpal.py::test_high_priority_scheduled_before_low PASSED           [ 44%]
test_pawpal.py::test_recurring_daily_task_produces_next_day PASSED       [ 55%]
test_pawpal.py::test_once_task_returns_none_on_complete PASSED           [ 66%]
test_pawpal.py::test_filter_tasks_by_pet_name PASSED                     [ 77%]
test_pawpal.py::test_detect_conflicts_finds_overlap PASSED               [ 88%]
test_pawpal.py::test_detect_conflicts_no_overlap PASSED                  [100%]

============================== 9 passed in 0.02s ===============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority + duration sort | `Scheduler.generate_plan()` | Tasks sorted high→medium→low, then shortest first within each tier |
| Sort by start time | `Scheduler.sort_by_time()` | Returns slots in HH:MM order; HH:MM strings sort correctly as plain strings |
| Filter by pet / status | `Scheduler.filter_tasks(pet_name, completed)` | Returns `(Pet, Task)` pairs; both filters are optional and combinable |
| Conflict detection | `Scheduler.detect_conflicts()` | Pairwise overlap check; returns warning strings, never crashes |
| Recurring tasks | `Task.mark_complete(today)` | Returns a new `Task` for the next occurrence (`+1 day` daily, `+7 days` weekly); returns `None` for one-off tasks |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
