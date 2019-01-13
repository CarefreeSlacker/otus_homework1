from storages.films_to_csv_writer import FilmsToCsvWriter
from raw_data.best_500 import MOVIES, NAME


class WriteBestHundreds:

    def __init__(self):
        return

    def perform(self):
        converter = FilmsToCsvWriter('data/best_500.csv')
        converter.write_data(MOVIES, NAME)
        return
