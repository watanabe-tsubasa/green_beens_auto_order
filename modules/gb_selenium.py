from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os
import time

# Assuming get_resource_path function is defined elsewhere
from modules.get_resource_path import resource_path

load_dotenv()

class AutoOrder(webdriver.Chrome):
  
  def __init__(self, timeout=20):
    self.base_url = os.environ.get('RTE_URL')
    self.address_name = '新小岩'
    
    driver_path = os.environ.get('DRIVER_PASS')
    service = Service(executable_path=resource_path(driver_path))
    
    super().__init__(service=service)
    self.implicitly_wait(timeout)

  def access(self):
    basic_id = os.environ.get('BASIC_ID')
    basic_pass = os.environ.get('BASIC_PASS')
    auth_url = f'https://{basic_id}:{basic_pass}@{self.base_url}'
    self.get(auth_url)
    self.get(f'https://{self.base_url}/login')

  def login(self):
    input_id = self.find_element(By.CLASS_NAME, 'c-input__input')
    input_pass = self.find_element(By.CLASS_NAME, 'c-pwd-input__input')
    login_button = self.find_element(By.CLASS_NAME, 'c-button')

    login_id = os.environ.get('ORDER_ID_2')
    login_pass = os.environ.get('ORDER_PASS_2')
    input_id.send_keys(login_id)
    input_pass.send_keys(login_pass)
    login_button.click()

  def add_to_cart(self, id: str, count: int):
    product_detail_url = f'https://{self.base_url}/products/{id}/details'
    self.get(product_detail_url)

    add_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="add-button"]')
    add_button.click()
    counter_input = self.find_element(By.CSS_SELECTOR, 'input[data-synthetics="quantity-in-basket"]')
    counter_input.send_keys(Keys.BACK_SPACE)
    counter_input.send_keys(str(count))
    counter_input.send_keys(Keys.ENTER)

  def purchase(self):
    self.get(f'https://{self.base_url}/delivery/home?in-checkout-walk=true')
    self.login()
    delivery_address_button = self.find_element(By.CSS_SELECTOR, f'button[aria-label="{self.address_name}へ配送"]')
    delivery_address_button.click()
    # 10時00分 - 11時00分の時間帯の最初のボタンを探す
    # 14時00分 - 15時00分を含むaria-label属性を持つtime要素を探す
    time_xpath = "//time[contains(@aria-label, '14時00分 - 15時00分')]/ancestor::button[@data-synthetics='selectable-slot']"

    # 要素を取得
    time_button = self.find_element(By.XPATH, time_xpath)

    # ボタンをクリックする
    # time_button.click()
    self.execute_script("arguments[0].click();", time_button)
    
    confirm_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="confirm-slot"]')
    confirm_button.click()
    next_step_button = self.find_element(By.CSS_SELECTOR, 'a[data-synthetics="next-step"]')
    next_step_button.click()
    place_order_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="place-order-button"]')
    place_order_button.click()
    
    time.sleep(20)
    checkout_frame = self.find_element(By.CSS_SELECTOR, 'iframe[data-test="3ds-iframe"]')
    self.switch_to.frame(checkout_frame)
    checkout_submit_button = self.find_element(By.ID, 'primer-checkout-submit-button')
    checkout_submit_button.click()
    # self.execute_script("arguments[0].click();", checkout_submit_button)
