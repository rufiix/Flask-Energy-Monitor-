import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect('energy.db')
cur = conn.cursor()

num_devices = 3       # liczba urządzeń
days = 30             # ile dni wstecz
readings_per_day = 10 # liczba odczytów na dzień

now = datetime.now()

for device_id in range(1, num_devices + 1):
    for day in range(days):
        day_time = now - timedelta(days=day)
        for i in range(readings_per_day):
            # Losowy czas w ciągu dnia
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            timestamp = day_time.replace(hour=hour, minute=minute, second=second, microsecond=0)
            
            # Losowa wartość zużycia
            value_wh = round(random.uniform(5, 50), 2)
            
            cur.execute(
                "INSERT INTO readings (device_id, timestamp, value_wh) VALUES (?, ?, ?)",
                (device_id, timestamp.strftime('%Y-%m-%d %H:%M:%S'), value_wh)
            )

conn.commit()
conn.close()

print(f"Dodano {num_devices * days * readings_per_day} rekordów do tabeli readings!")
