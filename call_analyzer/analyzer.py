"""Keyword-based metrics for one voice-bot call."""

import re
import warnings
import pandas as pd

from .keywords import DEFAULT_KEYWORDS, REQUIRED_COLUMNS
from .text import (
    classify_bargein_type,
    clean_and_substantive_check,
    is_valid_stt,
)


def _prepare_logs(logs):
    if logs is None:
        raise ValueError("logs must not be None")
    group = pd.DataFrame(logs)
    if group.empty:
        raise ValueError("logs is empty - nothing to analyze")
    missing = REQUIRED_COLUMNS - set(group.columns)
    if missing:
        raise ValueError(f"missing required columns in log: {sorted(missing)}")
    call_ids = group["call_id"].dropna().astype(str).unique()
    if len(call_ids) > 1:
        raise ValueError(f"logs must contain a single call_id, got {len(call_ids)}: {sorted(call_ids)[:5]}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed_ts = pd.to_datetime(group["ts"], errors="coerce")
    sort_key = parsed_ts if parsed_ts.notna().all() else group["ts"]
    group = group.assign(_ts=sort_key).sort_values("_ts", kind="stable").drop(columns="_ts").reset_index(drop=True)
    call_id = str(call_ids[0]) if len(call_ids) else None
    return call_id, group


def _normalize_for_repeat(text):
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def analyze_call(logs, keywords=None):
    """Return exactly the five supported metrics."""
    kw = keywords if keywords is not None else DEFAULT_KEYWORDS
    call_id, group = _prepare_logs(logs)

    stt_sentences = []
    bargein_object = 0
    bargein_confirm = 0
    cust_objection = 0
    complain_already_answered = 0

    for index, row in group.iterrows():
        event_name = str(row.get("event_name", ""))
        event_code = row.get("event_code", "")
        event_detail = row.get("event_detail", "")

        if event_name == "STT" and is_valid_stt(event_code, kw):
            is_substantive, cleaned = clean_and_substantive_check(event_detail, kw)
            if is_substantive:
                stt_sentences.append(_normalize_for_repeat(cleaned))
                if any(keyword in cleaned for keyword in kw.object_keywords):
                    cust_objection += 1
                if any(keyword in cleaned for keyword in kw.complain_keywords):
                    complain_already_answered += 1
        elif event_name == "Barge-in":
            following_stt = group.iloc[index + 1:]
            following_stt = following_stt[following_stt["event_name"] == "STT"]
            for _, stt_row in following_stt.iterrows():
                if not is_valid_stt(stt_row.get("event_code", ""), kw):
                    continue
                is_substantive, cleaned = clean_and_substantive_check(stt_row.get("event_detail", ""), kw)
                if not is_substantive:
                    continue
                bargein_type = classify_bargein_type(cleaned, kw)
                if bargein_type == "object":
                    bargein_object += 1
                elif bargein_type == "confirm":
                    bargein_confirm += 1
                break


    return {
        "call_id": call_id,
        "cust_objection": cust_objection,
        "complain_already_answered": complain_already_answered,
        "bargein_confirm": bargein_confirm,
        "bargein_object": bargein_object,
    }
