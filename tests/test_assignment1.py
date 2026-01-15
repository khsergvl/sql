from pathlib import Path
import sqlite3

def run_student_sql(conn, sql_file):
    sql = Path(sql_file).read_text()
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def test_assignment1_returns_rows(sqlite_db):
    """
    Description:
    Student must return all users older than 25.
    Expected columns: name, age
    """
    rows = run_student_sql(sqlite_db, "sql/assignment1.sql")

    # Example asserts (you write these)
    assert len(rows) > 0, "Query returned no rows"

    for name, age in rows:
        assert age > 25, f"User {name} is not older than 25"


def test_assignment1_expected_users(sqlite_db):
    """
    Description:
    Only Alice and Charlie should be returned.
    """
    rows = run_student_sql(sqlite_db, "sql/assignment1.sql")

    names = {row[0] for row in rows}

    assert names == {"Alice", "Charlie"}, f"Unexpected users returned: {names}"