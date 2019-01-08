from storages.films_to_csv_writer import FilmsToCsvWriter
from raw_data.best_500 import MOVIES, NAME

if __name__ == '__main__':
    converter = FilmsToCsvWriter('data/best_500.csv')
    converter.write_data(MOVIES, NAME)
