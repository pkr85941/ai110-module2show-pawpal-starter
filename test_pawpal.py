from pawpal_system import Owner, Pet, Task, Scheduler, DailyPlan


# ---------------------------------------------------------------------------
# Original tests (Phase 3)
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = Task("Morning walk", 30, priority="high", category="walk")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", breed="Golden Retriever")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", 20))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Feed", 10))
    assert len(pet.tasks) == 2


def test_scheduler_respects_time_budget():
    owner = Owner(name="Jordan", available_minutes=30)
    pet = Pet(name="Biscuit", breed="Golden Retriever")
    pet.add_task(Task("Walk", 30, priority="high"))
    pet.add_task(Task("Grooming", 20, priority="medium"))
    owner.add_pet(pet)
    plan = Scheduler(owner).generate_plan()
    assert plan.total_time_used <= 30
    assert len(plan.skipped_tasks) == 1


def test_high_priority_scheduled_before_low():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", breed="Siamese Cat", species="cat")
    pet.add_task(Task("Nail trim", 10, priority="low"))
    pet.add_task(Task("Feeding",    5, priority="high"))
    owner.add_pet(pet)
    plan = Scheduler(owner).generate_plan()
    scheduled_names = [task.name for _, _, task in plan.slots]
    assert scheduled_names.index("Feeding") < scheduled_names.index("Nail trim")


# ---------------------------------------------------------------------------
# New tests (Phase 4)
# ---------------------------------------------------------------------------

def test_recurring_daily_task_produces_next_day():
    task = Task("Morning walk", 30, priority="high", frequency="daily")
    next_task = task.mark_complete(today="2026-07-06")
    assert next_task is not None
    assert next_task.due_date == "2026-07-07"
    assert next_task.completed is False


def test_once_task_returns_none_on_complete():
    task = Task("Vet checkup", 60, priority="high", frequency="once")
    result = task.mark_complete(today="2026-07-06")
    assert result is None


def test_filter_tasks_by_pet_name():
    owner = Owner(name="Jordan", available_minutes=120)
    biscuit = Pet(name="Biscuit", breed="Golden Retriever")
    mochi   = Pet(name="Mochi",   breed="Siamese Cat", species="cat")
    biscuit.add_task(Task("Walk", 30, priority="high"))
    mochi.add_task(  Task("Feed",  5, priority="high"))
    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    scheduler = Scheduler(owner)
    results = scheduler.filter_tasks(pet_name="Biscuit")
    assert len(results) == 1
    assert results[0][1].name == "Walk"


def test_detect_conflicts_finds_overlap():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Biscuit", breed="Golden Retriever")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.plan = DailyPlan(date="2026-07-06", owner_name="Jordan")
    scheduler.plan.add_slot("09:00", pet, Task("Vet appointment", 45, priority="high"))
    scheduler.plan.add_slot("09:15", pet, Task("Training",        30, priority="medium"))
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "Conflict" in warnings[0]


def test_detect_conflicts_no_overlap():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Biscuit", breed="Golden Retriever")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    scheduler.plan = DailyPlan(date="2026-07-06", owner_name="Jordan")
    scheduler.plan.add_slot("09:00", pet, Task("Walk",  30, priority="high"))
    scheduler.plan.add_slot("09:30", pet, Task("Feed",  10, priority="high"))
    warnings = scheduler.detect_conflicts()
    assert warnings == []
