print("start")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from db_mysql import log_to_mysql
import time


def scrape_delhi_high_court(case_type, case_number, filing_year):
    url = "https://delhihighcourt.nic.in/app/get-case-type-status"

    # Setup WebDriver
    service = Service(executable_path="C:/chromedriver/chromedriver.exe")  # Adjust path if needed
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Wait until form loads
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "case_type"))
        )

        # Fill the form
        Select(driver.find_element(By.NAME, "case_type")).select_by_value(case_type)
        driver.find_element(By.NAME, "case_number").send_keys(case_number)
        Select(driver.find_element(By.NAME, "case_year")).select_by_value(filing_year)

        # Auto-fill CAPTCHA
        captcha_value = driver.find_element(By.ID, "captcha-code").text.strip()
        driver.find_element(By.ID, "captchaInput").send_keys(captcha_value)

        # Submit the form
        time.sleep(2)
        driver.find_element(By.ID, "search").click()
        time.sleep(2)
        # Wait for results table
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "caseTable"))
        )

        # Parse results with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(driver.page_source, "html.parser")

        table = soup.find("table", {"id": "caseTable"})
        rows = table.find("tbody").find_all("tr")

        if not rows:
            return "No data found for this case."

        data = []
        for row in rows:
            cols = [td.text.strip() for td in row.find_all("td")]
            data.append(cols)
        #print(data)



        driver.execute_script("arguments[0].click();", driver.find_elements(By.XPATH, "//table[@id='caseTable']//a[normalize-space()='Orders']")[0])
        time.sleep(2)
        # Find all <a> tags with href containing '.pdf'
        pdf_links = []

        rows = driver.find_elements(By.XPATH, "//table[@id='caseTable']//tbody/tr")
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) >= 3:
                link_elem = tds[1].find_element(By.TAG_NAME, "a")
                pdf_links.append({
                    "text": link_elem.text.strip(),
                    "link": link_elem.get_attribute("href"),
                    "date": tds[2].text.strip()
                })

        # Example print

            #print(f"{item['text']} → {item['link']}")

        # ✅ Log to MySQL
        log_to_mysql(case_type=case_type,
                     case_number=case_number,
                     filing_year=filing_year,
                     html_response=html,
                     result_summary=str(data))
        print('Loaded in mysql ')

        return data,pdf_links


    except Exception as e:
        print("❌ Error occurred. Saved HTML to result.html for debugging.")
        with open("result.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise ValueError("❗ Could not parse result. Maybe the case number is invalid or the site layout changed.") from e

    finally:

        time.sleep(3)
        driver.quit()
#result,pdf_links=scrape_delhi_high_court('W.P.(C)', '8531', '2022')
#print(result)
#print(pdf_links)
