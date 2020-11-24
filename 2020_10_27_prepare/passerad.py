import csv

f = open('passenger_counts.csv',mode='r',encoding='utf-8-sig')
csv_reader = csv.reader(f)
rows = [i for i in csv_reader]
airport_dict = {}
for row in rows[1:]:
    if row[0] not in airport_dict and row[1] == '2016':
        airport_dict[row[0]] = 0
for row in rows[1:]:
    if  row[1] == '2016':
        airport_dict[row[0]] += int(row[3]) - int(row[4])
for key,value in airport_dict.items():
    print('{} : {}'.format(key,value))