import inspect
from typing import Any

from langsmith.run_helpers import _get_inputs


def test__get_inputs_with_no_args() -> None:
    def foo() -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature)
    assert inputs == {}


def test__get_inputs_with_args() -> None:
    def foo(a: int, b: int, c: int) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, 2, 3)
    assert inputs == {"a": 1, "b": 2, "c": 3}


def test__get_inputs_with_defaults() -> None:
    def foo(a: int, b: int, c: int = 3) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, 2)
    assert inputs == {"a": 1, "b": 2, "c": 3}


def test__get_inputs_with_var_args() -> None:
    # Mis-named args as kwargs to check that it's mapped correctly
    def foo(a: int, b: int, *kwargs: Any) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, 2, 3, 4)
    assert inputs == {"a": 1, "b": 2, "kwargs": (3, 4)}


def test__get_inputs_with_var_kwargs() -> None:
    def foo(a: int, b: int, **kwargs: Any) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, 2, c=3, d=4)
    assert inputs == {"a": 1, "b": 2, "c": 3, "d": 4}


def test__get_inputs_with_var_kwargs_and_varargs() -> None:
    def foo(a: int, b: int, *args: Any, **kwargs: Any) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, 2, 3, 4, c=5, d=6)
    assert inputs == {"a": 1, "b": 2, "args": (3, 4), "c": 5, "d": 6}


def test__get_inputs_with_class_method() -> None:
    class Foo:
        @classmethod
        def bar(cls, a: int, b: int) -> None:
            pass

    signature = inspect.signature(Foo.bar)
    inputs = _get_inputs(signature, 1, 2)
    assert inputs == {"a": 1, "b": 2}


def test__get_inputs_with_static_method() -> None:
    class Foo:
        @staticmethod
        def bar(a: int, b: int) -> None:
            pass

    signature = inspect.signature(Foo.bar)
    inputs = _get_inputs(signature, 1, 2)
    assert inputs == {"a": 1, "b": 2}


def test__get_inputs_with_self() -> None:
    class Foo:
        def bar(self, a: int, b: int) -> None:
            pass

    signature = inspect.signature(Foo.bar)
    inputs = _get_inputs(signature, Foo(), 1, 2)
    assert inputs == {"a": 1, "b": 2}


def test__get_inputs_with_kwargs_and_var_kwargs() -> None:
    def foo(a: int, b: int, **kwargs: Any) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, 2, c=3, **{"d": 4})
    assert inputs == {"a": 1, "b": 2, "c": 3, "d": 4}


def test__get_inputs_with_var_kwargs_and_other_kwargs() -> None:
    def foo(a: int, b: int, **kwargs: Any) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, 2, c=3, other_kwargs={"d": 4})
    assert inputs == {"a": 1, "b": 2, "c": 3, "other_kwargs": {"d": 4}}


def test__get_inputs_with_keyword_only_args() -> None:
    def foo(a: int, *, b: int, c: int) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, b=2, c=3)
    assert inputs == {"a": 1, "b": 2, "c": 3}


def test__get_inputs_with_keyword_only_args_and_defaults() -> None:
    def foo(a: int, *, b: int = 2, c: int = 3) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1)
    assert inputs == {"a": 1, "b": 2, "c": 3}


def test__get_inputs_misnamed_and_required_keyword_only_args() -> None:
    def foo(kwargs: int, *, b: int, c: int, **some_other_kwargs: Any) -> None:
        pass

    signature = inspect.signature(foo)
    inputs = _get_inputs(signature, 1, b=2, c=3, d=4, e=5, other_kwargs={"f": 6})
    assert inputs == {
        "kwargs": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "other_kwargs": {"f": 6},
    }
