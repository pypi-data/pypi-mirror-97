"""
Batch a list of features output by describers.transform method
"""
from typing import Any, List, Callable, Optional, Union

import numpy as np
import pandas as pd


def pandas_concat(features: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatenate a list of pandas dataframe into a single one
    Args:
        features (list): list of pandas dataframe

    Returns: concatenated pandas dataframe

    """
    concatenated = pd.concat(features, keys=range(len(features)), names=["input_index", None])
    return concatenated


def stack_first_dim(features: List[np.ndarray]) -> np.ndarray:
    """
    Stack the first dimension. If the original features
    are a list of nxm array, the stacked features will be lxnxm,
    where l is the number of entries in the list
    Args:
        features (list): list of numpy array features

    Returns: stacked features

    """
    return np.stack(features)


def stack_padded(features: List[np.ndarray]) -> np.ndarray:
    """
    Stack the first dimension. If the original features
    are a list of nxm array, the stacked features will be lxnxm,
    where l is the number of entries in the list
    Args:
        features (list): list of numpy array features

    Returns: stacked features

    """
    feature_dims = np.array([i.shape[0] for i in features])
    n_data = len(feature_dims)
    max_feature_dims = np.max(feature_dims)
    res = np.zeros((n_data, max_feature_dims))
    index1 = np.tile(np.arange(max_feature_dims)[None, :], (n_data, 1))
    masks = index1 < feature_dims[:, None]
    res[masks] = np.concatenate(features)
    return res


def no_action(features: List[Any]) -> List[Any]:
    """
    return original feature lists

    """
    return features


AVAILABLE_FB_METHODS = {
    "pandas_concat": pandas_concat,
    "stack_first_dim": stack_first_dim,
    "stack_padded": stack_padded,
    "no_action": no_action,
}


def get_feature_batch(fb_name: Optional[Union[str, Callable]] = None) -> Callable:
    """
    Providing a feature batch name, returning the function callable
    Args:
        fb_name (str): name of the feature batch function
    Returns: callable feature batch function
    """
    if fb_name is None:
        return no_action

    if isinstance(fb_name, str):
        try:
            return AVAILABLE_FB_METHODS[fb_name]
        except KeyError:
            raise KeyError(
                "Feature batch method not supported!" "Available ones are %s" % str(AVAILABLE_FB_METHODS.keys())
            )
    else:
        return fb_name
