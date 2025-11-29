"""Behavior tree node definitions."""

from __future__ import annotations

from typing import Any, Iterable


class BTNode:
    """Base behavior tree node."""

    name: str

    def __init__(self, name: str | None = None) -> None:
        self.name = name or self.__class__.__name__

    def tick(self, ctx: dict) -> bool:  # pragma: no cover - interface method
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.name}>"


class SequenceNode(BTNode):
    """Executes children in order until one fails."""

    def __init__(self, *children: BTNode, name: str | None = None) -> None:
        super().__init__(name)
        self.children: Iterable[BTNode] = children

    def tick(self, ctx: dict) -> bool:
        for child in self.children:
            if not child.tick(ctx):
                _record_trace(ctx, self.name, False)
                return False
        _record_trace(ctx, self.name, True)
        return True


class SelectorNode(BTNode):
    """Executes children until one succeeds."""

    def __init__(self, *children: BTNode, name: str | None = None) -> None:
        super().__init__(name)
        self.children: Iterable[BTNode] = children

    def tick(self, ctx: dict) -> bool:
        for child in self.children:
            if child.tick(ctx):
                _record_trace(ctx, self.name, True)
                return True
        _record_trace(ctx, self.name, False)
        return False


class ConditionNode(BTNode):
    """Runs a condition function that returns True/False."""

    def __init__(self, fn, name: str | None = None) -> None:
        super().__init__(name)
        self.fn = fn

    def tick(self, ctx: dict) -> bool:
        result = bool(self.fn(ctx))
        _record_trace(ctx, self.name, result)
        return result


class ActionNode(BTNode):
    """Runs an action function that returns True/False."""

    def __init__(self, fn, name: str | None = None) -> None:
        super().__init__(name)
        self.fn = fn

    def tick(self, ctx: dict) -> bool:
        result = bool(self.fn(ctx))
        _record_trace(ctx, self.name, result)
        return result


def _record_trace(ctx: dict, node_name: str, result: bool) -> None:
    trace = ctx.setdefault("trace", [])
    trace.append({"node": node_name, "result": result})
