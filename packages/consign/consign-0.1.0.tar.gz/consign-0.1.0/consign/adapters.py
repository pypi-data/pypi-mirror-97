import csv
import json


class StoreAdapter():
    """
    """

    def __init__(self, method):
        self.method = method


    def store(self, data, url, delimiter):
        if self.method == 'CSV':
            self.to_csv(data, url, delimiter)
        elif self.method == 'JSON':
            self.to_json(data, url)


    def to_csv(self, data, url, delimiter):
        with open(url, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file, delimiter=delimiter)
            for row in data:
                writer.writerow(row)


    def to_json(self, data, url):
        with open(url, 'w') as output_file:
            json.dump(data, output_file)
