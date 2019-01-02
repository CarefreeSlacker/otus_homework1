import requests
import logging
from urllib import parse
import time
import sys
import random
sys.path.append('../parsers')
from parsers.films_list_parser import FilmsListParser
from parsers.film_parser import FilmParser

logger = logging.getLogger("Scrapper")

AWAIT_TIMES = [10, 12, 15]
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' , 'Cookie' : 'PHPSESSID=2hqthies1uiaunsnk4nt8h1lc3; user_country=ru; yandex_gid=213; tc=1; mobile=no; _csrf_csrf_token=5VrUPPMW74qZDZ_lsxjPH97RaLX7gRD2AMYzVIFRF8A; i=GH7we4fxcA+1dglD89EeBgnvh3NsVhD+Q2JYW4kOd9f0BCcS9FYH+JInJvOtWqSsN1T3HcHub8BQTU8KTPKw5F/KKto=; rheftjdd=rheftjddVal; noflash=true; desktop_session_key=8ce3476e00b8e2c9b22a8f2830d23b72470d7c4c9ea0b57bfdb2397fa97f4055663cd90f48c058d8bcb844c0a9b1631aab59e69815c917d2bbaba0c08ecce62e4fd6132891f6e9a29ff68afa21e72ee25e01b047a6dbf82dffd317cbada7fe52; desktop_session_key.sig=tzWdGwTar4Dqpd7bmruXWA7WMko; _ym_uid=1546449812312286617; _ym_d=1546449812; mda=0; yandex_plus_metrika_cookie=true; yandexuid=309105971546449811; refresh_yandexuid=309105971546449811; _ym_isad=2; _ym_visorc_22663942=b'}

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
        self.__get_films()
        return self.films

    def __get_film_urls(self):
        parsed_page = self.__get_and_parse_page(self.start_url, FilmsListParser)

        if(not parsed_page.has_films_list):
            logger.error('No films on page {0}'.format(self.start_url))
            return False

        while parsed_page.has_next_page():
            time.sleep(self.__get_random_await_time())
            self.__get_film_urls_from_page(parsed_page)
            next_page_url = self.__make_url_from_path(parsed_page.next_page_path())
            print('check another page {0}'.format(next_page_url))
            parsed_page = self.__get_and_parse_page(next_page_url, FilmsListParser)
        else:
            self.__get_film_urls_from_page(parsed_page)

        return True

    def __make_url_from_path(self, path):
        return '{0}{1}'.format(self.host_url, path)

    def __get_and_parse_page(self, url, parser):
        text = requests.get(url, headers=headers).text
        return parser(text)

    def __get_film_urls_from_page(self, parsed_page):
        self.film_urls += parsed_page.film_paths_list()
        return True

    def __get_films(self):
        for film_url in self.film_urls:
            time.sleep(self.__get_random_await_time())
            url = self.__make_url_from_path(film_url)
            parsed_page = self.__get_and_parse_page(url, FilmParser)
            self.films += parsed_page.get_film_data()
        return True

    def __get_random_await_time(self):
        return random.choice(AWAIT_TIMES)
