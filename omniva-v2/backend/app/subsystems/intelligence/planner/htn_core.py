"""Core data structures for a simple Hierarchical Task Network (HTN) planner."""

from __future__ import annotations

from typing import Callable, Dict, Iterable, List


class HTNTask:
    """Represents an abstract task within the HTN."""

    def __init__(self, name: str):
        self.name = name


class HTNMethod:
    """Represents one way to decompose a task into subtasks or primitive actions."""

    def __init__(
        self,
        name: str,
        task_name: str,
        condition_fn: Callable[[Dict], bool],
        subtasks: Iterable[str],
    ) -> None:
        self.name = name
        self.task_name = task_name
        self.condition_fn = condition_fn
        self.subtasks = list(subtasks)


class HTNPlanner:
    """Small HTN engine that recursively expands tasks by applicable methods."""

    def __init__(self, tasks: Dict[str, HTNTask] | None = None, methods: List[HTNMethod] | None = None):
        self.tasks = tasks or {}
        self.methods = methods or []

    def add_task(self, task: HTNTask) -> None:
        self.tasks[task.name] = task

    def add_method(self, method: HTNMethod) -> None:
        self.methods.append(method)

    def applicable_methods(self, task_name: str, ctx: Dict) -> List[HTNMethod]:
        return [method for method in self.methods if method.task_name == task_name and method.condition_fn(ctx)]

    def plan(self, task_name: str, ctx: Dict) -> List[str]:
        if task_name not in self.tasks:
            raise ValueError(f"Unknown task: {task_name}")

        methods = self.applicable_methods(task_name, ctx)
        if not methods:
            return []

        method = methods[0]
        plan: List[str] = []
        for subtask in method.subtasks:
            if subtask.startswith("action:"):
                plan.append(subtask)
            else:
                plan.extend(self.plan(subtask, ctx))
        return plan
