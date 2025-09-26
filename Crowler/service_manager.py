import os
import sys
import subprocess

def manage_service(service_name, action, app_path=None):
    service_file = f"/etc/systemd/system/{service_name}.service"
    
    def run_cmd(cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    
    if action == "install" and app_path:
        script_dir = os.path.dirname(app_path)
        service_content = f"""[Unit]
Description=Crowler Service with Hourly Logging
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {app_path}
Restart=always
RestartSec=10
User=root
WorkingDirectory={script_dir}

[Install]
WantedBy=multi-user.target"""
        
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        run_cmd("systemctl daemon-reload")
        run_cmd(f"systemctl enable {service_name}")
        print(f"Service {service_name} installed!")
    
    elif action == "start":
        success, out, err = run_cmd(f"systemctl start {service_name}")
        print("Service started!" if success else f"Error: {err}")
    
    elif action == "stop":
        success, out, err = run_cmd(f"systemctl stop {service_name}")
        print("Service stopped!" if success else f"Error: {err}")
    
    elif action == "uninstall":
        run_cmd(f"systemctl stop {service_name}")
        run_cmd(f"systemctl disable {service_name}")
        os.remove(service_file)
        run_cmd("systemctl daemon-reload")
        print("Service uninstalled!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 service_manager.py <service> <action> [app_path]")
        sys.exit(1)
    
    service = sys.argv[1]
    action = sys.argv[2]
    app_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    manage_service(service, action, app_path)