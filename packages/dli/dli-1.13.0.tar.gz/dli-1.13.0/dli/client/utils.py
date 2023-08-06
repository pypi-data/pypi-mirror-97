#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
from pathlib import Path

from dli.models import AttributesDict


def makedirs(path, exist_ok=False):
    Path(path).mkdir(parents=True, exist_ok=exist_ok)

def to_camel_case(snake_str):
    split = snake_str.split('_')
    camel_case_parts = [split[0].lower()] + [s.title() for s in split[1:]]
    return ''.join(camel_case_parts)

def to_camel_cased_dict(dictionary):
    return {to_camel_case(key): value for (key, value) in dictionary.items()}

def filter_out_unknown_keys(dictionary, keys_set):
    return {k: v for (k, v) in dictionary.items() if k in keys_set}

def ensure_count_is_valid(count):
    count = int(count)
    if count <= 0:
        raise ValueError("`count` should be a positive integer")


def print_model_metadata(model: AttributesDict):
    for (k, v) in vars(model).items():
        if k == "documentation" and type(v) is str:
            val = v[0:100].replace('\n', ' ').replace('\r', '') + "..." \
                if len(v) > 100 else v
        else:
            val = v

        if not (hasattr(v, '__dict__') or k.startswith("_")):
            print(f"{k}: " + f"{val}")
