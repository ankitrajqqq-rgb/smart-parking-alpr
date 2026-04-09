import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect("parking.db", check_same_thread=False)
cursor = conn.cursor()

# Create table (UPDATED STRUCTURE)
cursor.execute("""
CREATE TABLE IF NOT EXISTS parking (
    plate TEXT PRIMARY KEY,
    slot INTEGER,
    entry_time TEXT,
    exit_time TEXT,
    amount REAL
)
""")
conn.commit()

# 💰 Rate per hour
RATE_PER_HOUR = 20


def calculate_bill(entry_time):
    entry = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    hours = (now - entry).total_seconds() / 3600
    amount = round(hours * RATE_PER_HOUR, 2)

    return amount


def vehicle_entry(plate, slot):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT * FROM parking WHERE plate=?", (plate,))
    data = cursor.fetchone()

    # New vehicle entry
    if data is None:
        cursor.execute(
            "INSERT INTO parking (plate, slot, entry_time, exit_time, amount) VALUES (?, ?, ?, ?, ?)",
            (plate, slot, now, None, None)
        )
        conn.commit()
        print(f"[ENTRY] Plate: {plate} | Slot: {slot} | Time: {now}")


def vehicle_exit(plate):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT * FROM parking WHERE plate=?", (plate,))
    data = cursor.fetchone()

    if data and data[3] is None:  # exit_time is None
        entry_time = data[2]
        amount = calculate_bill(entry_time)

        cursor.execute(
            "UPDATE parking SET exit_time=?, amount=? WHERE plate=?",
            (now, amount, plate)
        )
        conn.commit()

        print(f"[EXIT] Plate: {plate} | Time: {now} | Amount: ₹{amount}")