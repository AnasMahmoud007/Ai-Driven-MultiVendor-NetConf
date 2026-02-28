import logging
import requests
import urllib3
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/deploy', methods=['POST'])
def deploy_config():
    data = request.json
    
    vendor = data.get('vendor')
    config_text = data.get('config')
    
    # -------------------------------------------------------
    # CREDENTIAL HANDLING
    # 1. Use values from UI text boxes if provided
    # 2. Fallback to hardcoded defaults if empty
    # -------------------------------------------------------
    host = data.get('host')
    if not host or host.strip() == "":
        host = "192.168.122.50"
        
    username = data.get('username') 
    if not username or username.strip() == "":
        username = "admin"
        
    password = data.get('password')
    if not password:
        password = "admin"
    # -------------------------------------------------------

    if not all([vendor, config_text]):
        return jsonify({"success": False, "error": "Missing Vendor or Config data"}), 400

    # Device Type Mapping
    device_type_map = {
        "Cisco IOS-XE": "cisco_ios",
        "Cisco NX-OS": "cisco_nxos",
        "Juniper Junos": "juniper_junos",
        "Fortinet FortiOS": "fortinet",
        "Arista EOS": "arista_eos",
        "Palo Alto PAN-OS": "paloalto_panos",
        "Huawei VRP": "huawei",
        "MikroTik RouterOS": "mikrotik_routeros"
    }

    netmiko_type = device_type_map.get(vendor, "autodetect")
    logger.info(f"Connecting to {host} ({netmiko_type}) as {username}...")

    device = {
        "device_type": netmiko_type,
        "host": host,
        "username": username,
        "password": password,
        "port": 22,
        "fast_cli": False,
        "global_delay_factor": 2  # Slow down for older devices/GNS3
    }

    try:
        net_connect = ConnectHandler(**device)
        config_lines = config_text.splitlines()
        
        # Send configuration
        output = net_connect.send_config_set(config_lines)
            
        # Commit for Juniper
        if "juniper" in netmiko_type:
            output += "\n" + net_connect.commit()

        net_connect.disconnect()
        
        logger.info("Configuration applied successfully.")
        return jsonify({"success": True, "log": output})

    except NetmikoAuthenticationException:
        return jsonify({"success": False, "error": f"Authentication Failed for {username}@{host}"}), 401
    except NetmikoTimeoutException:
        return jsonify({"success": False, "error": f"Timeout: Could not reach {host} on port 22"}), 408
    except Exception as e:
        logger.error(f"Deployment Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
