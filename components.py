#!/usr/bin/env python
'''
Components management

Stores all components internally, grouping components by class.
'''

from collections import namedtuple, defaultdict

Entry = namedtuple('Entry', 'entity component')

# Mapping component class -> list of entries
_registry = defaultdict(list)


def add(entity, *components):
    '''Adds the component(s) to the specified entity'''

    for component in components:
        klass = component.__class__
        entry = Entry(entity, component)
        _registry[klass].append(entry)


def by_class(klass):
    '''Generator that yields all the components of a given class'''
    try:
        for entry in _registry[klass]:
            yield entry
    except KeyError:
        pass

def by_entity(entity):
    '''Generator that yields all the components of a given entity'''
    for klass, entries in _registry.items():
        for entry in entries:
            if entry.entity == entity:
                yield entry

def by_entity_and_class(entity, klass):
    '''All the components of a given entity mathing the component class'''
    try:
        for entry in _registry[klass]:
            if entry.entity == entity:
                yield entry
    except KeyError:
        pass

def single_match(*klasses):
    '''Yields lists of components from entities that have all the specified component classes'''

    if len(klasses) < 1:
        return

    entries = by_class(klasses[0])
    if len(klasses) == 1:
        for entry in entries:
            yield entry

    for entity, component in entries:
        retlist = [entity, component]
        for klass in klasses[1:]:
            for _, component in by_entity_and_class(entity, klass):
                retlist.append(component)
                break
            else:
                # klass not found, break outside
                break
        else:
            yield retlist

