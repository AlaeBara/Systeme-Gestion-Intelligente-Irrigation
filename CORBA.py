#!/usr/bin/env python3

# Import render_template for HTML pages and jsonify for API responses
from flask import Flask, request, jsonify, render_template
import sys
import json
import time
import sqlite3
import os

# --- Database Configuration ---
DATABASE_FILE = "sensor_data.db"
# ----------------------------

# --- CORBA Imports and Setup ---
# (Same as before - checking if CORBA is available)
try:
    from omniORB import CORBA
    import CosNaming
    import IoTData # Assumes SensorData.idl produced an IoTData module
    print("CORBA libraries imported successfully.")
    CORBA_ENABLED = True
except ImportError as e:
    print(f"WARNING: Failed to import CORBA libraries or IDL stubs: {e}", file=sys.stderr)
    print("Gateway will run WITHOUT CORBA integration.", file=sys.stderr)
    CORBA_ENABLED = False
    # Define dummy classes/variables if CORBA is not enabled
    class CORBA:
        class Exception(Exception): pass
    class IoTData:
        class SensorReadings: pass
    class CosNaming:
        class NamingContext: pass
        class NotFound(Exception): pass
# ----------------------------------

# --- Configuration ---
GATEWAY_LISTEN_IP = "192.168.148.171" # Specific IP address to listen on
GATEWAY_PORT = 5001                  # Port for this gateway service
# --- CORBA Target Configuration (Only used if CORBA_ENABLED is True) ---
CORBA_NAMING_SERVICE_IP = "192.168.148.171"
CORBA_NAMING_SERVICE_PORT = "1050"
CORBA_OBJECT_NAME = "SensorManager"
# Default/sentinel values for potentially missing sensor data
DEFAULT_TEMP = None
DEFAULT_AIR_HUM = None
DEFAULT_SOIL_MOIST = None
# -------------------

# --- Global CORBA Variables ---
orb = None
sensor_manager_ref = None
# --------------------------

# --- Function to Initialize SQLite Database ---
def initialize_database():
    """Creates the database file and table if they don't exist."""
    print(f"Initializing database '{DATABASE_FILE}'...")
    try:
        # Use check_same_thread=False for Flask's multithreaded access
        conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        cursor = conn.cursor()
        # This definition includes the 'id' column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature REAL,
                air_humidity REAL,
                soil_moisture INTEGER,
                pump_on INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
        return True
    except sqlite3.Error as e:
        print(f"FATAL ERROR: Failed to initialize SQLite database: {e}", file=sys.stderr)
        return False
# -----------------------------------------

# --- Function to Save Data to SQLite ---
def save_to_database(timestamp, temp, air_hum, soil_moist, pump_on):
    """Inserts a new record into the sensor_readings table."""
    print("Attempting to save data to SQLite database...")
    try:
        conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_readings (timestamp, temperature, air_humidity, soil_moisture, pump_on)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, temp, air_hum, soil_moist, 1 if pump_on else 0))
        conn.commit()
        conn.close()
        print("Data saved to database successfully.")
        return True
    except sqlite3.Error as e:
        print(f"ERROR saving data to SQLite database: {e}", file=sys.stderr)
        return False
# --------------------------------------

# --- Function to Get Readings from DB (Used by Web UI and JSON API) ---
def get_readings_from_db(limit=None):
     """
     Fetches sensor readings from the database.
     If limit is specified, gets the latest N records.
     If limit is None, gets all records.
     """
     readings = []
     # --- CODE FIX: Order by timestamp instead of id to avoid 'no such column' error ---
     # --- if the table was created without the id column initially.              ---
     query = '''
            SELECT timestamp, temperature, air_humidity, soil_moisture, pump_on
            FROM sensor_readings
            ORDER BY timestamp DESC
        '''
     # --------------------------------------------------------------------------------
     params = []
     if limit:
         query += " LIMIT ?"
         params.append(limit)

     try:
        conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row # Access rows by column name
        cursor = conn.cursor()
        cursor.execute(query, params)
        readings = cursor.fetchall() # Fetch results
        conn.close()
        print(f"Fetched {len(readings)} readings from database (Limit: {limit}).")
     except sqlite3.Error as e:
        print(f"ERROR fetching data from SQLite database: {e}", file=sys.stderr)
     # Convert Row objects to dictionaries for JSON serialization
     return [dict(row) for row in readings]
