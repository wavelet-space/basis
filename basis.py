


def nested():
    """
    Make flat structure nested again. 
    """

def flatten(json: str | dict):
    """
    Flatten a nested structure such as JSON or dictionary.
    
    >>> data = {
    ...     'a': [1, 2, 3]
    ... } 
    
    expect a_0 a_1 a_2

    >>> data = {
    ...     'a': [1, 2, 3],
    ...     'b': {
    ...         'a': 1,
    ...         'b': 2,
    ...         'c': {
    ...             'a': 1,
    ...             'b': 2,
    ...         }
    ...     }
    ... }   
    
    expected flatten a_0, a_1, a_2, b_a, b_b, b_c_a,, b_c_b,  
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
