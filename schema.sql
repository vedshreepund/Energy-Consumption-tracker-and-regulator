
DROP TABLE IF EXISTS energy_data;

CREATE TABLE energy_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    power_consumption REAL NOT NULL,
    voltage REAL NOT NULL
);

-- Add some sample data for testing
INSERT INTO energy_data (device_id, timestamp, power_consumption, voltage) VALUES 
    ('ESP32-001', '2023-04-10 08:00:00', 120.5, 220.0),
    ('ESP32-001', '2023-04-10 09:00:00', 150.2, 221.5),
    ('ESP32-001', '2023-04-10 10:00:00', 135.8, 219.8),
    ('ESP32-001', '2023-04-10 11:00:00', 142.3, 220.3),
    ('ESP32-001', '2023-04-10 12:00:00', 165.7, 220.1),
    ('ESP32-001', '2023-04-10 13:00:00', 178.9, 221.0),
    ('ESP32-001', '2023-04-10 14:00:00', 169.3, 220.8),
    ('ESP32-001', '2023-04-10 15:00:00', 155.6, 220.2),
    ('ESP32-001', '2023-04-11 08:00:00', 125.7, 219.7),
    ('ESP32-001', '2023-04-11 09:00:00', 145.3, 220.5),
    ('ESP32-001', '2023-04-11 10:00:00', 138.9, 220.1);
