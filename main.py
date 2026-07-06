from pawpal_system import Owner, Pet, Task, Scheduler

# --- Owner setup ---
owner = Owner(name="Jordan", available_minutes=90)

# --- Pets ---
biscuit = Pet(name="Biscuit", breed="Golden Retriever")
mochi = Pet(name="Mochi", breed="Siamese Cat", species="cat")

owner.add_pet(biscuit)
owner.add_pet(mochi)

# --- Tasks for Biscuit ---
biscuit.add_task(Task("Morning walk",  30, priority="high",   category="walk"))
biscuit.add_task(Task("Breakfast",     10, priority="high",   category="feed"))
biscuit.add_task(Task("Brush coat",    15, priority="low",    category="grooming"))

# --- Tasks for Mochi ---
mochi.add_task(Task("Feeding",          5, priority="high",   category="feed"))
mochi.add_task(Task("Playtime",        20, priority="medium", category="enrichment"))
mochi.add_task(Task("Nail trim",       10, priority="low",    category="grooming"))

# --- Generate and display ---
scheduler = Scheduler(owner)
plan = scheduler.generate_plan(date="2026-07-06", start_time="08:00")
plan.display()

print(scheduler.explain_plan())
