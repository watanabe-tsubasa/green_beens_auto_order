from modules.gb_selenium import AutoOrder
from modules.reader import make_single_order

if __name__ == '__main__':
  
  product_ids, product_counts = make_single_order(
    './data/2023-11-23_type3_test_order.xlsx',
    100
  )
  
  auto_order = AutoOrder(
    address='sample_1',
    id='2',
    date=27,
    time=16,
    timeout=1
  )
  
  auto_order.access()
  auto_order.login()
  not_found_id_list = []
  for id, count in zip(product_ids, product_counts):
    # 12_000円を超えるとエラー出るので、その前に止める
    current_price = auto_order.get_current_price()
    print(current_price)
    if current_price > 10_000:
      break
    try:
      auto_order.add_to_cart(id, count)
    except:
      print(f'{id} not found')
      not_found_id_list.append(id)
  auto_order.set_delivery()
  auto_order.payment()

  auto_order.quit()