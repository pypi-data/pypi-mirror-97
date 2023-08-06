"""
mem_reduce
===========
A package for reducing memory usage while working with python dataframe. 
"""

import numpy as np
import pandas as pd

def reduce_mem_usage(df, verbose=True):
    """Reduces the memory usage of a Pandas DataFrame and returns it. 
    
    Python uses pass by reference here. As a result the change of the input 
    Pandas dataframe is permanent and the function returns a dataframe reduced
    in size

    Parameters
    ----------
    df : Pandas DataFrame
        Pandas DataFrame
    verbose : Boolean
        When verbose is "True", the function prints a string stating the
        reduction of the data
        (Default value = True)

    Returns
    -------
    df : Pandas DataFrame
        Returns a Pandas DataFrame that is reduced in size. If verbose is "True" 

    """
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(
            end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


def mem_usage(pandas_obj):
    """Calculates the memory used by a pandas dataframe

    Parameters
    ----------
    pandas_obj : Pandas DataFrame or Series
        A pandas DataFrame or Series can be inputed as parameter. 
        

    Returns
    -------
    usage_mb : String
        A string that states the memory usage. 

    """
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2  # convert bytes to megabytes
    usage_mb = "{:03.2f} MB".format(usage_mb)
    return usage_mb

# We’ll write a loop to iterate over each object column,
# check if the number of unique values is more than 50%,
# and if so, convert it to the category atype.


def reduce_by_category_type(df):
    """

    Parameters
    ----------
    df :
        

    Returns
    -------

    """
    converted_obj = pd.DataFrame()
    for col in df.columns:
        num_unique_values = len(df[col].unique())
        num_total_values = len(df[col])
        if num_unique_values / num_total_values < 0.5 and df[col].dtype == 'object':
            converted_obj.loc[:, col] = df[col].astype('category')
        else:
            converted_obj.loc[:, col] = df[col]
    return converted_obj


def missing_percentage(df):
    """Takes a DataFrame(df) as input and calculates two column missing_count and missing_percentage

    Parameters
    ----------
    df : Pandas DataFrame
        Takes in a dataframe and counts the missing values. 

    Returns
    -------
    df : Pandas DataFrame
        Returns a dataframe with two columns "missing_count" and "missing_percentage"

    """
    # the two following line may seem complicated but its actually very simple.
    total = df.isnull().sum().sort_values(ascending=False)
    total = total[total > 0]
    percent = total/len(df)
    return pd.concat([total, percent], axis=1, keys=['missing_count', 'missing_percentage'])
