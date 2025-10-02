import os
from ftplib import FTP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def upload_jobs_to_ftp():
    # Get FTP credentials from environment variables
    ftp_host = os.getenv('FTP_HOST')
    ftp_username = os.getenv('FTP_USERNAME')
    ftp_password = os.getenv('FTP_PASSWORD')
    ftp_directory = os.getenv('FTP_DIRECTORY')
    
    # Validate that all required environment variables are set
    if not all([ftp_host, ftp_username, ftp_password, ftp_directory]):
        raise ValueError("Missing required FTP environment variables. Please check your .env file.")
    
    ftp = FTP(ftp_host)
    ftp.login(ftp_username, ftp_password)
    ftp.cwd(ftp_directory) 
    
    # Upload jobs.json file
    with open('jobs.json', 'rb') as file:
        ftp.storbinary('STOR jobs.json', file)
    print("jobs.json uploaded successfully")
    
    # Upload jobs directory
    jobs_dir = "jobs"
    if os.path.exists(jobs_dir):
        # Create jobs directory on FTP server
        try:
            ftp.mkd('jobs')
        except:
            pass  # Directory might already exist
        
        # Get all HTML files from jobs directory
        jobs_files = []
        for file in os.listdir(jobs_dir):
            if file.endswith('.html'):
                local_path = os.path.join(jobs_dir, file)
                jobs_files.append((local_path, f'jobs/{file}'))
        
        # Upload each HTML file
        for local_path, remote_path in jobs_files:
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
            print(f"Uploaded: {remote_path}")
        
        print(f"Uploaded {len(jobs_files)} job description files")
    else:
        print("Warning: jobs directory does not exist")
    
    ftp.quit()
    print("All files uploaded successfully to FTP")