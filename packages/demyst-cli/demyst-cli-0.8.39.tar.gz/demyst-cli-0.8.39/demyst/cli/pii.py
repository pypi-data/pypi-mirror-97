import unittest
import pandas as pd
import re

from demyst.common import PII_REGEX, is_value

# Mask columns in dataframe that match PII_REGEX.  If columns
# parameter is specified, mask only those columns, ignoring PII_REGEX.
def mask_pii(df, columns=[]):
    columns = __find_columns_to_mask(df, columns)
    for col in columns:
        df[col] = __mask_column(df[col])
    return df

# Returns names of columns that will be masked.
def mask_columns(df):
    return __find_columns_to_mask(df, [])

def __find_columns_to_mask(df, columns):
    if len(columns) > 0:
        return columns
    else:
        return [col for col in list(df) if re.search(PII_REGEX, col)]

def __mask_column(series):
    def mask(value):
        if is_value(value):
            return "Masked"
        else:
            return value
    return series.map(mask)
