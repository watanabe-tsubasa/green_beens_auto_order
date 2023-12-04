import csv

def csv_writer(path, id_list):
  with open(path, 'w', newline='') as file:
    writer = csv.writer(file)
    for id in id_list:
      writer.writerow([id])