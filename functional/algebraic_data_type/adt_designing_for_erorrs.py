"""Designing for errors.

Unhappy paths are requirements too!

This code implements the basic error handling example in slides 129-135 of;
    https://www.slideshare.net/ScottWlaschin/railway-oriented-programming?ref=https://fsharpforfunandprofit.com/rop/

References:
    https://www.slideshare.net/ScottWlaschin/railway-oriented-programming
    https://fsharpforfunandprofit.com/posts/exceptions/

Uses:
    https://pypi.org/project/algebraic-data-types/

"""

# %%

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from toolz import curry
from toolz.curried import pipe

from adt import Case, adt

# %%
#
# Simple types.
#


class EmailAddress(str):
    """Email Address."""


class Name(str):
    """Name."""

# %%
#
# Error Message.
#


@adt
class Error:
    """Error Message."""

    NAME_MUST_NOT_BE_BLANK: Case
    EMAIL_NUST_NOT_BE_BLANK: Case
    EMAIL_NOT_VALID: Case[EmailAddress]


def error_message(err: Error) -> str:
    """Error message."""
    return err.match(
        NAME_MUST_NOT_BE_BLANK=lambda: "Name must not be blank",
        EMAIL_NUST_NOT_BE_BLANK=lambda: "Email must not be blank",
        EMAIL_NOT_VALID=lambda email: f"Email `{email}` is not valid.")


# %%
#
# Result
#

_T = TypeVar('_T')


@adt
class Result(Generic[_T]):
    """Result."""

    SUCCESS: Case['Result']
    FAILURE: Case[Error]


def result_message(result: Result) -> str:
    """Result message."""
    return result.match(
        # Success...
        SUCCESS=lambda any: f"The result was a success...  `{any}`",
        # Failures...
        FAILURE=lambda err: f"The result was a failure... `{error_message(err)}`")  # pylint: disable=unnecessary-lambda
    # FAILURE=lambda err:  err.match(
    #     NAME_MUST_NOT_BE_BLANK=lambda: "Name must not be blank",
    #     EMAIL_NUST_NOT_BE_BLANK=lambda: "Email must not be blank",
    #     EMAIL_NOT_VALID=lambda email: f"Email `{email}` is not valid."))


@curry
def result_bind(result: Result, func: Callable) -> Result:
    """Result bind."""
    return result.match(
        SUCCESS=lambda any: func(any),  # `func(...)` returns `Result.SUCCESS` or `Result.FAILURE`
        FAILURE=lambda result: Result.FAILURE(result))


# For other functions see;
#
# Defining the core functions for Result
# https://fsharpforfunandprofit.com/posts/elevated-world-3/#defining-the-core-functions-for-result
#

def result_map(result: Result) -> Result:
    """Result map."""
    _ = result
    pass


def result_return(x: Any) -> Result:
    """Result return (lift)."""
    return Result.SUCCESS(x)


def result_apply(fresult: Result, xresult: Result) -> Result:
    """Result apply."""
    _ = fresult, xresult
    pass


# %%
#
# Test Result
#

result_message(Result.SUCCESS("Well done!"))

result_message(Result.FAILURE(Error.NAME_MUST_NOT_BE_BLANK()))

result_message(Result.FAILURE(Error.EMAIL_NUST_NOT_BE_BLANK()))

result_message(Result.FAILURE(Error.EMAIL_NOT_VALID("mickey@disney.com")))


# %%
#
# Input
#

@dataclass
class Input:
    """Input."""

    name: Name
    email: EmailAddress


def input_name_not_blank(input: Input) -> Result:
    """Name not blank."""
    if input.name == "":
        return Result.FAILURE(Error.NAME_MUST_NOT_BE_BLANK())
    else:
        return Result.SUCCESS(input)


def input_email_not_blank(input: Input) -> Result:
    """Email not blank."""
    if input.email == "":
        return Result.FAILURE(Error.EMAIL_NUST_NOT_BE_BLANK())
    else:
        return Result.SUCCESS(input)


# %%
#
# Input testing...
#

input_valid = Input(Name("Alan"), EmailAddress("alan@mail.com"))
input_blank = Input(Name(""), EmailAddress(""))

input_name_not_blank(input_valid)

input_name_not_blank(input_blank)


# %%
#
# Curry testing...
#

result_bind(Result.SUCCESS(input_valid), input_name_not_blank)
result_bind(Result.SUCCESS(input_valid))(input_name_not_blank)  # Curried.
result_bind(func=input_name_not_blank)(Result.SUCCESS(input_valid))  # Curried.

result_bind(Result.FAILURE(input_blank), input_name_not_blank)
result_bind(Result.FAILURE(input_blank))(input_name_not_blank)  # Curried.
result_bind(func=input_email_not_blank)(Result.FAILURE(input_blank))  # Curried.


# %%
#
# Pipe.
#

def result_pipe(data: Any, *funcs: list) -> Result:
    """Result pipe."""
    return pipe(result_return(data), (result_bind(func=fn) for fn in funcs))


def input_validation(input: Input):
    """Input validation."""
    return pipe(result_return(input),
                result_bind(func=input_name_not_blank),
                result_bind(func=input_email_not_blank))


# %%
#
# Pipe testing...
#

result_valid = input_validation(input_valid)
result_message(result_valid)


# %%
result_valid = input_validation(input_blank)
result_message(result_valid)


# %%
