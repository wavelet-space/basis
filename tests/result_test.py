import basis.result as result


def test_success_result_evaluates_to_true():
    success = result.Success("some value")
    assert bool(success)


def test_failure_result__evaluates_to_false():
    failure = result.Failure("some error")
    assert not bool(failure)
