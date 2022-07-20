from math import log2
from typing import Iterable
import numpy as np
import json
from string import ascii_lowercase
import itertools


def dedupe_preserving_order(list_of_items):
    return list(dict.fromkeys(list_of_items))


def escape_columns(cols):
    return [c.name(escape=True) for c in cols]


def prob_to_bayes_factor(prob):
    return prob / (1 - prob)


def prob_to_match_weight(prob):
    return log2(prob_to_bayes_factor(prob))


def match_weight_to_bayes_factor(weight):
    return 2**weight


def bayes_factor_to_prob(bf):
    return bf / (1 + bf)


def interpolate(start, end, num_elements):
    steps = num_elements - 1
    step = (end - start) / steps
    vals = [start + (i * step) for i in range(0, num_elements)]
    return vals


def normalise(vals):
    return [v / sum(vals) for v in vals]


def ensure_is_iterable(a):
    return a if isinstance(a, Iterable) else [a]


def ensure_is_list(a):
    return a if isinstance(a, list) else [a]


def join_list_with_commas_final_and(lst):
    if len(lst) == 1:
        return lst[0]
    return ", ".join(lst[:-1]) + " and " + lst[-1]


class NumpyEncoder(json.JSONEncoder):
    """
    Used to correctly encode numpy columns within a pd dataframe
    when dumping it to json. Without this, json.dumps errors if
    given an a column of class int32, int64 or np.array.

    Thanks to:
    https://github.com/mpld3/mpld3/issues/434#issuecomment-340255689
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def all_letter_combos(n):
    """a,b,....,z,aa,ab,...,aaa"""

    combos = []
    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            combos.append("".join(s))
            if len(combos) >= n:
                return combos


def calculate_cartesian(df_rows):
    """
    Calculates the cartesian product for the input df(s).
    """
    n = df_rows
    numerator = n * (n - 1)
    return numerator / 2


def calculate_reduction_ratio(N, cartesian):
    """
    Args:
        N (int): The number of record pairs generated by a
            blocking rule.
        cartesian (int): The cartesian product of your input
            dataframe(s).

    Generates the reduction ratio. This represents the % reduction
    in the comparison space as a result of using your given blocking
    rule. This is a measure of how much the Blocking Rule reduces
    the total search space.
    """
    return 1 - (N / cartesian)
