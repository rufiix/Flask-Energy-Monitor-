PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  location TEXT,
  serial TEXT UNIQUE,
  installed_at DATETIME DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER NOT NULL,
  timestamp DATETIME NOT NULL,
  value_wh REAL NOT NULL,
  FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_readings_device_time ON readings(device_id, timestamp);

-- przykładowe urządzenie
INSERT OR IGNORE INTO devices (id, name, location, serial) VALUES (1,'Licznik 1','Biuro','SN001');
