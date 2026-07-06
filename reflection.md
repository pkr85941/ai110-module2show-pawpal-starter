# PawPal+ Project Reflection

## 1. System Design

**a. Core user actions**

The three core actions a user can perform in PawPal+ are:

1. **Enter pet and owner info**: The user provides their name, their pet's name and breed, and how much time they have available for the day. This gives the scheduler the constraints it needs before building a plan.

2. **Add and manage care tasks**: The user creates tasks such as a morning walk, feeding, medication, or grooming, specifying a duration and a priority level for each. These tasks are the raw material the scheduler works from; without them there is nothing to plan.

3. **Generate and view today's schedule**: The user triggers schedule generation and receives a time-ordered daily plan showing each task's start time, duration, and priority. The plan should also explain why tasks were ordered the way they were, so the owner understands and trusts the output.

**b. Initial design**

The initial design has five classes:

- **Owner** — holds the user's name and how many minutes they have available today. Responsible for representing the human-side constraints the scheduler must respect.
- **Pet** — holds the pet's name, breed, and species. A pure data object with no scheduling logic; it exists so the plan output can reference the pet by name.
- **Task** — holds everything about a single care activity: name, duration, priority, category, and whether it recurs daily. Responsible for expressing one unit of work. Uses a dataclass for clean equality and default values.
- **Scheduler** — the central coordinator. Holds an `Owner`, a `Pet`, and a list of `Task`s. Responsible for accepting tasks, running the scheduling algorithm (`generate_plan`), and explaining the result (`explain_plan`). The only class that is not a dataclass, because it owns mutable state and behavior.
- **DailyPlan** — the output of the scheduler. Holds the ordered list of `(start_time, Task)` slots and any tasks that were skipped due to time constraints. Responsible for displaying the plan to the user and summarizing it in one line.

**b. Design changes**

After reviewing the skeleton, three issues were identified and two were fixed:

1. **Added `start_time` to `generate_plan()` and `DailyPlan`** — the original skeleton accepted only a `date`, which meant the scheduler had no way to compute when each slot begins. Adding `start_time: str = "08:00"` to both `generate_plan()` and `DailyPlan` gives the scheduling logic the anchor it needs to place tasks on a timeline.

2. **Added `pet_name` to `DailyPlan`** — `DailyPlan.display()` originally printed "Daily plan for {date}" with no mention of the pet. Since `DailyPlan` is a standalone output object (it does not hold a reference to `Pet`), the pet's name is passed in as a plain string when the plan is created, keeping the class self-contained while making the output meaningful.

