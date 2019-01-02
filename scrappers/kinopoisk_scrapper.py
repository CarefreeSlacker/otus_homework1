import requests
import logging
from urllib import parse
import sys
sys.path.append('../parsers')
from parsers.films_list_parser import FilmsListParser

logger = logging.getLogger("Scrapper")

class KinopoiskScrapper(object):
    def __init__(self, url):
        if (url == ''):
            logger.error('KinopoiskScrapper No url given')
        else:
            parsed_url = parse.urlparse(url)
            self.host_url = '{scheme}://{host}'.format(scheme=parsed_url.scheme, host=parsed_url.netloc)
            self.start_url = url
            self.film_urls = []
            self.films = []

    def perform(self):
        self.__get_film_urls()
        # self.__get_films()
        return self.films

    def __get_film_urls(self):
        parsed_page = self.__get_page(self.start_url)

        if(not parsed_page.has_films_list):
            logger.error('No films on page {0}'.format(self.start_url))
            return False

        while parsed_page.has_next_page():
            self.__get_film_urls_from_page(parsed_page)
            next_page_url = self.__get_next_page_url(parsed_page)
            parsed_page = self.__get_page(next_page_url)
        else:
            self.__get_film_urls_from_page(parsed_page)

        return True



    def __get_next_page_url(self, parsed_page):
        return '{0}{1}'.format(self.host_url, parsed_page.next_page_path())

    def __get_page(self, url):
        text = requests.get(url).text
        return FilmsListParser(text)

    def __get_film_urls_from_page(self, parsed_page):
        self.film_urls += parsed_page.film_paths_list()
        return True

    def __parse_films(self):
        return True
