import sys
import os
import time
import logging
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

logging.basicConfig(filename='example.log', level=logging.DEBUG)

def test_selenium_server_available():
    session = requests.Session()
    retry = Retry(connect=10, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    session.get("http://selenium:4444/wd/hub")

test_selenium_server_available()

options = Options()
options.add_argument("--no-sandbox") # Bypass OS security model
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
options.add_argument("--window-size=1024x768")
options.add_argument("--disable-extensions")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    options=options
)
wait = WebDriverWait(driver, 20)

driver.get("https://www.vevor.mx/limpiador-ultrasonico-c_11064/vevor-limpieza-por-ultrasonidos-1-8-2l-limpiador-ultrasonico-40-khz-p_010447073412")
time.sleep(20)

wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='detailInfo']/h1[@class='detailInfo_title']")))
h1_element = driver.find_element(by=By.XPATH, value="//div[@class='detailInfo']/h1[@class='detailInfo_title']")
if h1_element:
    title = h1_element.get_attribute('innerText')
    print(title)
    title_v2 = h1_element.text
    print(title_v2)
    logging.warning(title)  # will print a message to the console
    logging.info(title_v2)  # will not print anything
