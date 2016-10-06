import csv
from random import random

# line count from wc
total_entries = 363003
desired_num_results = 1000

chances_selected = desired_num_results / total_entries

with open('data/cleaned_data.csv', 'r') as input_file:
    reader = csv.reader(input_file, delimiter=',')

    sample = []
    for line in reader:
        if random() < chances_selected:
            sample.append(line)

    with open("data/subset.csv", "w") as output_file:
        writer = csv.writer(output_file)
        labels = ['users_program', 'user_id', 'zip', 'membership_type',
                  'bike', 'checkout_date', 'checkout_time', 'checkout_kiosk',
                  'return_date', 'return_time', 'return_kiosk', 'duration_minutes']
        writer.writerow(labels)
        writer.writerows(sample)
