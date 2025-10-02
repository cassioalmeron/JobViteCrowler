import os
from ftplib import FTP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def upload_service_files():
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
    
    # Define the source directories
    source_dirs = ["../Site/dist", "jobs"]
    
    # Get all files from the source directories recursively
    files_to_upload = []
    
    for source_dir in source_dirs:
        if not os.path.exists(source_dir):
            print(f"Warning: Source directory {source_dir} does not exist")
            continue
            
        # Get all files recursively from each directory
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate relative path from source_dir
                relative_path = os.path.relpath(file_path, source_dir)
                # Add directory name prefix to avoid conflicts
                if source_dir == "jobs":
                    relative_path = f"jobs/{relative_path}"
                files_to_upload.append((file_path, relative_path))
    
    # Upload each file
    uploaded_count = 0
    for local_path, remote_path in files_to_upload:
        try:
            # Create directory structure on FTP server if needed
            remote_dir = os.path.dirname(remote_path)
            if remote_dir and remote_dir != '.':
                try:
                    ftp.mkd(remote_dir)
                except:
                    pass  # Directory might already exist
            
            # Upload file
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
            print(f"Uploaded: {remote_path}")
            uploaded_count += 1
            
        except Exception as e:
            print(f"Error uploading {remote_path}: {e}")
    
    ftp.quit()
    print(f"Deploy completed! {uploaded_count} files uploaded to FTP")

if __name__ == "__main__":
    upload_service_files()