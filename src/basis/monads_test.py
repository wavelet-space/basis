"""
Test not only assert the correct behaviour but also serves as examples.
"""

from monarch import Success, Failure

# Result monad tests

def test_that_success_result_contains_value():
    result = Success(1)
    assert result.value == 1


def test_that_failure_result_contains_error_message():
    """Sometimes a simple text can be suficient.."""
    result = Failure("message")
    assert result.error == "message"


def test_that_failure_result_contains_exception_class():
    """
    Test that we can catch single exceptions.
    """
    result = Failure(Exception("message"))
    assert isinstance(result.error, Exception) 


def test_that_failure_result_contains_exception_classes():
    """
    Test that we can catch multiple exceptions.
    """
    result = Failure([Exception("message1"), Exception("message2")])

    error1, error2 = result.error
    
    assert isinstance(error1, Exception) and str(error1) == "message1" 
    assert isinstance(error2, Exception) and str(error2) == "message2"


def test_pattern_matching_on_success_result():
    result = Success(1)
    match result:
        case Success():
            assert True
        case _:
            assert False    


def test_pattern_matching_on_failure_result():
    result = Failure(1)
    match result:
        case Failure():
            assert True
        case _:
            assert False   


def test_result_functor_map():
    result = Success(1)
    mapped = result.map(lambda x: x + 1)
    assert mapped.value == 2

## Option monad tests
