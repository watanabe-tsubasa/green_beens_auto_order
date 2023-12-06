from modules.gb_selenium import AutoOrder
from modules.reader import make_single_order
from modules.csv_writer import csv_writer

if __name__ == '__main__':
  
  order_numbers = [
    '392',
    '398',
    '406',
    '409',
    '410',
    '412',
    '413',
    '419',
    '423',
    '425',
    '426',
    '429',
    '430',
    '431',
    '432',
  ] # 変える
  
  id = '1' # 変える
  
  ref_file_name = './data/2023-12-04_type3_test_order.xlsx'
  
  auto_order = AutoOrder(
    # address='sample_4',
    id=id, 
    date=6, # チェックする
    time=15, # チェックする
    timeout=1,
    headless=True
  )
  
  auto_order.access()
  auto_order.login()
  not_found_id_list = []
  waiting_id_list = []
  
  for idx, order_number in enumerate(order_numbers):
    address_count = (idx % 4) + 1
    auto_order.set_address(f'sample_{address_count}')
    product_ids, product_counts = make_single_order(
      ref_file_name,
      order_number
    )
    print(f'===注文開始：{order_number}===')
    for product_id, count in zip(product_ids, product_counts):
      # 12_000円を超えるとエラー出るので、その前に止める
      current_price = auto_order.get_current_price()
      print(current_price)
      if current_price > 9_000:
        break
      try:
        auto_order.add_to_cart(product_id, count)
      except:
        if auto_order.is_not_found():
          print(f'{product_id} not found')
          not_found_id_list.append(product_id)
        else:
          print(f'{product_id} is wating')
          waiting_id_list.append(product_id)
    auto_order.set_delivery()
    auto_order.payment()

  print('すべての注文処理が正常に終了しました')
  auto_order.quit()
  # csv_writer(f'./log/id{id}_not_found.csv', not_found_id_list)
  csv_writer(f'./log/id{id}_waiting.csv', waiting_id_list)