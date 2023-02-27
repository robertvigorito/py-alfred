"""Database fields schema.
"""
tables = {
    "job": {
        "code": "CHAR(5)",
        "description": "TEXT",
        "format": "CHAR(25)",
        "hours": "FLOAT",
        "lut": "CHAR(25)",
        "name": "CHAR(25)",
        "status": "CHAR(25)"
    },
    "scene": {
        "assigned": "CHAR(25)",
        "code": "CHAR(5)",
        "description": "TEXT",
        "hours": "FLOAT",
        "job": None,
        "status": "CHAR(25)",
        "tags": "TEXT"
    },
    "shot": {
        "assigned": "CHAR(25)",
        "code": "CHAR(5)",
        "description": "TEXT",
        "hours": "FLOAT",
        "job": None,
        "renders": None,
        "scene": None,
        "status": "CHAR(25)",
        "tags": "TEXT",
        "tasks": None
    },
    "status": [
        "complete",
        "in_progress",
        "omit",
        "hold",
        "review",
        "approved",
        "final"
    ]
}
