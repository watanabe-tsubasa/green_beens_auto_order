from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
from datetime import datetime
import os
import random
import time

# Assuming get_resource_path function is defined elsewhere
from modules.get_resource_path import resource_path

load_dotenv()

class AutoOrder(webdriver.Chrome):
  
  def __init__(
    self,
    address: str='sample_1',
    id:str='0',
    date:int=None,
    time:str=13,
    timeout=10,
    headless=True
  ):
    self.base_url = os.environ.get('RTE_URL')
    self.id = id
    self.address_name = address
    self.current_date = datetime.now().day
    self.headless = headless
    if date is None:
      self.date = self.current_date
    else:
      self.date = date
    self.time = time
    
    driver_path = os.environ.get('DRIVER_PASS')
    service = Service(executable_path=resource_path(driver_path))
    options  = Options()
    options.add_argument('--blink-settings=imagesEnabled=false')
    if self.headless:
      options.add_argument('--headless')

    super().__init__(service=service, options=options)
    self.implicitly_wait(timeout)

  def access(self):
    basic_id = os.environ.get('BASIC_ID')
    basic_pass = os.environ.get('BASIC_PASS')
    auth_url = f'https://{basic_id}:{basic_pass}@{self.base_url}'
    self.get(auth_url)
    self.get(f'https://{self.base_url}/login')

  def login(self):
    try:
      input_id = self.find_element(By.CLASS_NAME, 'c-input__input')
      input_pass = self.find_element(By.CLASS_NAME, 'c-pwd-input__input')
      login_button = self.find_element(By.CLASS_NAME, 'c-button')

      login_id = os.environ.get(f'ORDER_ID_{self.id}')
      login_pass = os.environ.get(f'ORDER_PASS_{self.id}')
      input_id.send_keys(login_id)
      input_pass.send_keys(login_pass)
      login_button.click()
    except:
      print('usual login process was skipped')

  def add_to_cart(self, id: str, count: int | str):
    product_detail_url = f'https://{self.base_url}/products/{id}/details'
    self.get(product_detail_url)

    add_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="add-button"]')
    add_button.click()
    counter_input = self.find_element(By.CSS_SELECTOR, 'input[data-synthetics="quantity-in-basket"]')
    counter_input.send_keys(Keys.BACK_SPACE)
    counter_input.send_keys(str(count))
    counter_input.send_keys(Keys.ENTER)

  def set_delivery(self):
    self.get(f'https://{self.base_url}/delivery/home')
    try:
      self.login()
    except:
      print('auto_login_failed')
    self.get(f'https://{self.base_url}/delivery/home')
    time.sleep(15)
    while True:
      try:
        delivery_address_button = self.find_element(By.CSS_SELECTOR, f'button[aria-label="{self.address_name}へ配送"]')
        delivery_address_button.click()
        break
      except:
        try:
          print('欠品例外処理に入りました')
          modal = self.find_element(By.CSS_SELECTOR, 'div[aria-labelledby="basket-merge-conflict-modal-header-label"]')
          cart_confirm_button = modal.find_element(By.CSS_SELECTOR, 'button[type="button"]')
          cart_confirm_button.click()
          basket_checkout_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="start-checkout-button"]')
          basket_checkout_button.click()
          delivery_start_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="delivery-method-van"]')
          delivery_start_button.click()
          try:
            delivery_address_button = self.find_element(By.CSS_SELECTOR, f'button[aria-label="{self.address_name}へ配送"]')
            delivery_address_button.click()
            break
          except:
            break
        except:
          try:
            print('直接操作します')
            set_time_link = self.find_element(By.CSS_SELECTOR, 'a[data-test="delivery-book-delivery-button"]')
            set_time_link.click()
            delivery_start_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="delivery-method-van"]')
            delivery_start_button.click()
          except:
            print('デリバリー選択を再試行します')
    
    count = 0    
    while count < 10:
      diff_date = self.date - self.current_date
      if diff_date > 2 :
        try:
          for _ in range (diff_date - 2):            
            next_day_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="select-next"]')
            next_day_button.click()
        except:
          print('翌日ボタンをクリックできませんでした')
      try:
        try:
          time_button = self.find_element(By.XPATH, f"//button[contains(@aria-label, '{str(self.date)}日') and contains(@aria-label, '{str(self.time)}時00分 - {str(self.time+1)}時00分')]")
        except:
          time_button = self.find_element(By.XPATH, f"//button[contains(@aria-label, '{str(self.date)}日') and contains(@aria-label, '{str(self.time+1)}時00分 - {str(self.time+2)}時00分')]")
        # JS効いているっぽいので直接JSを実行
        # time_button.click()
        self.execute_script("arguments[0].click();", time_button)
        break
      except:
        count += 1
        print(f'時間選択に失敗しました:{count}')
        if count == 10:
          print('時間選択に10回失敗しました。ルートを追加してください')
  
  def payment(self):
    while True:
      try:
        confirm_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="confirm-slot"]')
        confirm_button.click()
        break
      except Exception as e:
        print(f'欠品例外:{e}')
    while True:
      try:
        go_to_payment = self.find_element(By.CSS_SELECTOR, 'a[data-test="checkout-walk-crumbs-link"]')
        print('find go to payment')
        # go_to_payment.click()
        self.execute_script("arguments[0].click();", go_to_payment)
        break
      except Exception as e:
        print(e)
        try:
          cart_button = self.find_element(By.CSS_SELECTOR, 'button[data-test="basket-button"]')
          self.execute_script("arguments[0].click();", cart_button)
          # cart_button.click()
          start_checkout_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="start-checkout-button"]')
          self.execute_script("arguments[0].click();", start_checkout_button)
          # start_checkout_button.click()
        except Exception as e:
          print(f'予期せぬエラーです{e}')
        try: 
          go_to_payment = self.find_element(By.CSS_SELECTOR, 'a[data-test="checkout-walk-crumbs-link"]')
          print('find go to payment')
          go_to_payment.click()
          # self.execute_script("arguments[0].click();", go_to_payment)
          break
        except Exception as e:
          print(f'{e}')
          try:
            add_buttons = self.find_elements(By.CSS_SELECTOR, 'button[data-synthetics="add-button"]')
            random.choice(add_buttons).click()
          except:
            print(e)
        
    while True:
      is_finished = self.is_finished_order()
      if is_finished:
        # self.quit()
        print('決済処理に成功しました。次の注文に進みます')
        break
      else:
        print('注文終了を確認できていないので修了処理を開始します')

      try:
        age_confirm_box = self.find_element(By.CSS_SELECTOR, 'input[data-test="summary-age-confirmation-checkbox"]')
        age_confirm_box.click()
      except:
        print('年齢確認省略')
      try:      
        place_order_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="place-order-button"]')
        place_order_button.click()
      except:
        print('既に決済画面に移動しています')

      try:        
        checkout_frame = self.find_element(By.CSS_SELECTOR, 'iframe[data-test="3ds-iframe"]')
        print('iframe found')
        self.switch_to.frame(checkout_frame)
        print('switch frame')
        checkout_submit_button = self.find_element(By.ID, 'primer-checkout-submit-button')
        print('found submit button')
        self.execute_script("arguments[0].click();", checkout_submit_button)               
      except:
        print('決済過程でエラーが発生しました')
        self.switch_to.default_content()
        print('switch to default')
        
  def is_not_found(self):
    try:
      _ = self.find_element(By.XPATH, "//span[text()='ページが見つかりません。']")
      return True
    except:
      return False
    
  def is_finished_order(self):
    try:
      _ = self.find_element(By.XPATH, "//h1[text()='ご注文を受け付けいたしました']")
      return True
    except:
      return False
    
  def get_current_price(self):
    while True:
      try:
        current_price_str = self.find_element(By.CSS_SELECTOR, 'span[data-test="basket-price"]').text
        print('success to get price')
        current_price = int(current_price_str.replace('￥', '').replace(',', ''))
        return current_price
      except Exception as e :
        print(e)
        
  def set_address(self, address: str):
    self.address_name = address