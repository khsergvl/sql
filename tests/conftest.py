import sqlite3
import pytest
from pathlib import Path

@pytest.fixture
def sqlite_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    schema = Path("db/schema.sql").read_text()
    cursor.executescript(schema)

    yield conn

    conn.close()