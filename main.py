import sqlite3
import pandas as pd
from call_analyzer import analyze_call

def main():
    with sqlite3.connect(":memory:") as conn:
        pd.read_csv("Book1.csv", encoding="utf-8-sig").to_sql("calls", conn, index=False, if_exists="replace")
        dataframe = pd.read_sql("SELECT * FROM calls", conn)
    
    print(analyze_call(dataframe))

if __name__ == "__main__":
    main()