"""Just bunch of SQL query."""

createTimerTable = """
    CREATE TABLE IF NOT EXISTS timer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT,
        extra TEXT,
        expires REAL,
        created REAL,
        owner INT
    )
"""

# ---
