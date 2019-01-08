import csv
from converters.film_to_csv_converter import FilmToCsvConverter

class FilmsToCsvWriter:
    FIELDS = ['id', 'reward', 'name', 'country', 'budget', 'fees', 'kinopoisk_rating', 'imdb_rating']

    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        raise NotImplementedError

    def write_data(self, data, reward):
        with open(self.file_name, mode='w') as csv_file:
            writer = self.__make_writer(csv_file)
            writer.writeheader()
            self.__write_data(writer, data, reward)
        return 'Data to {0} written successfully'.format(self.file_name)

    def append_data(self, data, reward):
        with open(self.file_name, mode='a') as csv_file:
            writer = self.__make_writer(csv_file)
            self.__write_data(writer, data, reward)
        return 'Data to {0} append successfully'.format(self.file_name)

    def __write_data(self, writer, data, reward):
        for data_row in data:
            write_data = FilmToCsvConverter(data_row).perform()
            write_data['reward'] = reward
            writer.writerow(write_data)

    def __make_writer(self, csv_file):
        return csv.DictWriter(csv_file, fieldnames=self.FIELDS, delimiter=';')
