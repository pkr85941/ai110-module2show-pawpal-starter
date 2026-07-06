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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
