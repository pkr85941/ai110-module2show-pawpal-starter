from pawpal_system import Owner, Pet, Task, Scheduler


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
