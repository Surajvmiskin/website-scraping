
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time


def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def scrape_project_details(driver, url):
    driver.get(url)
    project_details = []
    try:
        wait = WebDriverWait(driver, 30)
        for i in range(1, 7):  # Loop from 1 to 6
            xpath = f'//*[@id="reg-Projects"]/div/div/div[{i}]/div/div/a'
            rera_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            rera_link.click()
            # Ensure the GSTIN number element is visible
            gstin_xpath = '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[13]/td[2]/span'
            gstin_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, gstin_xpath)))
            gstin = gstin_element.text if gstin_element else 'Not Available'

            pan_xpath = '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[6]/td[2]/span'
            pan_element = driver.find_element(By.XPATH, pan_xpath)
            pan = pan_element.text if pan_element else 'Not Available'

            name_xpath = '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[1]'
            name_element = driver.find_element(By.XPATH, name_xpath)
            name = name_element.text if name_element else 'Not Available'

            address_xpath = '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody/tr[12]'
            address_element = driver.find_element(By.XPATH, address_xpath)
            address = address_element.text.replace(
                'Correspondence Address', '').strip() if address_element else 'Not Available'

            project_details.append({
                'GSTIN No': gstin,
                'PAN No': pan,
                'Name': name,
                'Permanent Address': address
            })
            # Close the modal
            close_button = driver.find_element(By.CSS_SELECTOR, 'button.close')
            close_button.click()
            wait.until(EC.invisibility_of_element(close_button))
            time.sleep(1)  # Additional buffer to ensure the modal has closed
    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred: {e}")
    return project_details


def main():
    driver = setup_driver()
    url = 'https://hprera.nic.in/PublicDashboard'
    data = scrape_project_details(driver, url)
    driver.quit()
    df = pd.DataFrame(data)
    df.to_excel('project_details.xlsx', index=False)
    print("Data scraped and saved to Excel.")


if __name__ == "__main__":
    main()
