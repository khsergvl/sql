from pathlib import Path
import sqlite3
import re

QUERY_PATTERN = re.compile(
    r"--\s*QUERY\s*(\d+)\s*\n(.*?)\n--\s*END\s*QUERY",
    re.DOTALL | re.IGNORECASE
)

def load_queries(sql_file):
    sql = Path(sql_file).read_text()

    queries = {}
    for number, body in QUERY_PATTERN.findall(sql):
        query = body.strip().rstrip(";")
        if not query:
            raise ValueError(f"Query {number} is empty")
        queries[int(number)] = query

    if not queries:
        raise AssertionError(
            "No queries found. Use '-- QUERY <n>' and '-- END QUERY' markers."
        )

    return queries

def run_query(conn, sql_file, query_number):
    queries = load_queries(sql_file)

    if query_number not in queries:
        raise AssertionError(f"Query {query_number} not found in {sql_file}")

    cursor = conn.cursor()
    cursor.execute(queries[query_number])
    return cursor.fetchall()

def test_assignment1_query1(sqlite_db):
    rows = run_query(sqlite_db, "02_activities/assignments/DC_Cohort/assignment1.sql", 1)

    assert len(rows) > 0, "Query returned no rows"

    for name, age in rows:
        assert age > 25, f"User {name} is not older than 25"
