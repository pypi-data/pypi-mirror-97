import pandas as pd

def flatten_data(json_dict, sep="."):
    results = []
    __append_dict(json_dict, results, sep, "")
    return pd.DataFrame(results)

def __append_dict(object, results, sep, prefix):
    for key, value in object.items():
        __append(__maybe_prefix(prefix, sep, key), value, results, sep)

def __append_array(values, results, sep, prefix):
    for i, value in enumerate(values):
        __append("{}[{}]".format(prefix, i), value, results, sep)

def __append(key, value, results, sep):
    if isinstance(value, dict):
        __append_dict(value, results, sep, key)
    elif isinstance(value, list):
        __append_array(value, results, sep, key)
    else:
        results.append(__make_row(key, value))

def __maybe_prefix(prefix, sep, key):
    if len(prefix) > 0:
        return prefix + sep + key
    else:
        return key

def __make_row(key, value):
    return { "key": key, "value": str(value) }
