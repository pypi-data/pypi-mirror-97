"""
Base functions and classes for linked/joined operations.
"""

from typing import Mapping, Callable, Union, MutableMapping, Any
import operator

EmptyMappingFactory = Union[MutableMapping, Callable[[], MutableMapping]]
BinaryOp = Callable[[Any, Any], Any]

Neutral = object()


def key_aligned_val_op(
    x: Mapping,
    y: Mapping,
    op: BinaryOp,
    dflt_val_for_x=Neutral,
    dflt_val_for_y=Neutral,
):
    """
    
    >>> from operator import add, sub, mul, truediv, and_, or_, xor
    >>> x = {'a': 8, 'b': 4}
    >>> y = {'b': 2, 'c': 1}

    If no default vals are given, only those keys that are in both mappings will be in the output.

    >>> key_aligned_val_op(x, y, add)
    {'b': 6}

    If we specify a default for ``x`` then all items of ``y`` can be used.

    >>> key_aligned_val_op(x, y, add, dflt_val_for_x=0)
    {'b': 6, 'c': 1}

    If we specify a default for ``y`` then all items of ``x`` can be used.

    >>> key_aligned_val_op(x, y, add, dflt_val_for_y=0)
    {'a': 8, 'b': 6}


    """
    result_dict = dict()
    for k, v1 in x.items():
        v2 = y.get(k, dflt_val_for_y)
        if v2 is not Neutral:
            result_dict[k] = op(v1, v2)
            # else, don't include the key
    if dflt_val_for_x is not Neutral:
        for k in set(y).difference(result_dict):
            result_dict[k] = op(dflt_val_for_x, y[k])

    return result_dict


def key_aligned_val_op_with_forced_defaults(
    x: Mapping,
    y: Mapping,
    op: BinaryOp,
    dflt_val_for_x,
    dflt_val_for_y,
    empty_mapping_factory: EmptyMappingFactory = dict,
) -> Mapping:
    """Apply an operator to the key-aligned values of two dictionaries, using specified defaults for each dictionary.

    The output's keys will be the union of the keys of the input dictionaries.

    The type of the output will be the type of that is returned by empty_mapping_factory.

    >>> from operator import add, sub, mul, truediv, and_, or_, xor
    >>> x = {'a': 8, 'b': 4}
    >>> y = {'b': 2, 'c': 1}
    >>> key_aligned_val_op_with_forced_defaults(x, y, add, 0, 0)
    {'a': 8, 'b': 6, 'c': 1}
    >>> key_aligned_val_op_with_forced_defaults(x, y, sub, 0, 0)
    {'a': 8, 'b': 2, 'c': -1}
    >>> key_aligned_val_op_with_forced_defaults(x, y, mul, 1, 1)
    {'a': 8, 'b': 8, 'c': 1}
    >>> key_aligned_val_op_with_forced_defaults(x, y, truediv, 1, 1)
    {'a': 8.0, 'b': 2.0, 'c': 1.0}
    >>> x = {'a': [8], 'b': [4]}
    >>> y = {'b': [2], 'c': [1]}
    >>> key_aligned_val_op_with_forced_defaults(x, y, add, [], [])
    {'a': [8], 'b': [4, 2], 'c': [1]}
    >>> x = {'a': True, 'b': False}
    >>> y = {'b': True, 'c': False}
    >>> key_aligned_val_op_with_forced_defaults(x, y, and_, True, True)
    {'a': True, 'b': False, 'c': False}
    >>> key_aligned_val_op_with_forced_defaults(x, y, or_, True, True)
    {'a': True, 'b': True, 'c': True}
    >>> key_aligned_val_op_with_forced_defaults(x, y, xor, True, True)
    {'a': False, 'b': True, 'c': True}

    """
    result_dict = empty_mapping_factory()
    for k, v1 in x.items():
        v2 = y.get(k, dflt_val_for_y)
        result_dict[k] = op(v1, v2)
    for k in set(y).difference(result_dict):
        result_dict[k] = op(dflt_val_for_x, y[k])

    return result_dict


def map_op_val(x: Mapping, val, op: BinaryOp, items_to_mapping=dict):
    """Apply operation op(v, val) to every value v of mapping x.

    >>> from operator import add, sub, mul, truediv
    >>> x = dict(a=2, b=3)
    >>> map_op_val(x, 2, add)
    {'a': 4, 'b': 5}
    >>> map_op_val(x, 2, sub)
    {'a': 0, 'b': 1}
    >>> map_op_val(x, 2, mul)
    {'a': 4, 'b': 6}
    >>> map_op_val(x, 2, truediv)
    {'a': 1.0, 'b': 1.5}

    """
    return items_to_mapping(((k, op(v, val)) for k, v in x.items()))


class OperableMapping(dict):
    """
    >>> d = OperableMapping({'a': 8, 'b': 4})
    >>> dd = OperableMapping(b=2, c=1)  # you can make one this way too
    >>> d + dd
    {'a': 8, 'b': 6, 'c': 1}
    >>> d - dd
    {'a': 8, 'b': 2, 'c': -1}
    >>> d * dd
    {'a': 8, 'b': 8, 'c': 1}
    >>> d / dd
    {'a': 8.0, 'b': 2.0, 'c': 1.0}

    The result of the operations are themselves DictWithOps, so you can compose several.

    >>> d * (dd + d) / d  # notice that this is equivalent to d + dd (but with numbers cast to floats)
    {'a': 8.0, 'b': 6.0, 'c': 1.0}

    """

    def __add__(self, y):
        if isinstance(y, dict):
            return key_aligned_val_op_with_forced_defaults(
                self, y, operator.__add__, 0, 0, __class__
            )
        else:
            return map_op_val(self, y, operator.__add__)

    def __sub__(self, y):
        if isinstance(y, dict):
            return key_aligned_val_op_with_forced_defaults(
                self, y, operator.__sub__, 0, 0, __class__
            )
        else:
            return map_op_val(self, y, operator.__sub__)

    def __mul__(self, y):
        if isinstance(y, dict):
            return key_aligned_val_op_with_forced_defaults(
                self, y, operator.__mul__, 1, 1, __class__
            )
        else:
            return map_op_val(self, y, operator.__mul__)

    def __truediv__(self, y):
        if isinstance(y, dict):
            return key_aligned_val_op_with_forced_defaults(
                self, y, operator.__truediv__, 1, 1, __class__
            )
        else:
            return map_op_val(self, y, operator.__truediv__)
