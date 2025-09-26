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
    
    # Use storbinary for binary files instead of storlines
    with open('jobs.json', 'rb') as file:
        ftp.storbinary('STOR jobs.json', file)
    
    ftp.quit()
    print("jobs.json uploaded successfully to FTP")