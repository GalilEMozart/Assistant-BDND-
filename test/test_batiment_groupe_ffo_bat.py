import sqlite3
import pytest

DB_PATH = "db/bdnb.sqlite3"
TABLE_NAME = "batiment_groupe_ffo_bat"  # adapte selon ta base
EXPECTED_COLUMN_NUMBER = 8

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


def test_colonne_number(db_conn):
    
    cursor = db_conn.cursor()
    cursor.execute(f"PRAGMA table_info({TABLE_NAME});")
    columns_info = cursor.fetchall()
    nb_colonnes = len(columns_info)
      
    print(f"Nombre de colonnes dans la table '{TABLE_NAME}': {nb_colonnes}")
    assert nb_colonnes == EXPECTED_COLUMN_NUMBER, f"Attendu {EXPECTED_COLUMN_NUMBER} colonnes, trouvé {nb_colonnes}"
