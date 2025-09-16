import sqlite3
from datetime import datetime, timedelta
import random

DB = 'energy.db'

def add_devices(conn, n=10):
    cur = conn.cursor()
    for i in range(1, n+1):
        name = f'Licznik {i}'
        location = f'Pomieszczenie {i}'
        serial = f'SN{i:03d}'
        cur.execute('INSERT OR IGNORE INTO devices (id, name, location, serial) VALUES (?, ?, ?, ?)', (i, name, location, serial))
    conn.commit()

def add_readings(conn, days=30, devices=10, per_day=24):
    cur = conn.cursor()
    now = datetime.now()
    for device_id in range(1, devices+1):
        for day in range(days):
            base = now - timedelta(days=day)
            for h in range(per_day):
                ts = (base.replace(hour=h, minute=0, second=0, microsecond=0)).isoformat(sep=' ')
                value = random.uniform(100, 500)  # 100-500 Wh
                cur.execute('INSERT INTO readings (device_id, timestamp, value_wh) VALUES (?, ?, ?)', (device_id, ts, value))
    conn.commit()

def main():
    conn = sqlite3.connect(DB)
    add_devices(conn, n=10)
    add_readings(conn, days=30, devices=10, per_day=24)
    conn.close()
    print('Dodano testowe urządzenia i odczyty!')

if __name__ == '__main__':
    main()
