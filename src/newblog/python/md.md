# Rust error handling in 10 lines of Python

```python
import dataclass from dataclasses
from typing import TypeVar, Generic, Union


@dataclass
class Err():
    error: str


T = TypeVar("T")


@dataclass
class Ok(Generic[T]):
    value: T


Result = Union[Ok[T], Err]
```

# references

https://jellis18.github.io/post/2021-12-13-python-exceptions-rust-go/
https://peps.python.org/pep-0636/#matching-sequences
