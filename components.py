#!/usr/bin/env python
'''
Components management

Stores all components internally, grouping components by class.
'''

from collections import namedtuple, defaultdict

Entry = namedtuple('Entry', 'entity component')

# _registry[component_class][entity] = component_instance
_registry = defaultdict(dict)


def add(entity, *components):
    '''Adds the component(s) to the specified entity'''

    for component in components:
        klass = component.__class__
        _registry[klass][entity] = component


def by_class(klass):
    '''Generator that yields all the components of a given class'''
    try:
        for entity in _registry[klass]:
            yield Entry(entity, _registry[klass][entity])
    except KeyError:
        pass


def by_entity(entity):
    '''Generator that yields all the components of a given entity'''
    for klass in _registry:
        if entity in _registry[klass]:
            return Entry(entity, _registry[klass][entity])


def by_entity_and_class(entity, klass):
    '''Component of a given entity mathing the component class, or raises KeyError'''
    return _registry[klass][entity]


def single_match(*klasses):
    '''Yields [entity, components...] from all matching entities'''

    if len(klasses) < 1:
        return

    entries = by_class(klasses[0])
    if len(klasses) == 1:
        for entry in entries:
            yield entry

    for entity, component in entries:
        retlist = [entity, component]
        for klass in klasses[1:]:
            try:
                retlist.append(by_entity_and_class(entity, klass))
            except KeyError:
                break
        else:
            # All found
            yield retlist

