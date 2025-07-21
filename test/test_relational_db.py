import sqlite3
import pytest

DB_PATH = "db/bdnb.sqlite3"
TABLE_NAME = "batiment_groupe"  # adapte selon ta base

@pytest.fixture(scope="module")
def db_conn():
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()

def test_tables_exist(db_conn):
    
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    assert TABLE_NAME in tables, f"La table '{TABLE_NAME}' doit exister"

def test_list_tables(db_conn):
    
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables dans la base :")
    for t in tables:
        print(f" - {t}")
    assert len(tables) > 0, "Aucune table trouvée dans la base"


def test_list_columns(db_conn):
    cursor = db_conn.cursor()
    cursor.execute(f"PRAGMA table_info({TABLE_NAME});")
    columns_info = cursor.fetchall()
    column_names = [col[1] for col in columns_info]
    
    print(f"Colonnes dans la table '{TABLE_NAME}':")
    for name in column_names:
        print(f" - {name}")
    
    assert len(column_names) > 0, f"Aucune colonne trouvée dans la table {TABLE_NAME}"
