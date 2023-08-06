"""
Local Variables to work around Python annoying limitations about lambdas.

Python forbids local variables and
"""

from __future__ import annotations

from dataclasses import dataclass
from raffiot.untyped import io, resource
from raffiot.untyped.io import IO
from raffiot.untyped.resource import Resource
from collections import abc
from abc import ABC


__all__ = [
    "Val",
    "Var",
    "sequence",
]


@dataclass
class Val:
    value: None

    def get(self):
        return self.value

    def get_io(self):
        return io.defer(self.get)

    def get_rs(self):
        return resource.defer(self.get)

    @classmethod
    def pure(cls, a):
        return Val(a)

    def map(self, f):
        return Val(f(self.value))

    def flat_map(self, f):
        return f(self.value)

    @classmethod
    def zip(cls, *vals):
        if len(vals) == 1 and isinstance(vals[0], abc.Iterable):
            return Val([x.value for x in vals[0]])
        return Val([x.value for x in vals])

    def zip_with(self, *vals):
        return Val.zip(self, *vals)

    def ap(self, *arg):
        if len(arg) == 1 and isinstance(arg[0], abc.Iterable):
            l = [x.value for x in arg[0]]
        else:
            l = [x.value for x in arg]
        return Val(self.value(*l))


@dataclass
class Var(Val):
    value: None

    def set(self, v):
        old = self.value
        self.value = v
        return old

    def set_io(self, v):
        return io.defer(self.set, v)

    def set_rs(self, v):
        return resource.defer(self.set, v)

    @classmethod
    def pure(cls, a):
        return Var(a)

    def map(self, f):
        return Var(f(self.value))

    def flat_map(self, f):
        return f(self.value)

    @classmethod
    def zip(cls, *vars):
        if len(vars) == 1 and isinstance(vars[0], abc.Iterable):
            return Var([x.value for x in vars[0]])
        return Var([x.value for x in vars])

    def zip_with(self, *vars):
        return Var.zip(self, *vars)

    def ap(self, *arg):
        if len(arg) == 1 and isinstance(arg[0], abc.Iterable):
            l = [x.value for x in arg[0]]
        else:
            l = [x.value for x in arg]
        return Var(self.value(*l))


def sequence(*a):
    if len(a) == 1 and isinstance(a[0], abc.Iterable):
        return a[0][-1]
    return a[-1]
