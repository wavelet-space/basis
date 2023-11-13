def flatten(json: str | dict):
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
    ...             'b': 2,
    ...         }
    ...     }
    ... ]}
    >>> flatten(data)
    aa_0, a_1, a_2, b_a, b_b, b_c_a, b_c_b,
    """


def expand():
    """
    Expand a flattened structure.

    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
