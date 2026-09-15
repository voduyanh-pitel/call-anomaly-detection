"""Editable keyword groups for the metrics analyzer."""

from copy import deepcopy
from dataclasses import dataclass, field

REQUIRED_COLUMNS = {"call_id", "ts", "turn", "event_name", "event_detail", "event_code"}

@dataclass
class KeywordConfig:
    object_keywords: list = field(default_factory=lambda: [
        "không phải", "không đúng", "chưa đúng", "sai rồi", "nhầm rồi", "em nhầm",
        "không chính xác", "ý tôi là", "ý chị là", "ý anh là", "ý em là",
        "hình như", "khoan", "khoan đã", "đợi đã", "từ từ",
    ])
    confirm_keywords: list = field(default_factory=lambda: [
        "đúng rồi", "chính xác", "phải rồi", "đồng ý", "được rồi", "hiểu rồi",
        "biết rồi", "ừ đúng", "vâng đúng", "ok em",
    ])
    complain_keywords: list = field(default_factory=lambda: [
        "tôi nói rồi", "vừa bảo xong", "nãy giờ", "đã nói",
    ])
    invalid_codes: set = field(default_factory=lambda: {"ERROR", "RETRY_1", "RETRY_2", "RETRY_3"})

    def __post_init__(self):
        for group in self.keyword_groups:
            values = getattr(self, group)
            normalized = [self._normalize(value) for value in values]
            setattr(self, group, list(dict.fromkeys(normalized)))
        self.invalid_codes = {str(value).upper() for value in self.invalid_codes}
 
    @property
    def keyword_groups(self):
        return (
            "object_keywords", "confirm_keywords", "complain_keywords",
        )

    @staticmethod
    def _normalize(value):
        return str(value).strip().lower()

    def add(self, group, keyword):
        self._check_group(group)
        normalized = self._normalize(keyword)
        if normalized not in getattr(self, group):
            getattr(self, group).append(normalized)

    def remove(self, group, keyword):
        self._check_group(group)
        normalized = self._normalize(keyword)
        setattr(self, group, [value for value in getattr(self, group) if value != normalized])

    def add_multiple(self, group, keywords):
        for keyword in keywords:
            self.add(group, keyword)

    def remove_multiple(self, group, keywords):
        for keyword in keywords:
            self.remove(group, keyword)

    def add_object_keyword(self, keyword):
        self.add("object_keywords", keyword)

    def remove_object_keyword(self, keyword):
        self.remove("object_keywords", keyword)

    def add_complain_keyword(self, keyword):
        self.add("complain_keywords", keyword)

    def remove_complain_keyword(self, keyword):
        self.remove("complain_keywords", keyword)

    def copy(self):
        return deepcopy(self)

    def _check_group(self, group):
        if group not in self.keyword_groups:
            raise ValueError(f"unknown keyword group: {group}")


DEFAULT_KEYWORDS = KeywordConfig()