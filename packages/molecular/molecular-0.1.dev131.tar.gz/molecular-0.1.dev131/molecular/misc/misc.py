
import numpy as np
from typelike import ArrayLike


# Assert that an array is incremental
def assert_incremental(a, increment=1):
    """
    Assert that something like an array has entries that increment by a specific value.

    Parameters
    ----------
    a : ArrayLike
        Array to check if entries increment by specific value.
    increment : int
        Increment value.

    Raises
    ------
    AssertionError
        If `a` does not have entries that increment by `increment`
    """

    assert is_incremental(a, increment=increment)


# Test if an array is incremental
def is_incremental(a, increment=1):
    return (np.diff(a) == increment).all()

