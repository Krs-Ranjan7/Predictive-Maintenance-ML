import sqlite3, os, datetime, random

DB = os.path.join(os.path.dirname(__file__), "database.db")
conn = sqlite3.connect(DB)
cur = conn.cursor()

# --------------------------
# Readings
# --------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    equipment_id TEXT,
    usage_hours REAL,
    temperature REAL,
    vibration REAL,
    pressure REAL,
    failure INTEGER
)
""")

# --------------------------
# Predictions
# --------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    equipment_id TEXT,
    predicted_prob REAL,
    predicted_label INTEGER
)
""")

# --------------------------
# Maintenance tasks
# --------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS maintenance_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT,
    description TEXT,
    scheduled_date TEXT,
    status TEXT
)
""")

# --------------------------
# Users
# --------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# --------------------------
# Dummy data insertion
# --------------------------
# Users
cur.execute("SELECT * FROM users WHERE username='employee1'")
if not cur.fetchone():
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", ("employee1","emp123"))
cur.execute("SELECT * FROM users WHERE username='admin'")
if not cur.fetchone():
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", ("admin","admin123"))

# Predictions
cur.execute("SELECT * FROM predictions")
if not cur.fetchone():
    cur.execute("INSERT INTO predictions (timestamp,equipment_id,predicted_prob,predicted_label) VALUES (?,?,?,?)",
                ("2025-10-08 10:00:00", "EQ-1", 0.75, 0))
    cur.execute("INSERT INTO predictions (timestamp,equipment_id,predicted_prob,predicted_label) VALUES (?,?,?,?)",
                ("2025-10-08 10:05:00", "EQ-2", 0.85, 1))

# Maintenance tasks
cur.execute("SELECT * FROM maintenance_tasks")
if not cur.fetchone():
    cur.execute("INSERT INTO maintenance_tasks (equipment_id, description, scheduled_date, status) VALUES (?,?,?,?)",
                ("EQ-1","Replace filter","2025-10-10","Pending"))
    cur.execute("INSERT INTO maintenance_tasks (equipment_id, description, scheduled_date, status) VALUES (?,?,?,?)",
                ("EQ-2","Lubricate motor","2025-10-12","Pending"))

# Dummy readings
cur.execute("SELECT * FROM readings")
if not cur.fetchone():
    equipments = ["Pump1","Pump2","Fan1","Compressor1","Compressor2"]
    for eq in equipments:
        for i in range(5):
            ts = (datetime.datetime.now() - datetime.timedelta(minutes=i*5)).strftime("%Y-%m-%d %H:%M:%S")
            temp = random.uniform(60,85)
            vib = random.uniform(0.01,0.06)
            pressure = random.uniform(105,115)
            usage = random.uniform(1,12)
            failure = 1 if temp>80 and vib>0.05 else 0
            cur.execute("INSERT INTO readings (timestamp,equipment_id,usage_hours,temperature,vibration,pressure,failure) VALUES (?,?,?,?,?,?,?)",
                        (ts, eq, usage, temp, vib, pressure, failure))

conn.commit()
conn.close()
print("✅ Database initialized successfully!")
