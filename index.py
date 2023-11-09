from modules.gb_selenium import AutoOrder
from modules.reader import make_single_order

if __name__ == '__main__':
  import time
  
  product_ids, product_counts = make_single_order('./data/type3_test_order.xlsx', 90)
  
  auto_order = AutoOrder(address='ローソン 稲毛海浜公園店')
  auto_order.access()
  auto_order.login()
  not_found_id_list = []
  for id, count in zip(product_ids, product_counts):
    try:
      auto_order.add_to_cart(id, count)
    except:
      print(f'{id} not found')
      not_found_id_list.append(id)
  # time.sleep(2)
  # time.sleep(60)
  auto_order.purchase()

  auto_order.quit()