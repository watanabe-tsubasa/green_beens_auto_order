from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv; load_dotenv()
import os

from modules.get_resource_path import resource_path

# init
base_url = os.environ.get('RTE_URL')

# access
basic_id = os.environ.get('BASIC_ID')
basic_pass = os.environ.get('BASIC_PASS')
auth_url = f'https://{basic_id}:{basic_pass}@{base_url}'
driver_pass = os.environ.get('DRIVER_PASS')

service = Service(executable_path=resource_path(driver_pass))

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(20)
driver.get(auth_url)

# login
driver.get(f'https://{base_url}/login')

input_id = driver.find_element(By.CLASS_NAME, 'c-input__input')
input_pass = driver.find_element(By.CLASS_NAME, 'c-pwd-input__input')
login_button = driver.find_element(By.CLASS_NAME, 'c-button')

login_id = os.environ.get('ORDER_ID_2')
login_pass = os.environ.get('ORDER_PASS_2')
input_id.send_keys(login_id)
input_pass.send_keys(login_pass)
login_button.click()

# add_cart
product_ids = ['14902705030982', '14902150661885']
product_counts = [3, 2]

for id, count in zip(product_ids, product_counts):
  product_detail_url = f'https://rte.aeon.osp.world/products/{id}/details'
  driver.get(product_detail_url)

  # リカー購入時のチェックを入れる
  add_button = driver.find_element(By.CSS_SELECTOR, 'button[data-synthetics="add-button"]')
  add_button.click()
  counter_input = driver.find_element(By.CSS_SELECTOR, 'input[data-synthetics="quantity-in-basket"]')
  counter_input.send_keys(Keys.BACK_SPACE)
  counter_input.send_keys(str(count))
  counter_input.send_keys(Keys.ENTER)

# purchase


if __name__ == '__main__':
  import time
  
  time.sleep(10)
  driver.quit()