from flask import Flask, jsonify, g, render_template
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATABASE = 'energy_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with open('schema.sql') as f:
                db.executescript(f.read())
            generate_simulated_data(db)
            db.commit()

def generate_simulated_data(db, steps=10):
    start_time = datetime.strptime("2023-04-10 08:00:00", "%Y-%m-%d %H:%M:%S")
    base_voltage = 220.0
    base_power = 100.0

    for i in range(steps):
        timestamp = start_time + timedelta(minutes=10 * i)
        voltage = base_voltage + (i * 80)
        power = base_power + (i * 10)  # Or another pattern
        energy = power * (10.0 / 60.0)  # Power × hours (10 mins = 1/6 hr)
        db.execute(
            'INSERT INTO energy_data (timestamp, power_consumption, voltage, energy) VALUES (?, ?, ?, ?)',
            (timestamp.strftime('%Y-%m-%d %H:%M:%S'), power, voltage, energy)
        )

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM energy_data ORDER BY timestamp DESC LIMIT 1')
    latest_data = cur.fetchone()
    cur = db.execute('SELECT SUM(energy) as total_energy FROM energy_data')
    total_energy = cur.fetchone()['total_energy'] or 0
    return render_template('index.html', latest_data=latest_data, total_energy=total_energy)

@app.route('/api/interval_deltas')
def get_interval_deltas():
    db = get_db()
    cur = db.execute('SELECT timestamp, power_consumption, energy FROM energy_data ORDER BY timestamp ASC')
    rows = cur.fetchall()
    result = []

    for i in range(1, len(rows)):
        prev = rows[i - 1]
        curr = rows[i]
        delta_power = curr['power_consumption'] - prev['power_consumption']
        delta_energy = curr['energy'] - prev['energy']
        result.append({
            'interval_start': prev['timestamp'],
            'interval_end': curr['timestamp'],
            'delta_power': round(delta_power, 2),
            'delta_energy': round(delta_energy, 4)
        })

    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
