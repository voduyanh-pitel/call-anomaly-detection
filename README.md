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

Ket qua tra ve 3 metric cho mot cuoc goi:

```
{'call_id': '1c7792ee-313a-4411-962c-b0f4914df8a6',
 'cust_objection': 2,
 'complain_already_answered': 0,
 'bargein_object': 2}
```

## Su dung - goi ham tu code

```python
from call_analyzer import analyze_call

metrics = analyze_call(logs)
```

Dau vao la log cua mot cuoc goi dang `pandas.DataFrame` hoac `list[dict]`,
gom `call_id`, `ts`, `turn`, `event_name`, `event_detail`, `event_code`.

Ket qua chi gom 3 metric:

`call_id`, `cust_objection`, `complain_already_answered`, `bargein_object`.
