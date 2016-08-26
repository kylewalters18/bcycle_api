import csv


with open('data/subset_2015denverbcycletripdata_public.csv', 'rb') as csvfile:
    trip_data = csv.reader(csvfile, delimiter=',')
    for row in trip_data:
        print ', '.join(row)
