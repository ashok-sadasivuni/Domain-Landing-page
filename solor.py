import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

inout_file = r"C:\IPV6\Test cases(Solor changes).csv"
try:
    df = pd.read_csv(csv_file_path)
# Set up WebDriver once (instead of reinitializing for each domain)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for index, row in df.iterrows():
    domain = row[0]  # Assuming the first column contains the domain URLs

    try:
        driver.get(domain)
        time.sleep(3)  # Allow page to load

        # Click button on the home page
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()
        time.sleep(3)

        # Locate the company dropdown
        company_dropdown = Select(driver.find_element(By.ID, "companyDropdown"))
        companies = company_dropdown.options

        # Print number of companies in dropdown
        print(f"{domain} - Total Companies Found: {len(companies) - 1}")


        for i in range(1, len(companies)):  # Skipping placeholder option
            company_name = companies[i].text
            company_dropdown.select_by_index(i)
            time.sleep(2)

            # Click the search button
            search_button = driver.find_element(By.ID, "searchButton")  # Adjust ID if needed
            search_button.click()
            time.sleep(3)

            # Check job listings
            job_elements = driver.find_elements(By.CLASS_NAME, "job-title")  # Adjust class if needed
            job_titles = [job.text for job in job_elements]

            # Count unique job titles
            unique_job_titles = set(job_titles)
            num_jobs = len(unique_job_titles)

            # Print company name and number of unique job titles
            print(f"Company: {company_name}, Jobs Found: {num_jobs}")

            # Validate job listings (1-5 unique titles)
            if 1 <= num_jobs <= 5:
                print(f"{domain} - {company_name}: ✅ Passed")
            else:
                print(f"{domain} - {company_name}: ❌ Failed (Job listings issue)")

            # Re-locate the dropdown (to avoid stale element error)
            company_dropdown = Select(driver.find_element(By.ID, "companyDropdown"))

    except Exception as e:
        print(f"{domain}: ❌ Error - {e}")

driver.quit()
