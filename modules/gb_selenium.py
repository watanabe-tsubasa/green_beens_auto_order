from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException


from dotenv import load_dotenv
import os
import time

# Assuming get_resource_path function is defined elsewhere
from modules.get_resource_path import resource_path

load_dotenv()

class AutoOrder(webdriver.Chrome):
  
  def __init__(self, address: str='新小岩', timeout=10):
    self.base_url = os.environ.get('RTE_URL')
    self.address_name = address
    
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
    try:
      input_id = self.find_element(By.CLASS_NAME, 'c-input__input')
      input_pass = self.find_element(By.CLASS_NAME, 'c-pwd-input__input')
      login_button = self.find_element(By.CLASS_NAME, 'c-button')

      login_id = os.environ.get('ORDER_ID_2')
      login_pass = os.environ.get('ORDER_PASS_2')
      input_id.send_keys(login_id)
      input_pass.send_keys(login_pass)
      login_button.click()
    except:
      print('usual login process was skipped')
    
    try:
      i = 0
      while i < 3:
        try:
          temp_button = self.find_element(By.CSS_SELECTOR, 'button[class="c-button c-button--primary"]')
          temp_button.click()
          # self.execute_script("arguments[0].click();", temp_button)
          print('success click')
          break
        except NoSuchElementException:
          print(f'attempt {i}')
        i += 1
      time.sleep(0.5)
      
      # i = 0
      # while i < 4:
      #   try:
      #     temp_submit_button = self.find_element(By.CSS_SELECTOR, 'div.c-buttoncontainer button[type="submit"]')
      #     if i == 3:
      #       self.execute_script("arguments[0].click();", temp_submit_button)
      #       break
      #     temp_submit_button.click()
      #     print('success confirm')
      #     break
      #   except NoSuchElementException:
      #       print(f'Submit button not found, attempt {i}')
      #   except ElementClickInterceptedException:
      #       print(f'Submit button was intercepted, attempt {i}')
      #   except ElementNotInteractableException:
      #       print(f'Submit button not interactable, attempt {i}')
     
      # wait = WebDriverWait(self, 10)  # 10秒間待つ設定
      # try:
      #     # クリック可能になるまで待つ
      #     temp_submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.c-buttoncontainer button[type="submit"]')))
      #     temp_submit_button.click()
      #     print('Submit button clicked')
      # except TimeoutException:
      #     # 10秒経過してもクリック可能にならない場合はJavaScriptを使用
      #     temp_submit_button = self.find_element(By.CSS_SELECTOR, 'div.c-buttoncontainer button[type="submit"]')
      #     self.execute_script("arguments[0].click();", temp_submit_button)
      #     print('Submit button clicked with JavaScript')
      #     i += 1
      
      try:
        action = ActionChains(self)
        submit_button = self.find_element(By.CSS_SELECTOR, 'div.c-buttoncontainer button[type="submit"]')
        action.move_to_element(submit_button).perform()

        # ホバー後にクリック
        submit_button.click()
        print('Submit button clicked after hover')
      except:
        print('それではダメみたい')
      
    except Exception as e:
      print(f'An error occurred: {e}')
    finally:
      print('finish')

  def add_to_cart(self, id: str, count: int | str):
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
    try:
      self.login()
    except:
      print('auto_login_failed')
    
    time.sleep(15)
    while True:
      try:
        delivery_address_button = self.find_element(By.CSS_SELECTOR, f'button[aria-label="{self.address_name}へ配送"]')
        delivery_address_button.click()
        break
      except:
        print('欠品例外が発生したので、欠品例外を実装してください')
        modal = self.find_element(By.CSS_SELECTOR, 'div[aria-labelledby="basket-merge-conflict-modal-header-label"]')
        cart_confirm_button = modal.find_element(By.CSS_SELECTOR, 'button[type="button"]')
        cart_confirm_button.click()
        basket_checkout_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="start-checkout-button"]')
        basket_checkout_button.click()
        delivery_start_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="delivery-method-van"]')
        delivery_start_button.click()
        
    # 10時00分 - 11時00分の時間帯の最初のボタンを探す
    # 14時00分 - 15時00分を含むaria-label属性を持つtime要素を探す
    
    try:
      time_button = self.find_element(By.XPATH, "//time[contains(@aria-label, '12時00分 - 13時00分')]/ancestor::button[@data-synthetics='selectable-slot']")      
    except:
      time_button = self.find_element(By.XPATH, "//time[contains(@aria-label, '13時00分 - 14時00分')]/ancestor::button[@data-synthetics='selectable-slot']")      
    # JS効いているっぽいので直接JSを実行
    # time_button.click()
    self.execute_script("arguments[0].click();", time_button)
    
    while True:
      try:
        confirm_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="confirm-slot"]')
        confirm_button.click()
        next_step_button = self.find_element(By.CSS_SELECTOR, 'a[data-synthetics="next-step"]')
        next_step_button.click()
        break
      except:
        print('欠品例外が発生したので、欠品例外を実装してください')
    
    try:
      age_confirm_box = self.find_element(By.CSS_SELECTOR, 'input[data-test="summary-age-confirmation-checkbox"]')
      age_confirm_box.click()
    except:
      print('年齢確認省略')
    place_order_button = self.find_element(By.CSS_SELECTOR, 'button[data-synthetics="place-order-button"]')
    place_order_button.click()
    
    time.sleep(30)
    try:
      checkout_frame = self.find_element(By.CSS_SELECTOR, 'iframe[data-test="3ds-iframe"]')
      self.switch_to.frame(checkout_frame)
      checkout_submit_button = self.find_element(By.ID, 'primer-checkout-submit-button')
      checkout_submit_button.click()
      # self.execute_script("arguments[0].click();", checkout_submit_button)
    except:
      self.quit()