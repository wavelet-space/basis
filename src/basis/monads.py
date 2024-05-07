"""
Simple monadic architecture for Python.
Monads and Monadic Pipelines in Python.

Some notes inspired by Haskell documentation:

Monad is a triple M := (m, return, >>=) where

- m is a type constructor
- return is a function `return :: a -> m a`
- >>= is an operator called bind `>>= :: m a -> (a -> m b) -> m b`

Features
- Functor (Mappable)
- Applicative (Flatten + Mappable)

Monad types
- Option aka Maybe
- Result aka Either

"""

from abc import abstractmethod
from typing import Self
from typing import Generic, Protocol, Any, T, TypeVar, Callable, TypeAlias, runtime_checkable, final
from typing import TypeVar, Protocol, Callable
# import typing_extensions

from dataclasses import dataclass


T = TypeVar('T', covariant=True)
U = TypeVar('U', covariant=False)


# A function with one argument. See https://aplwiki.com/wiki/Monadic_function
Function1: TypeAlias = Callable[[T], U] 


@runtime_checkable
class Functor(Protocol[T, U]):
    """
    The functor is used for values that can be mapped over.
    """

    def map(self: Self, callable: Callable[[T], U]) -> U:
        """
        Map a function over the wrapped value.
        """


# @runtime_checkable
class Applicative(Functor[T, U]):
    """
    The applicative is an extension of functor.

    """
    
    def apply(self: Self, callable: Callable[[T], U]) -> Self:
        """
        Jak to funguje:
        Mějme funktor `F(T)` a funkci `f(T) -> U`. Potom metoda apply 
        vezme hodnotu z funktoru F a aplikuje na ní funkci f a zabalí ji zpět do funktoru, který vrací.

        Metoda se též nazývaná **`fmap`** s operátorovým aliasem `<*>`.
        """


class Monadic(Protocol, Generic[T]):
    
    @property
    def value(self) -> T:
        """
        Get the wrapped value.
        """
    
    def bind(self, callable: Callable) -> Self:
        """
        Apply function to the value.
        """

    def __shift__(self, callable: Callable) -> Self:
        ...
        

@dataclass(frozen=True, slots=True)
class Monad(Generic[T, U]):
    
    value: T
    
    def bind(self ,callable: Function1) -> Self:
        """
        Apply monadic function to the value.
        """
        return type(self)(callable(self.value))

    def __call__(self, callable: Function1) -> Self:
        return self.bind(callable=callable)

    def __or__(self, some: Self | Callable) -> Self:
        """
        A :py:meth:`bind` method operator alias.
        """
        return self.bind(some)
    
    def __shift__(self, some: Self | Callable) -> Self:
        """
        A :py:meth:`bind` method operator alias.
        """
        return self.bind(some)
    
    def __ror__(self,  some: Self | Callable) -> Self:
        return self | some


class Option(Generic[T, U]):
    """
    This monad, also called Maybe, is used for possibly missing values.
    """

    # Functor methods

    # Applicative methods

    # Mona methods


@final
@dataclass(frozen=True, slots=True)
class Nothing(Option[T, U]):
    ...


@final
@dataclass(frozen=True, slots=True)
class Something(Option[T, U]):
    value: T


class Result(Generic[T, U]):
    """
    This monad, also called Either, wraps a value of operation which can fail.

    The :py:class:`Result` subclasses (variants) are :py:class:`Success` and :py:class:`Failure`.

    """
    # Functor methods

    def map(self, function: Callable[[T], U]) -> U:
        # I'm not OK with this string-typed solution, but it works.
        match type(self).__name__: 
            case 'Success':
                return type(self)(function(self.value))
            case 'Failure':
                return
            case _:
                raise TypeError("Only `Success` or `Failure` is allowed!") 
            
    # Applicative methods
    # def flat_map

    # Monad methods
 
    
@final
@dataclass(frozen=True, slots=True)
class Success(Result[T, U]):
    value: T




@final
@dataclass(frozen=True, slots=True)
class Failure(Result[T, U]):
    error: U


if __name__ == "__main__":
    # Using the constructor is the same (and more idiomatic) then defining the `unit` factory class method.
    # m2 = Monad(1)      
    # m1 = Monad(2)

    # print(m1, m2)

    # from operator import neg
    
    # print( m1.bind(neg) )
    # print( m1 | neg)
    # print( neg | m1)
    # print(neg | m1)

    # Maybe monad
    # some = Maybe.some(1)
    # none = Maybe.none(2)

    # print(some.empty)
    # print(none.empty)

    # TODO: Test monad laws
    # 1. The *right unit law*
    # 2. The *left unit law*
    # 3. The *associativity law*

    # Result

    # a: Result[int, str] = Success[int, str](1)
    a = Success[int, str](1)

    # b: Result[int, str] = Failure[int, str](Exception("message"))
    b = Failure[int, str](Exception("message"))

    x = a
    match x:
        case Success():
            print(x)
        case Failure():
            print(x)
