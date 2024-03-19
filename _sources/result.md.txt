# Result

Simple monadic result library for Python.

## Install

```shell
pip install git+https://github.com/wavelet-space/result.git
```

## Usage

```python
import wavelet.result as result

success: Success[int] = Success(1)
print(bool(success))
# True

failure: Failure[int] = Failure(0)
print(bool(failure))
# False

# Show enum class for error.
# Show match-case for error.
```

## Observers

- `value`
- `error`
- `value_or(default: T)`

### Monadic operations

 The monadic operations allow us to chain calls together.

- `and_then()`
- `or_else()`

## References

- <https://adambennett.dev/2020/05/the-result-monad/>
- <https://github.com/rustedpy/result>
- <https://fsharpforfunandprofit.com/posts/recipe-part2/>
- <https://jellis18.github.io/post/2021-12-13-python-exceptions-rust-go/>
- <https://www.cppstories.com/2023/monadic-optional-ops-cpp23/>
- <https://ducmanhphan.github.io/2020-12-15-monad-pattern/>
