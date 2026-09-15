"""Keyword-only call metrics."""

from .analyzer import analyze_call
from .keywords import DEFAULT_KEYWORDS, KeywordConfig
__version__ = "3.0.0"

__all__ = [
    "analyze_call",
    "KeywordConfig",
    "DEFAULT_KEYWORDS",
]
