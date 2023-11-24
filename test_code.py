from modules.gb_selenium import AutoOrder
from modules.reader import get_id_name

if __name__ == '__main__':
  import csv
  
  product_ids, product_names = get_id_name('./data/231113_3000.csv')
  
  auto_order = AutoOrder(address='sample_1', id='0')
  auto_order.access()
  auto_order.login()
  not_found_id_list = []
  not_found_product_name = []
  waiting_id_list = []
  waiting_product_name =[]
  
  for id, name in zip(product_ids, product_names):
    try:
      auto_order.add_to_cart(id, 0)
    except:
      if auto_order.is_not_found():
        print(f'{id} not found')
        not_found_id_list.append(id)
        not_found_product_name.append(name)
      else:
        print(f'{id} is wating')
        waiting_id_list.append(id)
        waiting_product_name.append(name)

  auto_order.quit()
  
  with open('./not_found.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for id, name in zip(not_found_id_list, not_found_product_name):
        writer.writerow(id, name)

  with open('./waiting.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for id, name in zip(waiting_id_list, waiting_product_name):
        writer.writerow(id, name)