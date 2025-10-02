from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import subprocess
from ftptransfer import upload_jobs_to_ftp
from datetime import datetime

def get_driver():
    chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')
    
    options = webdriver.ChromeOptions()
    if chrome_driver_path:
        options.binary_location = chrome_driver_path
    
        # Add necessary options for server environment
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--user-data-dir=/tmp/chrome-user-data")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
    
    return webdriver.Chrome(options=options)

def get_jobs(driver):
    driver.get("https://jobs.jobvite.com/leantechio/")
    
    # Wait for the page to load and elements to be present
    wait = WebDriverWait(driver, 10)
    
    try:
        # Wait for job list elements to be present
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jv-job-list-name")))
        
        # Find all elements with the class jv-job-list-name
        job_elements = driver.find_elements(By.CLASS_NAME, "jv-job-list-name")
        
        # Extract text content from all job elements
        job_titles = []
        for element in job_elements:
            link = element.find_element(By.TAG_NAME, "a")
            link_href = link.get_attribute("href")
            jobvite_id = link_href.split("/")[-1]
            job_title = element.text.strip()
            if job_title:  # Only add non-empty titles
                job_titles.append({"jobviteId": jobvite_id, "jobTitle": job_title})
        
        return job_titles
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
        
def get_job_meta_info(driver, jobvite_id) -> dict:
    """Extract sector, work mode and country from job meta information"""
    try:
        # Wait for meta element to be present
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jv-job-detail-meta")))
        
        meta_element = driver.find_element(By.CLASS_NAME, "jv-job-detail-meta")
        meta_text = meta_element.get_attribute("innerHTML")
        
        # Parse the meta information
        sector = ""
        work_mode = ""
        country = ""
        
        # Extract text content and split by separators
        import re
        # Remove HTML tags and get clean text
        clean_text = re.sub(r'<[^>]+>', '|', meta_text)
        clean_text = clean_text.replace('&amp;', '&')
        
        # Split by separators (| and ,)
        parts = [part.strip() for part in re.split(r'[|,]', clean_text) if part.strip()]
        
        if len(parts) >= 1:
            sector = parts[0]
        if len(parts) >= 2:
            work_mode = parts[1]
        if len(parts) >= 3:
            country = parts[2]
        
        return {
            "sector": sector,
            "work_mode": work_mode,
            "country": country
        }
        
    except Exception as e:
        print(f"Error extracting meta info for job {jobvite_id}: {e}")
        return {
            "sector": "",
            "work_mode": "",
            "country": ""
        }

def get_job_description(driver, jobvite_id) -> dict:
    driver.get(f"https://jobs.jobvite.com/leantechio/job/{jobvite_id}")
    
    wait = WebDriverWait(driver, 10)
    
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jv-job-detail-description")))
        
        # Get job description
        job_description = driver.find_element(By.CLASS_NAME, "jv-job-detail-description").get_attribute("innerHTML")
        job_description = job_description.replace("background-color: rgb(255,255,255);", "none")
        job_description = job_description.replace("\n", "")
        
        # Get meta information (sector, work mode, country)
        meta_info = get_job_meta_info(driver, jobvite_id)
        
        return {
            "description": job_description,
            "sector": meta_info["sector"],
            "work_mode": meta_info["work_mode"],
            "country": meta_info["country"]
        }
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            "description": "",
            "sector": "",
            "work_mode": "",
            "country": ""
        }
    
def sync_jobs():
    """Sync jobs from website and save to JSON file"""
    driver = get_driver()
    
    # Create jobs directory if it doesn't exist
    jobs_dir = "jobs"
    os.makedirs(jobs_dir, exist_ok=True)
    
    jobs = get_jobs(driver)
    
    # Update job descriptions and meta information
    for job in jobs:
        jobvite_id = job["jobviteId"]
        print(f"Processing {jobvite_id}: {job['jobTitle']}")
        job_details = get_job_description(driver, jobvite_id)
        
        # Save job description to separate HTML file
        html_file_path = os.path.join(jobs_dir, f"{jobvite_id}.html")
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(job_details["description"])
        print(f"  Saved description to: {html_file_path}")
        
        # Add all the extracted information in camelCase
        job["sector"] = job_details["sector"]
        job["workMode"] = job_details["work_mode"]
        job["country"] = job_details["country"]
        
        print(f"  Sector: {job['sector']}")
        print(f"  Work Mode: {job['workMode']}")
        print(f"  Country: {job['country']}")
        
    json_content = {
        "jobs": jobs,
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save updated jobs
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    
    driver.quit()
    
if __name__ == "__main__":
    sync_jobs()
    upload_jobs_to_ftp()