# --------------------------------------------

# --- Function to Initialize CORBA (Only if enabled) ---
def initialize_corba():
    # (CORBA initialization code remains the same as before)
    # ... [omitted for brevity - see previous version] ...
    global orb, sensor_manager_ref
    if not CORBA_ENABLED:
        print("CORBA is disabled, skipping initialization.")
        return False
    if orb is not None: return True # Assume okay

    try:
        print("Initializing CORBA ORB...")
        orb_args = sys.argv + [ f'-ORBInitRef', f'NameService=corbaloc::1.2@{CORBA_NAMING_SERVICE_IP}:{CORBA_NAMING_SERVICE_PORT}/NameService' ]
        orb = CORBA.ORB_init(orb_args, CORBA.ORB_ID)
        if orb is None: raise RuntimeError("ORB_init failed")
        print(f"Resolving NameService at {CORBA_NAMING_SERVICE_IP}:{CORBA_NAMING_SERVICE_PORT}...")
        obj = orb.resolve_initial_references("NameService")
        ncRef = obj._narrow(CosNaming.NamingContext)
        if ncRef is None: raise RuntimeError("Failed to narrow NamingContext.")
        print(f"Resolving CORBA object '{CORBA_OBJECT_NAME}'...")
        name = [CosNaming.NameComponent(CORBA_OBJECT_NAME, "")]
        obj = ncRef.resolve(name)
        sensor_manager_ref = obj._narrow(IoTData.SensorDataManager)
        if sensor_manager_ref is None: raise RuntimeError(f"Failed to narrow reference to IoTData.SensorDataManager.")
        print("CORBA setup successful.")
        return True
    except CosNaming.NotFound as ex:
        print(f"CORBA Error: Object '{CORBA_OBJECT_NAME}' not found.", file=sys.stderr); sensor_manager_ref = None; return False
    except (CORBA.COMM_FAILURE, CORBA.TRANSIENT) as ex:
         print(f"CORBA Communication Error.", file=sys.stderr); sensor_manager_ref = None; return False
    except CORBA.Exception as ex:
        print(f"CORBA Error during initialization: {ex}", file=sys.stderr); sensor_manager_ref = None; return False
    except Exception as ex:
         print(f"Non-CORBA Error during initialization: {ex}", file=sys.stderr); sensor_manager_ref = None; return False
# ----------------------------------

# --- Flask Application ---
# Initialize Flask app. It will look for templates in a 'templates' folder
app = Flask(__name__)

# --- Route for the Web Dashboard ---
@app.route('/', methods=['GET'])
def dashboard():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request received for dashboard ('/')")
    # Fetch the latest readings from the database for the web page
    latest_readings_for_web = get_readings_from_db(limit=50) # Get latest 50 records

    # Render the HTML template, passing the data to it
    # Flask automatically looks for 'dashboard.html' in the 'templates' folder
    # Pass the current time to the template as well
    current_time_str = time.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('dashboard.html', readings=latest_readings_for_web, current_time=current_time_str)
# ---------------------------------

# --- NEW Route to provide data as JSON ---
@app.route('/showdata', methods=['GET'])
def show_data_json():
    """API endpoint to return all sensor readings from the database as JSON."""
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request received for JSON data ('/showdata')")
    # Fetch all readings from the database (no limit)
    all_readings = get_readings_from_db(limit=None)

    # Return the data using Flask's jsonify function, which sets the correct Content-Type header
    return jsonify(all_readings)
# -----------------------------------------

