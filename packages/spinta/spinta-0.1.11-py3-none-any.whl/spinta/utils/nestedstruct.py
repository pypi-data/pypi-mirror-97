from typing import List

import types
import itertools


def flatten(value, sep='.'):
    value, lists = _flatten(value, sep)

    if value is None:
        for k, vals in lists:
            for v in vals:
                yield from flatten(v, sep)

    elif lists:
        keys, lists = zip(*lists)
        for vals in itertools.product(*lists):
            val = {
                sep.join(k): v
                for k, v in zip(keys, vals)
            }
            val.update(value)
            yield from flatten(val, sep)

    else:
        yield value


def _flatten(value, sep, key=()):
    if isinstance(value, dict):
        data = {}
        lists = []
        for k, v in value.items():
            v, more = _flatten(v, sep, key + (k,))
            data.update(v or {})
            lists += more
        return data, lists

    elif isinstance(value, (
        list,
        types.GeneratorType,
        itertools.groupby,
        # _grouper is type of `g` in `k, g = next(itertools.groupby([1, 1]))`
        itertools._grouper,
        itertools.chain,
    )):
        if value:
            return None, [(key, value)]
        else:
            return None, []

    else:
        return {sep.join(key): value}, []


def build_select_tree(select: List[str]):
    tree = {}
    for name in select:
        split = name, None
        while len(split) == 2:
            name, node = split
            if name not in tree:
                tree[name] = set()
            if node:
                tree[name].add(node)
            split = name.rsplit('.', 1)
    return tree
