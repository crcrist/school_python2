import streamlit as st
import sqlite3
import pandas as pd

def get_inventory_data(item_id=None):
    """Get inventory data from the catalog table"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    if item_id is not None:
        query = "SELECT * FROM catalog WHERE item_id = ?"
        df = pd.read_sql_query(query, conn, params=(item_id,))
    else:
        df = pd.read_sql_query("SELECT * FROM catalog", conn)

    conn.close()
    return df
