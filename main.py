from pawpal_system import Owner, Pet, Task, Scheduler, DailyPlan

TODAY = "2026-07-06"

# ---------------------------------------------------------------------------
# Setup: owner + two pets
# ---------------------------------------------------------------------------
owner = Owner(name="Jordan", available_minutes=90)

biscuit = Pet(name="Biscuit", breed="Golden Retriever")
mochi   = Pet(name="Mochi",   breed="Siamese Cat", species="cat")

owner.add_pet(biscuit)
owner.add_pet(mochi)

# Tasks added deliberately out of priority order to show sorting later
biscuit.add_task(Task("Brush coat",    15, priority="low",    category="grooming",   frequency="weekly"))
biscuit.add_task(Task("Morning walk",  30, priority="high",   category="walk",       frequency="daily"))
biscuit.add_task(Task("Breakfast",     10, priority="high",   category="feed",       frequency="daily"))
mochi.add_task(  Task("Playtime",      20, priority="medium", category="enrichment", frequency="daily"))
mochi.add_task(  Task("Feeding",        5, priority="high",   category="feed",       frequency="daily"))
mochi.add_task(  Task("Nail trim",     10, priority="low",    category="grooming",   frequency="weekly"))

# ---------------------------------------------------------------------------
# 1. Generate plan (priority + duration sort, greedy fit)
# ---------------------------------------------------------------------------
scheduler = Scheduler(owner)
plan = scheduler.generate_plan(date=TODAY, start_time="08:00")
plan.display()
print(scheduler.explain_plan())

# ---------------------------------------------------------------------------
# 2. Sorting — re-order slots by start time
#    (useful if slots were manually added out of order)
# ---------------------------------------------------------------------------
print("\n--- Sorted by start time ---")
for t, pet, task in scheduler.sort_by_time():
    print(f"  {t}  {task.name:<22} → {pet.name}")

# ---------------------------------------------------------------------------
# 3. Filtering — show only incomplete high-priority tasks for Biscuit
# ---------------------------------------------------------------------------
print("\n--- Biscuit's incomplete tasks ---")
for pet, task in scheduler.filter_tasks(pet_name="Biscuit", completed=False):
    print(f"  [{task.priority}] {task.name}")

print("\n--- All incomplete tasks across all pets ---")
for pet, task in scheduler.filter_tasks(completed=False):
    print(f"  {pet.name}: {task.name}")

# ---------------------------------------------------------------------------
# 4. Recurring tasks — mark Morning walk complete, get next occurrence
# ---------------------------------------------------------------------------
walk = biscuit.tasks[1]          # Morning walk (daily)
next_task = walk.mark_complete(today=TODAY)
print(f"\n--- Recurring task completed ---")
print(f"  '{walk.name}' marked done for {TODAY}.")
if next_task:
    biscuit.add_task(next_task)
    print(f"  Next occurrence created: '{next_task.name}' due {next_task.due_date}")

# ---------------------------------------------------------------------------
# 5. Conflict detection — manually build a plan with two overlapping slots
# ---------------------------------------------------------------------------
print("\n--- Conflict detection demo ---")
conflict_plan = DailyPlan(date=TODAY, owner_name="Jordan")
conflict_plan.add_slot("09:00", biscuit, Task("Vet appointment", 45, priority="high",  category="meds"))
conflict_plan.add_slot("09:15", biscuit, Task("Training session", 30, priority="medium", category="other"))

scheduler.plan = conflict_plan
warnings = scheduler.detect_conflicts()
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")
