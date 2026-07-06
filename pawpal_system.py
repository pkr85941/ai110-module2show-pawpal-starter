from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

Priority = Literal["high", "medium", "low"]
Category = Literal["walk", "feed", "meds", "grooming", "enrichment", "other"]

_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority = "medium"
    category: Category = "other"
    recurring: bool = True
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done for today."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task has high priority."""
        return self.priority == "high"

    def __repr__(self) -> str:
        status = "✓" if self.completed else " "
        return f"[{status}][{self.priority.upper()}] {self.name} ({self.duration_minutes} min)"


@dataclass
class Pet:
    name: str
    breed: str
    species: str = "dog"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a specific task instance by identity (not value equality)."""
        self.tasks = [t for t in self.tasks if t is not task]

    def summary(self) -> str:
        """Return a one-line description of the pet."""
        return f"{self.name} the {self.breed} ({len(self.tasks)} task(s))"


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's household."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all (pet, task) pairs across every pet the owner has."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]

    def set_availability(self, minutes: int) -> None:
        """Update how many minutes the owner has available today."""
        self.available_minutes = minutes

    def summary(self) -> str:
        """Return a one-line description of the owner and their household."""
        return f"{self.name} — {len(self.pets)} pet(s), {self.available_minutes} min available today"


def _add_minutes(time_str: str, minutes: int) -> str:
    """Advance a HH:MM string by the given number of minutes."""
    h, m = map(int, time_str.split(":"))
    total = h * 60 + m + minutes
    return f"{total // 60:02d}:{total % 60:02d}"


@dataclass
class DailyPlan:
    date: str
    owner_name: str = ""
    start_time: str = "08:00"
    slots: list[tuple[str, Pet, Task]] = field(default_factory=list)  # (HH:MM, Pet, Task)
    skipped_tasks: list[tuple[Pet, Task]] = field(default_factory=list)

    @property
    def total_time_used(self) -> int:
        """Return the total number of scheduled minutes."""
        return sum(task.duration_minutes for _, _, task in self.slots)

    def display(self) -> None:
        """Print the full schedule to the terminal in a readable format."""
        header = (
            f"Today's Schedule for {self.owner_name} ({self.date})"
            if self.owner_name
            else f"Schedule — {self.date}"
        )
        print(f"\n{'=' * 54}")
        print(f"  {header}")
        print(f"{'=' * 54}")
        for time_str, pet, task in self.slots:
            print(
                f"  {time_str}  {task.name:<22} {task.duration_minutes:>3} min"
                f"  [{task.priority:<6}]  {pet.name}"
            )
        if self.skipped_tasks:
            print(f"\n  Skipped — not enough time ({len(self.skipped_tasks)}):")
            for pet, task in self.skipped_tasks:
                print(f"    • {task.name} ({task.duration_minutes} min) [{task.priority}] → {pet.name}")
        print(f"\n  Total: {self.total_time_used} min scheduled")
        print(f"{'=' * 54}\n")

    def summary(self) -> str:
        """Return a one-line summary of the plan."""
        return (
            f"{len(self.slots)} task(s) scheduled, "
            f"{self.total_time_used} min used, "
            f"{len(self.skipped_tasks)} skipped"
        )


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Initialise the scheduler with an owner (and their pets and tasks)."""
        self.owner = owner
        self.plan: DailyPlan | None = None

    def generate_plan(self, date: str = "today", start_time: str = "08:00") -> DailyPlan:
        """Sort tasks by priority then duration and fit them into the owner's time budget."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = sorted(
            all_tasks,
            key=lambda pt: (_PRIORITY_ORDER[pt[1].priority], pt[1].duration_minutes),
        )

        plan = DailyPlan(date=date, owner_name=self.owner.name, start_time=start_time)
        budget = self.owner.available_minutes
        current_time = start_time

        for pet, task in sorted_tasks:
            if task.duration_minutes <= budget:
                plan.slots.append((current_time, pet, task))
                current_time = _add_minutes(current_time, task.duration_minutes)
                budget -= task.duration_minutes
            else:
                plan.skipped_tasks.append((pet, task))

        self.plan = plan
        return plan

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why tasks were ordered as they were."""
        if self.plan is None:
            return "No plan generated yet — call generate_plan() first."
        lines = [
            f"Plan for {self.owner.name} on {self.plan.date}.",
            f"Available time: {self.owner.available_minutes} min.",
            "Tasks sorted by priority (high → medium → low), then shortest first.",
            "",
        ]
        for time_str, pet, task in self.plan.slots:
            lines.append(f"  {time_str}  {task.name} [{task.priority}] → {pet.name}")
        if self.plan.skipped_tasks:
            lines.append(f"\nSkipped (exceeded time budget):")
            for pet, task in self.plan.skipped_tasks:
                lines.append(f"  • {task.name} ({task.duration_minutes} min) → {pet.name}")
        return "\n".join(lines)
