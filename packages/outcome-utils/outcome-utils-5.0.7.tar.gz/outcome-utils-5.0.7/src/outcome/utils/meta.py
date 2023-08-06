"""Helpers to manipulate class arguments."""

from inspect import getclasstree, getfullargspec
from typing import Iterable, List, Set, Union

__all__ = ['get_init_args']


def get_all_subclasses(cls: type) -> List[type]:
    all_subclasses: List[type] = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def get_init_args(cls: type) -> Set[str]:
    # Get the list of classes that the original_field herits from
    original_tree_class = getclasstree([cls], unique=True)
    list_classes = _flatten_list_of_types(original_tree_class)

    # From these classes, get the list of args we can use when creating the instances
    list_args = set()
    for cl in list_classes:
        # `getfullargspec` allows to get the arguments of a specific function - here we use
        # it on the __init__ function that initializes instances of a class
        list_args.update(getfullargspec(cl.__init__).args)  # noqa: WPS609

    # Remove special args
    list_args.remove('self')  # Represents the instance of the class - can't be used to create a new instance
    return list_args


NestedClasses = Iterable[Union[type, 'NestedClasses']]


def _flatten_list_of_types(list_to_flatten: NestedClasses) -> Set[type]:
    """Flatten a list of types with nested lists and tuples.

    When using the `inspect` module `getclasstree`, it returns a list of types in a hierarchical order.
    We only need the list of unique types, without any nesting.

    Examples:
    list_to_flatten = [
        (<class 'playhouse.postgres_ext.IndexedFieldMixin'>, (<class 'object'>,)),
        [
            (
                <class 'playhouse.postgres_ext.BinaryJSONField'>,
                (
                    <class 'playhouse.postgres_ext.IndexedFieldMixin'>, <class 'playhouse.postgres_ext.JSONField'>
                )
            )
        ]
    ]
    flattened_list = [
        <class 'playhouse.postgres_ext.IndexedFieldMixin'>,
        <class 'object'>,
        <class 'playhouse.postgres_ext.JSONField'>,
        <class 'playhouse.postgres_ext.BinaryJSONField'>
    ]

    Args:
        list_to_flatten (NestedClasses): The list to be flattened

    Returns:
        Set[type]: The set of classes.
    """
    ancestor_set = set()
    for el in list_to_flatten:
        if isinstance(el, type):
            # If the element is a type, then we want to keep it.
            ancestor_set.add(el)
        else:
            # But if we can iterate on it (list, tuple, ..), then we need to go deeper to get the types.
            sublist = _flatten_list_of_types(el)
            ancestor_set.update(sublist)
    return ancestor_set
