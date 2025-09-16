

from flask import Flask, request, jsonify, g, Response, send_from_directory
import sqlite3, csv, io
from datetime import datetime, date

DB = 'energy.db'
app = Flask(__name__, static_folder='static', static_url_path='/static')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Serwujemy frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Lista urządzeń
@app.route('/api/devices', methods=['GET'])
def list_devices():
    db = get_db()
    rows = db.execute('SELECT id, name, location, serial FROM devices').fetchall()
    return jsonify([dict(r) for r in rows])

# Dodaj urządzenie (opcjonalne, przydatne do testów)
@app.route('/api/devices', methods=['POST'])
def add_device():
    j = request.get_json()
    name = j.get('name')
    if not name:
        return jsonify({'error':'name required'}), 400
    loc = j.get('location')
    serial = j.get('serial')
    db = get_db()
    cur = db.execute('INSERT INTO devices (name, location, serial) VALUES (?,?,?)', (name, loc, serial))
    db.commit()
    return jsonify({'id': cur.lastrowid}), 201

# Dodaj odczyt
@app.route('/api/readings', methods=['POST'])
def add_reading():
    j = request.get_json()
    try:
        device_id = int(j['device_id'])
        value_wh = float(j['value_wh'])
    except Exception:
        return jsonify({'error':'device_id and numeric value_wh required'}), 400

    ts = j.get('timestamp')
    if ts:
        # oczekujemy ISO8601 (np. "2025-09-14T12:00:00")
        try:
            # not strict parsing; store as string ISO
            parsed = datetime.fromisoformat(ts)
            ts = parsed.isoformat(sep=' ')
        except Exception:
            # jeśli nie parsuje, użyj przekazanego ciągu
            pass
    else:
        ts = datetime.utcnow().isoformat(sep=' ')

    db = get_db()
    db.execute('INSERT INTO readings (device_id, timestamp, value_wh) VALUES (?,?,?)', (device_id, ts, value_wh))
    db.commit()
    return jsonify({'status':'ok'}), 201

# Raport dzienny - JSON
@app.route('/api/reports/daily', methods=['GET'])
def daily_json():
    qdate = request.args.get('date')
    if not qdate:
        qdate = date.today().isoformat()
    db = get_db()
    sql = """SELECT d.id AS device_id, d.name,
             SUM(r.value_wh)/1000.0 AS kwh
             FROM readings r JOIN devices d ON d.id=r.device_id
             WHERE date(r.timestamp)=?
             GROUP BY r.device_id, d.name"""
    rows = db.execute(sql, (qdate,)).fetchall()
    out = [dict(r) for r in rows]
    return jsonify({'date': qdate, 'data': out})

# Raport dzienny - CSV
@app.route('/api/reports/daily.csv', methods=['GET'])
def daily_csv():
    qdate = request.args.get('date')
    if not qdate:
        qdate = date.today().isoformat()
    db = get_db()
    sql = """SELECT d.name, SUM(r.value_wh)/1000.0 AS kwh
             FROM readings r JOIN devices d ON d.id=r.device_id
             WHERE date(r.timestamp)=?
             GROUP BY r.device_id, d.name"""
    rows = db.execute(sql, (qdate,)).fetchall()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['device_name','kwh'])
    for r in rows:
        cw.writerow([r['name'], r['kwh']])
    return Response(si.getvalue(), mimetype='text/csv',
                    headers={"Content-disposition": f"attachment; filename=daily_{qdate}.csv"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
