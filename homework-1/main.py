"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import os
import csv

if __name__ == "__main__":
    csv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "north_data"))
    csv_files = {
        "customers": os.path.join(csv_folder, "customers_data.csv"),
        "employees": os.path.join(csv_folder, "employees_data.csv"),
        "orders": os.path.join(csv_folder, "orders_data.csv")
    }

    conn = psycopg2.connect(host='localhost', database='north', user='postgres', password='1999')
    cursor = conn.cursor()
    try:
        for table, csv_file in csv_files.items():
            with open(csv_file, "r", encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    columns = ", ".join(row.keys())
                    values = ", ".join(["%s"] * len(row))
                    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
                    cursor.execute(insert_query, list(row.values()))
                    conn.commit()
    finally:
        cursor.close()
        conn.close()