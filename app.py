import time
import logging
from flask import Flask, jsonify, request
from sql import find_uri, update_product
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(filename='web-scraper-app.log', level=logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def initialize():
    return jsonify({'message': str('Web Scraper API')}), 200

@app.post("/product/<id>/fetch-data")
def fetch_data(id):
    # Product data
    product_id = id
    name = None
    sku = None
    brand = None
    price = None
    description = None
    star_rating = None
    review_counter = None
    availability = None

    options = Options()
    options.add_argument("--no-sandbox") # Bypass OS security model
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
    options.add_argument("--window-size=1024x768")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--enable-javascript")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(20)

    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(driver, timeout=2, poll_frequency=.2, ignored_exceptions=errors)

    product = find_uri(id)
    if (product != None):
        driver.get(product['uri'])
        time.sleep(0.5)

        # html = driver.page_source
        # time.sleep(0.3)
        # print(html)
        # logging.info(html)

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='detailInfo']/h1[@class='detailInfo_title']")))
            name_element = driver.find_element(by=By.XPATH, value="//div[@class='detailInfo']/h1[@class='detailInfo_title']")
            if name_element:
                name = name_element.text
                print('Name:', name)
                logging.info(name)
        except NoSuchElementException:
            pass

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'detailInfo_reviewQuestion')]/a[contains(@class, 'detailInfo_reviewsNum')]")))
            review_element = driver.find_element(by=By.XPATH, value="//div[contains(@class, 'detailInfo_reviewQuestion')]/a[contains(@class, 'detailInfo_reviewsNum')]")
            if review_element:
                review_string = review_element.text
                review_number = [int(word) for word in review_string.split() if word.isdigit()]
                review_counter = review_number[0]
                print('Review:', review_counter)
                logging.info(review_counter)
        except NoSuchElementException:
            pass

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'detailPrice')]/strong[contains(@class, 'shopPrice')]/span")))
            price_element = driver.find_element(by=By.XPATH, value="//div[contains(@class, 'detailPrice')]/strong[contains(@class, 'shopPrice')]/span")
            if price_element:
                price = int(price_element.text.replace(',', ''))
                print('Price:', price)
                logging.info(price)
        except NoSuchElementException:
            pass

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'detailStock_wrap')]/span[contains(@class, 'detailStock')]")))
            availability_element = driver.find_element(by=By.XPATH, value="//div[contains(@class, 'detailStock_wrap')]/span[contains(@class, 'detailStock')]")
            if availability_element:
                availability = availability_element.text
                print('availability:', availability)
                logging.info(availability)
        except NoSuchElementException:
            pass

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'detailGuide')]/ul[contains(@class, 'detailGuide_cont')]/li")))
            description_elements = driver.find_elements(by=By.XPATH, value="//div[contains(@class, 'detailGuide')]/ul[contains(@class, 'detailGuide_cont')]/li")
            if description_elements:
                description = ''
                for description_element in description_elements:
                    description += description_element.text.strip()
                print('Description:', description)
                logging.info(description)
        except NoSuchElementException:
            pass

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except (Exception) as error:
            print(error)
            logging.error(error)
        finally:
            driver.quit()
    result = update_product(product_id, name, sku, price, description, star_rating, review_counter, availability)
    return jsonify({'data': result}), 200

if __name__ == '__main__':
    print('Startup')
    # run app in debug mode on port 5001
    app.run(debug=True, port=5001)
