
from flask import Flask, request, render_template, jsonify, g
import sqlite3
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

DATABASE = 'energy_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    # Get the latest energy consumption data
    db = get_db()
    cur = db.execute('SELECT * FROM energy_data ORDER BY timestamp DESC LIMIT 1')
    latest_data = cur.fetchone()
    
    # Get today's total consumption
    today = datetime.now().strftime('%Y-%m-%d')
    cur = db.execute('SELECT SUM(power_consumption) as today_total FROM energy_data WHERE date(timestamp) = ?', (today,))
    today_total = cur.fetchone()['today_total'] or 0
    
    return render_template('index.html', latest_data=latest_data, today_total=today_total)

@app.route('/daily')
def daily():
    return render_template('daily.html')

@app.route('/monthly')
def monthly():
    return render_template('monthly.html')

@app.route('/api/data', methods=['POST'])
def receive_data():
    """Endpoint for ESP32 to send energy data"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['device_id', 'power_consumption', 'voltage']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Get timestamp or use current time
    timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Store data in database
    db = get_db()
    db.execute(
        'INSERT INTO energy_data (device_id, timestamp, power_consumption, voltage) VALUES (?, ?, ?, ?)',
        (data['device_id'], timestamp, data['power_consumption'], data['voltage'])
    )
    db.commit()
    
    return jsonify({"status": "success", "message": "Data received"}), 201

@app.route('/api/daily_data')
def get_daily_data():
    """Get energy data for the past 7 days"""
    days = 7
    result = []
    db = get_db()
    
    for i in range(days-1, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        cur = db.execute(
            'SELECT SUM(power_consumption) as total FROM energy_data WHERE date(timestamp) = ?', 
            (date,)
        )
        total = cur.fetchone()['total'] or 0
        result.append({
            'date': date,
            'consumption': float(total)
        })
    
    return jsonify(result)

@app.route('/api/monthly_data')
def get_monthly_data():
    """Get energy data for the past 12 months"""
    months = 12
    result = []
    db = get_db()
    
    for i in range(months-1, -1, -1):
        today = datetime.now()
        first_day = (today.replace(day=1) - timedelta(days=i*30)).strftime('%Y-%m-%d')
        if i > 0:
            last_day = (today.replace(day=1) - timedelta(days=(i-1)*30 - 1)).strftime('%Y-%m-%d')
        else:
            last_day = today.strftime('%Y-%m-%d')
        
        month_name = (today - timedelta(days=i*30)).strftime('%B')
        
        cur = db.execute(
            'SELECT SUM(power_consumption) as total FROM energy_data WHERE date(timestamp) BETWEEN ? AND ?', 
            (first_day, last_day)
        )
        total = cur.fetchone()['total'] or 0
        result.append({
            'month': month_name,
            'consumption': float(total)
        })
    
    return jsonify(result)

@app.route('/api/hourly_data')
def get_hourly_data():
    """Get hourly energy data for today"""
    result = []
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    for hour in range(24):
        cur = db.execute(
            '''SELECT SUM(power_consumption) as total 
               FROM energy_data 
               WHERE date(timestamp) = ? 
               AND strftime('%H', timestamp) = ?''', 
            (today, f"{hour:02d}")
        )
        total = cur.fetchone()['total'] or 0
        result.append({
            'hour': f"{hour}:00",
            'consumption': float(total)
        })
    
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
