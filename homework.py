import logging
import sys

from scrappers.kinopoisk_scrapper import KinopoiskScrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#
# SCRAPPED_FILE = 'scrapped_data.txt'
# TABLE_FORMAT_FILE = 'data.csv'


def gather_process():
    logger.info("gather")
    # storage = FileStorage(SCRAPPED_FILE)

    # You can also pass a storage
    scrapper = KinopoiskScrapper(url=)
    scrapper.scrap_process(storage)


def convert_data_to_table_format():
    logger.info("transform")

    # Your code here
    # transform gathered data from txt file to pandas DataFrame and save as csv
    pass


def stats_of_data():
    logger.info("stats")

    # Your code here
    # Load pandas DataFrame and print to stdout different statistics about the data.
    # Try to think about the data and use not only describe and info.
    # Ask yourself what would you like to know about this data (most frequent word, or something else)


if __name__ == '__main__':
    """
    why main is so...?
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    elif sys.argv[1] == 'stats':
        stats_of_data()

    logger.info("work ended")
