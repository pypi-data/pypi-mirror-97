import pandas as pd

# Treat Pandas/Numpy NaN, as well as strings containing only
# whitespace, as not-a-value.  Everything else is considered a value.
def is_na(value):
    return pd.isna(value) or (isinstance(value, str) and value.strip() == "")

# For convenience
def is_value(value):
    return not is_na(value)