3. **`remove_task()` matches by value (noted, not yet fixed)** — because `Task` is a dataclass, two tasks with identical fields are considered equal, so `list.remove()` could delete the wrong one if duplicates exist. This will be addressed when the scheduling logic is implemented, likely by assigning each task a unique ID.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two constraints: **available time** (the owner's total minutes for the day) and **task priority** (high / medium / low). Tasks are sorted by priority first and by duration second (shortest first as a tiebreaker), then greedily assigned to time slots until the budget is exhausted. Tasks that do not fit are placed in a `skipped_tasks` list rather than dropped silently.

Priority was treated as the most important constraint because missing a high-priority task (medication, feeding) has a real consequence for the pet, whereas missing a low-priority grooming session does not. Duration as a secondary sort means that within the same priority tier, shorter tasks are scheduled first — this maximises the number of tasks that fit within the budget.

**b. Tradeoffs**

The conflict detector checks only for **exact time-slot overlap** — it compares whether one task's start-to-end window intersects another's. It does not account for travel time between tasks, buffer time for the owner to recover, or tasks that are logically incompatible (e.g., feeding a dog right before a vigorous walk). This keeps the detection simple and fast (O(n²) pairwise scan), and avoids requiring the owner to enter extra data the app has no way to collect. For a pet care app with 5–15 daily tasks, the performance cost is negligible and the simplification is reasonable. A future version could add a configurable "buffer minutes" field to each task to make the detection more realistic.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used at every phase of the project, but in different roles at each stage:

- **Design brainstorming (Phase 1):** Asked the AI to identify the main objects in the system and suggest their attributes and methods. The AI produced a clear first draft of the five classes quickly, which gave us a concrete starting point to react to rather than a blank page.
- **Skeleton review (Phase 2):** Attached `pawpal_system.py` and asked the AI to flag missing relationships or logic bottlenecks. This produced three actionable findings — the missing `start_time`, the missing `pet_name` on `DailyPlan`, and the value-equality ambiguity in `remove_task()`.
- **Algorithm design (Phase 4):** Asked the AI how to use a `lambda` key with `sorted()` for HH:MM strings. The AI correctly explained that lexicographic ordering works for HH:MM — a non-obvious fact that saved time.
- **Test drafting (Phase 5):** Asked the AI for a test plan focused on edge cases (zero tasks, exact same start time). The resulting tests caught real gaps in coverage.
- **Most effective prompt pattern:** Attaching a file and asking "what's missing or could go wrong?" consistently produced more useful output than open-ended "help me build X" prompts, because it forced the AI to react to real code rather than invent a generic answer.

**b. Judgment and verification**

The clearest moment of rejection was around `remove_task()`. The AI's initial suggestion used `self.tasks.remove(task)`, which removes by value equality. Because `Task` is a dataclass, two tasks with identical field values are considered equal — so `remove_task()` could silently delete the wrong task if duplicates existed. The AI's suggestion would have passed a basic test but introduced a subtle bug in real use. The fix was to replace it with an identity check: `self.tasks = [t for t in self.tasks if t is not task]`. This was verified by writing a test that added two tasks with identical values, removed one by reference, and confirmed only one remained.

A second moment: the AI suggested having `Scheduler` take both `Owner` and `Pet` as constructor arguments (mirroring the original skeleton). This was rejected because it implied the scheduler could only handle one pet. Passing only `Owner` — and having it expose `get_all_tasks()` — kept the design open to multiple pets without changing the Scheduler's interface.

**How separate chat sessions helped:** Keeping Phase 1 design, Phase 3 implementation, and Phase 5 testing in separate sessions prevented earlier context from bleeding into later questions. When asking "what edge cases should I test?", the AI gave sharper answers because it wasn't also trying to remember the design decisions from three phases earlier.

---

## 4. Testing and Verification

**a. What you tested**

The 12-test suite covers:

- **Core data operations:** `mark_complete()` changes the `completed` flag; `add_task()` grows the task list.
- **Scheduling correctness:** The greedy algorithm respects the time budget; high-priority tasks are placed before low-priority ones.
- **Recurrence logic:** Daily tasks return a next-day instance; one-off tasks return `None`.
- **Filtering:** `filter_tasks(pet_name=...)` returns only tasks belonging to the named pet.
- **Conflict detection:** Overlapping slots produce warnings; back-to-back slots do not; identical start times are caught.
- **Sort order:** `sort_by_time()` returns slots in strict chronological order regardless of insertion order.
- **Edge case — zero tasks:** An owner with a pet but no tasks produces an empty, valid `DailyPlan` with no errors.

These tests matter because the scheduling logic is the core value of the app. A bug in priority ordering or time-budget enforcement would produce a plan that looks plausible but misleads the user — exactly the kind of failure that is hard to notice without automated checks.

**b. Confidence**

**4 / 5 stars.** The suite covers all stated behaviors with both happy paths and edge cases. The missing star reflects two known limitations: (1) conflict detection does not account for buffer time between tasks, so a "Walk (30 min) at 09:00" followed by "Feed at 09:30" could conflict in practice but not in code; (2) `remove_task()` is fixed for identity but there is still no unique-ID system, which could cause subtle issues if the same task object is added to multiple pets. Next tests would cover: filtering by completed status, weekly recurrence producing a 7-day offset, and scheduling behavior when all tasks have equal priority.

---

## 5. Reflection

**a. What went well**

The cleanest part of the project is the separation between the five classes. Because `Task` is pure data, `Pet` owns its tasks, `Owner` aggregates pets, `Scheduler` handles all logic, and `DailyPlan` is a pure output object, each part could be built and tested independently. The `filter_tasks()` and `detect_conflicts()` methods required no changes to any other class — they were added to `Scheduler` without touching `Task`, `Pet`, or `DailyPlan`. That separation is the part of the design most worth keeping.

**b. What you would improve**

Two things stand out for a next iteration:

1. **Unique task IDs.** Every `Task` should carry a UUID generated at creation time. This would make `remove_task()` unambiguous and make it possible to track which specific instance was completed (important for recurring tasks, where two instances of "Morning walk" are otherwise indistinguishable).
2. **Buffer time on tasks.** A `buffer_after_minutes: int = 0` field on `Task` would let the conflict detector catch cases like scheduling a vigorous walk immediately before feeding — currently invisible to the system.

**c. Key takeaway**

The most important thing learned is that AI accelerates production but does not replace architecture decisions. AI generated correct code quickly at every step, but it could not decide: which class should own the task list, whether conflict detection should raise exceptions or return strings, or whether `recurring: bool` was too coarse a field. Those decisions required understanding the full system — what each class was responsible for, what would make testing easier, what a pet owner actually needs to see. The human role in this project was not to write code; it was to decide what the code should mean. That role did not shrink as the AI's contributions grew.

