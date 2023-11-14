"""
This module contains all the things shared across projects.
"""

__all__ = ["flatten", "expand"]


def flatten(json: str | dict, separator="."):
    """
    Flatten a nested structure such as JSON or dictionary.

    .. seealso:: :func:`expand`

    >>> data = [{
    ...     'a': [1, 2, 3],
    ...     'b': {
    ...         'a': 1,
    ...         'b': 2,
    ...         'c': {
    ...             'a': 1,
    ...             'b': 2
    ...         }
    ...     }
    ... ]}
    >>> flatten(data)
    [{'a[0]': 1, 'a[1]': 2, 'a[2]': 3, 'b.a': 1, 'b.b': 2, 'b.c.a': 1, 'b.c.b': 2}]
    >>> flatten(data, separator="_")
    [{'a[0]': 1, 'a[1]': 2, 'a[2]': 3, 'b_a': 1, 'b_b': 2, 'b_c_a': 1, 'b_c_b': 2}]
    """


def expand(data, separator="."):
    """
    Expand a flattened structure.

    >>> data = [{'a[0]': 1, 'a[1]': 2, 'a[2]': 3, 'b_a': 1, 'b_b': 2, 'b_c_a': 1, 'b_c_b': 2}]
    >>> expand(data, separator="_")
    [{'a': [1, 2, 3], 'b': {'a': 1, 'b': 2, 'c': {'a': 1, 'b': 2}}]}
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
