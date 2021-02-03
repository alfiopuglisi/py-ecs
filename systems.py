#!/usr/bin/env python


_systems = []


def register(system):
    _systems.append(system)


def run():
    for system in _systems:
        system()

