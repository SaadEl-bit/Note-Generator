"""Shared exceptions and utilities for API calls."""


class TokenLimitError(Exception):
    """Raised when a note exceeds the token limit."""
    pass

#this is an exception made class like in java