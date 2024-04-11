import psutil
import datetime
import subprocess
import os
import socket
import sys
import json
import logging

# Configure logging
logging.basicConfig(filename='client_side.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def install_requirements():
    if os.path.exists('/opt/perfmon/reqcheck.txt'):
        logging.info("Requirements already installed.")
        return

    if os.path.exists('requirements.txt'):
        try:
            logging.info("Installing packages from requirements.txt...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            logging.info("Installation completed.")

            with open('/opt/perfmon/reqcheck.txt', 'w') as f:
                f.write('Requirements installed.')

        except subprocess.CalledProcessError as e:
            logging.error(f"An error occurred while installing packages: {e}")
    else:
        logging.info("requirements.txt not found.")

def capture_server_health():
    health_data = {
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat(),
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'network_in': psutil.net_io_counters().bytes_recv,
        'network_out': psutil.net_io_counters().bytes_sent
    }
    return health_data

def transmit_server_health(health_data):
    logging.info(f"Transmitting server health metrics to remote server...")
    json_data = json.dumps(health_data)
    logging.info('Sending data: %s', json_data)

    curl_command = [
        'curl',
        '-X', 'POST',
        'http://merc.securelogic.us:9000/api/insert',
        '-H', 'Content-Type: application/json',
        '-d', json_data
    ]

    try:
        response = subprocess.run(curl_command, check=True, text=True, capture_output=True)
        logging.info('Server response: %s', response.stdout)
    except subprocess.CalledProcessError as e:
        logging.error('Curl command failed: %s', e)

def main():
    install_requirements()
    health_metrics = capture_server_health()
    transmit_server_health(health_metrics)

if __name__ == "__main__":
    main()
