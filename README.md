# call_analyzer

Thu vien va script phan tich log voice-bot bang keyword. Ket qua chi gom cac
chi so, khong co model, embedding, similarity hoac rule canh bao.

## Cau truc du an

```
call_analyzer/
    analyzer.py    ham analyze_call - tinh 5 metric cho mot cuoc goi
    keywords.py    lop KeywordConfig - dan sach keyword dieu chinh
    text.py        ham xu ly van ban (kiem tra STT, phan loai barge-in, ...)
main.py            doc log tu SQL (SQLite) va chay analyze_call
Book1.csv          file CSV goc dung lam nguon du lieu mo phong
```

## Su dung - chay truc tiep

`main.py` doc log tu SQL. No load file `Book1.csv` vao mot database SQLite
in-memory roi thi lai bang lenh `SELECT * FROM calls`, sau do cung cap ket
qua cho `analyze_call`:

```bash
python main.py
```

Ket qua tra ve 5 metric cho mot cuoc goi, moi metric di kem danh sach turn:

```
{'call_id': '...',
 'cust_objection': 2,
 'cust_objection_turns': [...],
 'complain_already_answered': 0,
 'complain_already_answered_turns': [...],
 'bargein_confirm': 1,
 'bargein_confirm_turns': [...],
 'bargein_object': 2,
 'bargein_object_turns': [...]}
```

## Su dung - goi ham tu code

```python
from call_analyzer import analyze_call

metrics = analyze_call(logs)
```

Dau vao la log cua mot cuoc goi dang `pandas.DataFrame` hoac `list[dict]`,
gom `call_id`, `ts`, `turn`, `event_name`, `event_detail`, `event_code`.

Ket qua gom 5 metric, moi metric di kem danh sach turn:

`call_id`, `cust_objection`, `cust_objection_turns`, `complain_already_answered`, `complain_already_answered_turns`, `bargein_confirm`, `bargein_confirm_turns`, `bargein_object`, `bargein_object_turns`.
