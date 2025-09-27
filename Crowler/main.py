#!/usr/bin/env python3
"""
Crowler Service Script with Hourly Logging
This script runs the crowler service with automatic hourly logging
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime
from crowler import sync_jobs, upload_jobs_to_ftp
from service_manager import manage_service

# Configure logging
log_dir = "/var/log"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/crowler.log'),
        logging.StreamHandler()
    ]
)

def six_hours_logger():
    """Log a message every six hours while the service is running"""
    while True:
        logging.info(f"Crowler service is running - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        run_crowler_job()
        time.sleep(6 * 3600)  # Sleep for 6 hours (21600 seconds)

def run_crowler_job():
    """Run the main crowler job"""
    try:
        logging.info("Starting crowler job...")
        sync_jobs()
        upload_jobs_to_ftp()
        logging.info("Crowler job completed successfully")
    except Exception as e:
        logging.error(f"Error in crowler job: {e}")
    
def main():
    """Main service function with hourly logging"""
    logging.info("Crowler service started")
    
    # Start the hourly logging in a separate thread
    logging_thread = threading.Thread(target=six_hours_logger, daemon=True)
    logging_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Crowler service stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error in service: {e}")
        
service_name = "LeanTech Jobs Crowler"

def install_service():
    """Install the crowler service using service_manager"""
    app_path = os.path.abspath(__file__)
    manage_service(service_name, "install", app_path)
    
def start_service():
    """Start the crowler service using service_manager"""
    manage_service(service_name, "start")
    
def stop_service():
    """Stop the crowler service using service_manager"""
    manage_service(service_name, "stop")
    
def uninstall_service():
    """Uninstall the crowler service using service_manager"""
    manage_service(service_name, "uninstall")

if __name__ == "__main__":
    # Se não há argumentos, executa como serviço
    if len(sys.argv) == 1:
        main()
    # Se há argumentos, executa comandos de gerenciamento
    else:
        action = sys.argv[1]
        if action == "install":
            install_service()
        elif action == "start":
            start_service()
        elif action == "stop":
            stop_service()
        elif action == "uninstall":
            uninstall_service()
        else:
            print("Invalid action. Available actions: install, start, stop, uninstall")
            print("Usage:")
            print("  python3 crowler_service.py          # Run as service")
            print("  python3 crowler_service.py install  # Install service")
            print("  python3 crowler_service.py start    # Start service")
            print("  python3 crowler_service.py stop     # Stop service")
            print("  python3 crowler_service.py uninstall # Uninstall service")
            sys.exit(1)
