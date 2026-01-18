import sqlite3
import pytest
from pathlib import Path

@pytest.fixture
def sqlite_db():
    source_db = Path("05_src/sql/farmersmarket.db")
    # Create in-memory DB
    conn = sqlite3.connect(":memory:")

    # Load schema.db into memory
    disk_db = sqlite3.connect(source_db)
    disk_db.backup(conn)
    disk_db.close()

    yield conn
    conn.close()