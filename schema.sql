DROP TABLE IF EXISTS energy_data;

CREATE TABLE energy_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    power_consumption REAL NOT NULL,  -- Watts
    voltage REAL NOT NULL,            -- Volts
    energy REAL NOT NULL              -- Watt-hours
);
