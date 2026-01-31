# simulator.py
import sqlite3, time, random, datetime

DB_PATH = "database.db"

equipments = ["Pump1", "Pump2", "Fan1", "Compressor1", "Compressor2"]

def generate_reading(equipment):
    """Generate one fake sensor reading for given equipment"""
    base_temp = 65
    base_vib = 0.02
    base_pressure = 110
    usage = round(random.uniform(1, 12), 2)

    # Normal values
    temp = base_temp + random.uniform(-5, 10)
    vib = base_vib + random.uniform(-0.01, 0.02)
    pressure = base_pressure + random.uniform(-5, 10)

    # Occasionally create failure spike
    if random.random() < 0.05:  # 5% chance
        temp += random.uniform(15, 25)
        vib += random.uniform(0.05, 0.1)
        pressure += random.uniform(15, 25)

    failure = 1 if (temp > 85 and vib > 0.05) else 0

    return (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        equipment,
        usage,
        round(temp, 2),
        round(vib, 4),
        round(pressure, 2),
        failure
    )

def insert_reading(row):
    """Insert one reading into database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO readings (timestamp, equipment_id, usage_hours, temperature, vibration, pressure, failure)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, row)
    conn.commit()
    conn.close()

def run_simulator():
    print("Starting simulator... Press CTRL+C to stop.")
    while True:
        eq = random.choice(equipments)
        row = generate_reading(eq)
        insert_reading(row)
        print("Inserted:", row)
        time.sleep(5)  # wait 5 seconds

if __name__ == "__main__":
    run_simulator()
