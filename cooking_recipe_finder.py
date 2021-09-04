
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')
driver.get("https://restegourmet.de/rezeptsuche/muss_hauptspeisen/,rocula,gnocchi,tomaten/direkt-loslegen")
timeout = 5
try:
    element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'source-url'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

with open("source.html", 'w') as f:
    f.write(driver.page_source)

links = driver.find_elements_by_class_name("source-url")

for link in links:
    print(link.text)

# links_cleaned = [link.text.replace("Quelle: ", "") for link in links]
# print(links_cleaned)
driver.quit()