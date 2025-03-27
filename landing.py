import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json


def get_response_code(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def get_og_site_name(driver, url):
    driver.get(url)
    try:
        return driver.find_element(By.XPATH, "//meta[@property='og:site_name']").get_attribute("content")
    except NoSuchElementException:
        print(f" og:site_name not found on {url}")
        return None


def check_for_http_links():
    return False


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://hiringjobsway.com/")
homepage_og_site_name = get_og_site_name(driver)
driver.get(url)
print(f"Homepage og:site_name: {homepage_og_site_name}")
main_window = driver.current_window_handle


try:

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //a[@href='/search' and @rel='nofollow']"))
    )
    driver.execute_script("arguments[0].click();", search_button)

    # Select dropdown
    dropdown = Select(driver.find_element(By.XPATH, "//select[@name='company']"))
    companyOptions = dropdown.options

    for index in range(1, len(companyOptions)):
        try:
            dropdown = Select(driver.find_element(By.XPATH, "//select[@name='company']"))
            dropdown.select_by_index(index)

            search_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@type='submit' or contains(text(),'earch') or contains(text(),'SEARCH')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", search_option)
            driver.execute_script("arguments[0].click();", search_option)


            apply_now_options = driver.find_elements(By.XPATH, "//*[text()='Apply Now' or text()='APPLY NOW']")

            for apply_now_option in apply_now_options[:1]:  # Checking only the first
                job_url = apply_now_option.get_attribute('href')
                modified_url = job_url + "?show=true"

                if get_response_code(modified_url) == 200:
                    driver.execute_script("window.open(arguments[0])", modified_url)


            new_window = [window for window in driver.window_handles if window != driver.current_window_handle][0]
            driver.switch_to.window(new_window)

            try:
                og_url = driver.find_element(By.XPATH, "//meta[@property='og:url']").get_attribute("content")
                print("OG URL:", og_url)

                body = driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.PAGE_DOWN)

                # scroll_up_button = WebDriverWait(driver, 20).until(
                #     EC.element_to_be_clickable((By.XPATH, "//*[@onclick='scrollToTop()']"))

                # driver.execute_script("arguments[0].click();", scroll_up_button)
                # print("Scroll up button clicked.")

                h1_text = driver.find_element(By.TAG_NAME, "h1").text
                if not h1_text:
                    print("Job title doesn't contain h1 tag.")

                canonical_url = driver.find_element(By.XPATH, "//link[@rel='canonical']").get_attribute("href")
                print("Canonical URL:", canonical_url)

                if og_url != job_url:
                    print("Mismatch: og:url and job URL.")
                if canonical_url != job_url:
                    print("Mismatch: canonical URL and job URL.")

                src_image = driver.find_element(By.XPATH, "//img[@src]").get_attribute("src")
                og_image = driver.find_element(By.XPATH, "//meta[@property='og:image']").get_attribute("content")

                if src_image != og_image:
                    print("Image src does not match og:image.")
                    #
                    # def get_og_site_name(driver):
                    #     try:
                    #         og_site_name = driver.find_element(By.XPATH,"//meta[@property='og:site_name']").get_attribute("content")
                    #         return og_site_name.strip() if og_site_name else None
                    #     except NoSuchElementException:
                    #         print("og:site_name meta tag not found.")
                    #         return None


                    landing_page_og_site_name = get_og_site_name(driver)
                    driver.find_element(By.XPATH, "//meta[@property='og:site_name']").get_attribute("content")
                    print(f"Landing Page og:site_name: {landing_page_og_site_name}")

                    # Step 3: Compare the values
                    if homepage_og_site_name and landing_page_og_site_name:
                        if homepage_og_site_name == landing_page_og_site_name:
                            print("og:site_name matches on both homepage and landing page.")
                        else:
                            print(" Mismatch: og:site_name differs between homepage and landing page.")
                    else:
                        print(" Unable to retrieve og:site_name from one or both pages.")

                # try:
                #     expired_message = WebDriverWait(driver, 20).until(
                #         EC.presence_of_element_located(
                #             (By.XPATH, "//*[contains(text(),'expired') or contains(text(),'Expired')]"))
                #     )
                #     print("Job expired message found.")
                # except TimeoutException:
                #     print("No expired job message found.")

                try:
                    copyright_text = driver.find_element(By.XPATH, "//*[contains(text(),'© 2024')]").text
                except NoSuchElementException:
                    print("Copyright element not found.")
                    copyright_text = ""

                if copyright_text:
                    title_after_pipe = driver.title.split("|")[-1].strip()
                    extracted_text = copyright_text.split("2024")[1].split(".")[0].strip()
                    if title_after_pipe == extracted_text:
                        print("Title after | matches copyright text.")

                description_lp_present = driver.find_elements(By.CLASS_NAME, "description-lp")
                print("description-lp presence:", bool(description_lp_present))

                og_locale_present = driver.find_elements(By.XPATH, "//meta[@property='og:locale']")
                print("og:locale meta tag found:", bool(og_locale_present))

                og_type_present = driver.find_elements(By.XPATH, "//meta[@property='og:type' and @content='website']")
                print("og:type meta tag with 'website' found:", bool(og_type_present))


                if check_for_http_links():
                    print("HTTP links found.")
                else:
                    print("No HTTP links found.")

            finally:
                driver.close()
                driver.switch_to.window(main_window)
                time.sleep(1)

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {e}")
        finally:

            try:
                clear_button_list = driver.find_elements(By.XPATH, "//a[contains(text(),'Clear') or contains(text(),'clear')]")
                if clear_button_list:
                    clear_Button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Clear') or contains(text(),'clear')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", clear_Button)
                    driver.execute_script("arguments[0].click();", clear_Button)
                    print("Clear Search button clicked successfully.")
                else:
                    print("Clear Search button NOT found.")
            except TimeoutException:
                print("Timeout: Clear Search button not found.")

except Exception as e:
    print(f"Unexpected error occurred: {e}")

finally:
    driver.quit()

