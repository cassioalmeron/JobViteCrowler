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
    options = webdriver.ChromeOptions()
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
                job_titles.append({"jobvite_id": jobvite_id, "job_title": job_title})
        
        return job_titles
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
        
def get_job_description(driver, jobvite_id) -> str:
    driver.get(f"https://jobs.jobvite.com/leantechio/job/{jobvite_id}")
    
    wait = WebDriverWait(driver, 10)
    
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jv-job-detail-description")))
        
        #job_title = driver.find_element(By.CLASS_NAME, "jv-job-details-title").text
        job_description = driver.find_element(By.CLASS_NAME, "jv-job-detail-description").get_attribute("innerHTML")
        
        return job_description
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {}
    
def sync_jobs():
    """Sync jobs from website and save to JSON file"""
    driver = get_driver()
    
    jobs = get_jobs(driver)
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print("Created new jobs.json file")
    
    # Update job descriptions
    for job in jobs:
        jobvite_id = job["jobvite_id"]
        print(jobvite_id, job["job_title"])
        job_description = get_job_description(driver, jobvite_id)
        job["job_description"] = job_description
        
    json_content = {
        "jobs": jobs,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save updated jobs
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    
    driver.quit()
    
if __name__ == "__main__":
    sync_jobs()
    upload_jobs_to_ftp()