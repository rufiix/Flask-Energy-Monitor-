# Flask Energy Monitoring System

## Overview

Energy Monitor is a web application designed to monitor the electricity consumption of various devices. Built with Python and the Flask framework, it provides a clean web interface to track energy usage in near real-time, generate daily reports, and export historical data.

The system uses an SQLite database to store device information and consumption readings, which are then visualized on the frontend using Chart.js. The application also includes a set of RESTful API endpoints for managing devices and data.

---

## Features

* **Device Management**: Add and list all monitored devices through the API.
* **Data Logging**: Record energy consumption readings (in Watt-hours) for each device with a timestamp.
* **Real-Time Visualization**: The frontend features an interactive bar chart (using Chart.js) that displays the latest energy consumption data for all devices.
* **Daily Reports**: Fetch aggregated daily energy consumption for any device and any given date.
* **CSV Export**: Export all historical readings for a specific device to a CSV file for further analysis.
* **Helper Scripts**: Includes scripts to initialize the database (`init_db.py`) and populate it with sample data (`populate_db.py`) for testing purposes.

---

## Technology Stack

* **Backend**: Python, Flask
* **Database**: SQLite
* **Frontend**: HTML, JavaScript, Chart.js

---

## Database Schema

The application uses an SQLite database (`energy.db`) with the following two tables:

### `devices` Table
Stores information about the monitored devices.
```sql
CREATE TABLE devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  location TEXT,
  serial TEXT UNIQUE,
  installed_at DATETIME DEFAULT (datetime('now'))
);
