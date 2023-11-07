from modules.gb_selenium import AutoOrder

if __name__ == '__main__':
  import time
  product_ids = ['14902705030982', '14902150661885']
  product_counts = [30, 20]

  auto_order = AutoOrder()
  auto_order.access()
  auto_order.login()
  for id, count in zip(product_ids, product_counts):
    auto_order.add_to_cart(id, count)
  auto_order.purchase()
  
  time.sleep(20)
  auto_order.quit()