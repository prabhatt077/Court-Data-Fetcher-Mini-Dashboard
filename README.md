# 🧾 Court-Data Fetcher & Mini-Dashboard

A lightweight Flask web app that allows users to search Delhi High Court case status by selecting 
Case Type, Case Number, and Filing Year. The app fetches metadata, displays latest case info and judgment/order PDFs (if available), and logs queries to a MySQL database.

---
[🎥 Watch Demo Video]([https://www.youtube.com/watch?v=YOUR_VIDEO_ID](https://youtu.be/0j7WWzrmxuk))


## ⚖️ Court Chosen

**✅ Delhi High Court**  
Website: https://delhihighcourt.nic.in/app/get-case-type-status

---

## 🚀 Features

- Simple frontend form to input case details
- Automated browser scraping using Selenium
- Auto-handles CAPTCHA (if code-based, not image-based)
- Parses case table: Parties, Dates, PDFs
- Stores every query + result in MySQL
- Displays all available judgment/order PDF download links

---

## 🧩 Stack & Tech Used

- Python (3.9+)
- Flask
- Selenium
- BeautifulSoup
- MySQL
- HTML + CSS (custom UI)
- Bootstrap Icons / Fonts (optional)


---

## 🧠 CAPTCHA Strategy

The Delhi High Court currently uses a **text-based (non-image)** CAPTCHA on its case status portal.  
We extract the value from the DOM directly:

```python
captcha_value = driver.find_element(By.ID, "captcha-code").text.strip()
driver.find_element(By.ID, "captchaInput").send_keys(captcha_value)