# --- Route to receive sensor data (API endpoint) ---
@app.route('/sensordata', methods=['POST'])
def receive_sensor_data():
    # (This function remains mostly the same as before)
    # ... [omitted for brevity - see previous version] ...
    global sensor_manager_ref
    request_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{request_timestamp}] Received request on /sensordata from {request.remote_addr}")

    if not request.is_json:
        print("Error: Request was not JSON"); return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.get_json(); print(f"Received data: {json.dumps(data, indent=2)}")

    if "pump_on" not in data:
         print(f"Error: Missing required key 'pump_on'"); return jsonify({"status": "error", "message": "Missing 'pump_on'"}), 400

    temp = data.get('temperature', DEFAULT_TEMP)
    air_hum = data.get('air_humidity', DEFAULT_AIR_HUM)
    soil_moist = data.get('soil_moisture', DEFAULT_SOIL_MOIST)
    pump_on = data.get('pump_on', False)

    db_save_success = save_to_database(request_timestamp, temp, air_hum, soil_moist, pump_on)
    if not db_save_success: print("WARNING: Failed to save data to database, continuing...")

    if CORBA_ENABLED:
        print("Attempting to forward data to CORBA server...")
        if sensor_manager_ref is None:
            print("CORBA ref invalid. Re-initializing...");
            if not initialize_corba():
                 print("Failed CORBA re-init."); return jsonify({"status": "error", "message": "Gateway cannot connect to CORBA service"}), 503

        try:
            corba_temp = float(temp if temp is not None else -999.9)
            corba_air_hum = float(air_hum if air_hum is not None else -1.0)
            corba_soil_moist = int(soil_moist if soil_moist is not None else -1)
            corba_pump_on = bool(pump_on)
        except (ValueError, TypeError) as e:
            print(f"Error: Invalid data type for CORBA - {e}", file=sys.stderr)
            return jsonify({"status": "partial_error", "message": "Invalid data type for CORBA forwarding"}), 400

        try:
            corba_data = IoTData.SensorReadings(temperature=corba_temp, airHumidity=corba_air_hum, soilMoisture=corba_soil_moist, isPumpOn=corba_pump_on)
            print(f"Prepared CORBA data: {corba_data}")
            print("Calling CORBA submitReadings method...")
            sensor_manager_ref.submitReadings(corba_data)
            print("Data forwarded successfully via CORBA.")
            return jsonify({"status": "success", "message": "Data received, saved to DB, and forwarded"}), 200
        except (CORBA.COMM_FAILURE, CORBA.TRANSIENT) as ex:
             print(f"CORBA Comm Error: {ex}", file=sys.stderr); sensor_manager_ref = None
             return jsonify({"status": "partial_error", "message": "Failed to communicate with CORBA server"}), 503
        except CORBA.Exception as ex:
            print(f"CORBA Error: {ex}", file=sys.stderr)
            return jsonify({"status": "partial_error", "message": "Failed to forward data due to CORBA error"}), 500
        except Exception as e:
            print(f"Error during CORBA call: {e}", file=sys.stderr)
            return jsonify({"status": "partial_error", "message": "Internal server error during CORBA forwarding"}), 500
    else:
        print("CORBA disabled. Acknowledging receipt/DB save.")
        if db_save_success: return jsonify({"status": "success", "message": "Data received/saved (CORBA disabled)"}), 200
        else: return jsonify({"status": "error", "message": "Data received but failed DB save (CORBA disabled)"}), 500

# --- Main Entry Point ---
if __name__ == '__main__':
    print("Starting HTTP Gateway Server with SQLite, Web UI & JSON API...")

    # --- Initialize Database ---
    if not initialize_database():
        sys.exit(1)

    # --- Initialize CORBA (if enabled) ---
    if CORBA_ENABLED: initialize_corba()
    else: print("Skipping CORBA initialization as it's disabled.")

    print(f"Gateway attempting to listen on http://{GATEWAY_LISTEN_IP}:{GATEWAY_PORT}")
    print(f"Web interface available at http://{GATEWAY_LISTEN_IP}:{GATEWAY_PORT}/")
    print(f"JSON data available at http://{GATEWAY_LISTEN_IP}:{GATEWAY_PORT}/showdata")
    print(f"Sensor data will be saved to '{DATABASE_FILE}'")
    print("Use Ctrl+C to stop the server.")
    # Run the Flask web server
    try:
        app.run(host=GATEWAY_LISTEN_IP, port=GATEWAY_PORT, debug=False)
    except OSError as e:
        if "Cannot assign requested address" in str(e):
             print(f"\nERROR: Cannot bind to IP address {GATEWAY_LISTEN_IP}.", file=sys.stderr)
             print("Verify IP belongs to this machine. Use '0.0.0.0' to listen on all interfaces.", file=sys.stderr)
        else: print(f"\nERROR starting Flask server: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR starting Flask server: {e}", file=sys.stderr)
        sys.exit(1)