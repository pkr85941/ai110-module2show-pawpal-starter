from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Owner:
    name: str
    available_minutes: int

    def set_availability(self, minutes: int) -> None:
        self.available_minutes = minutes

    def summary(self) -> str:
        return f"{self.name} ({self.available_minutes} min available today)"


@dataclass
class Pet:
    name: str
    breed: str
    species: str = "dog"

    def summary(self) -> str:
        return f"{self.name} the {self.breed}"


Priority = Literal["high", "medium", "low"]
Category = Literal["walk", "feed", "meds", "grooming", "enrichment", "other"]


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority = "medium"
    category: Category = "other"
    recurring: bool = True

    def is_high_priority(self) -> bool:
        return self.priority == "high"

    def __repr__(self) -> str:
        return f"[{self.priority.upper()}] {self.name} ({self.duration_minutes} min)"


@dataclass
class DailyPlan:
    date: str
    slots: list[tuple[str, Task]] = field(default_factory=list)  # (start_time, Task)
    skipped_tasks: list[Task] = field(default_factory=list)

    @property
    def total_time_used(self) -> int:
        return sum(task.duration_minutes for _, task in self.slots)

    def display(self) -> None:
        print(f"\nDaily plan for {self.date}:")
        for start_time, task in self.slots:
            print(f"  {start_time} — {task}")
        if self.skipped_tasks:
            print("Skipped (not enough time):")
            for task in self.skipped_tasks:
                print(f"  {task}")

    def summary(self) -> str:
        n = len(self.slots)
        return f"{n} task(s) scheduled, {self.total_time_used} min total"


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks: list[Task] = []
        self.plan: DailyPlan | None = None

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)

    def generate_plan(self, date: str = "today") -> DailyPlan:
        # Placeholder: real scheduling logic goes here
        self.plan = DailyPlan(date=date)
        return self.plan

    def explain_plan(self) -> str:
        # Placeholder: return human-readable reasoning for the generated plan
        return ""
