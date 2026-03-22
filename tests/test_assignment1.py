import json
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

def run_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def test_assignment_query(sqlite_db):
    json_file = open("test-results.json", "w")
    queries = load_queries("02_activities/assignments/DC_Cohort/assignment1.sql")
    test_result = []
    for number, query in queries.items():
        rows = run_query(sqlite_db, query)
        test_result.append( { "number":number, "query": query, "result": rows })

    json.dump(test_result, json_file, indent=2)
    json_file.close()
    assert True,  "test execution query {} result {}".format(query, rows)

