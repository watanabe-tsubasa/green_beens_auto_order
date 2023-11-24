import polars as pl

def make_single_order(path: str, order_num: int):
  num_str = str(order_num)
  df = pl.read_excel(path, sheet_name=num_str)
  id_list = df[f'SKUID'].to_list()
  count_list = df[f'数量'].to_list()
  return (id_list, count_list)

def get_id_name(path: str):
  df = pl.read_csv(path)
  id_list = df[f'SKUID'].to_list()
  name_list = df[f'商品名'].to_list()
  return (id_list, name_list)

if __name__ == '__main__':
  id_list, count_list = make_single_order('./data/231108.csv', 0)
  print(id_list)
  print(count_list)