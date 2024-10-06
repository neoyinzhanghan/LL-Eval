import pandas as pd
import sqlite3

def get_path_data(case_numbers):
    conn = sqlite3.connect("/media/ssd2/clinical_text_data/Copath Database/copath.db")
    placeholders = ','.join(['?'] * len(case_numbers))
    query = f"SELECT specnum_formatted, part_description, text_data_final FROM heme_v2 WHERE specnum_formatted IN ({placeholders})"
    df = pd.read_sql_query(query, conn, params=case_numbers)
    df = df.drop_duplicates(subset='specnum_formatted', keep='first')
    df.reset_index(drop=True, inplace=True)
    conn.close()
    return df

if __name__ == '__main__':
    case_numbers = ['H19-5749']
    df = get_path_data(case_numbers)
    print(df)