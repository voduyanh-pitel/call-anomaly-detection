"""Text helpers that use only configured keywords."""

import re

import pandas as pd

from .keywords import DEFAULT_KEYWORDS


def _get_kw(keywords):
    return keywords if keywords is not None else DEFAULT_KEYWORDS


def clean_and_substantive_check(text, keywords=None):
    if pd.isna(text):
        return False, ""
    cleaned = str(text).strip().lower()
    if not cleaned:
        return False, cleaned
    if not re.findall(r"\w+", cleaned):
        return False, cleaned
    return True, cleaned


def classify_bargein_type(text, keywords=None):
    kw = _get_kw(keywords)
    if any(keyword in text for keyword in kw.object_keywords):
        return "object"
    if any(keyword in text for keyword in kw.confirm_keywords):
        return "confirm"
    return "other"


def is_valid_stt(event_code, keywords=None):
    return str(event_code or "").upper() not in _get_kw(keywords).invalid_codes


def is_fallback(text, keywords=None):
    lowered = str(text).lower()
    return any(keyword in lowered for keyword in _get_kw(keywords).fallback_keywords)


def is_end_phrase(text, keywords=None):
    lowered = str(text).lower()
    return any(keyword in lowered for keyword in _get_kw(keywords).end_phrase_keywords)
