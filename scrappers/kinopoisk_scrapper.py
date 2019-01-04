import requests
import logging
from urllib import parse
import time
import random
import re
import yaml
from parsers.films_list_parser import FilmsListParser
from parsers.film_parser import FilmParser

logger = logging.getLogger("Scrapper")

class KinopoiskScrapper(object):

    AWAIT_TIME = 10
    REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }

    def __init__(self, url):
        if (url == ''):
            logger.error('KinopoiskScrapper No url given')
        else:
            parsed_url = parse.urlparse(url)
            self.host_url = '{scheme}://{host}'.format(scheme=parsed_url.scheme, host=parsed_url.netloc)
            self.start_url = url
            self.proxies = self.__load_proxies_configuration()
            self.film_urls = []
            self.films = []

    def __load_proxies_configuration(self):
        proxies = []
        with open('proxies.yml', 'r') as stream:
            try:
                for proxy in yaml.load(stream)['proxies']:
                    proxies.append(dict.fromkeys(['http', 'https'], proxy))
            except yaml.YAMLError as exc:
                print(exc)
        return proxies

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
        text = ''
        proxies = self.__get_random_configuration()
        time.sleep(self.AWAIT_TIME)
        attemption = 1
        while True:
            try:
                print('Get and parse page with url: {0} attemption {1}'.format(url, attemption))
                request = requests.get(url, headers=self.REQUEST_HEADERS, proxies=proxies)
                print('RequestResult {0}'.format(request))
                text = request.text
                break
            except:
                proxies = self.__get_random_configuration()
                attemption += 1
                continue

        return parser(text)

    def __get_random_configuration(self):
        return random.choice(self.proxies)

    def __get_film_urls_from_page(self, parsed_page):
        self.film_urls += parsed_page.film_paths_list()
        return True

    def __get_films(self):
        for film_url in self.film_urls:
            url = self.__make_url_from_path(film_url)
            attemption = 1
            while True:
                print('Get film from url: {0}, attemption: {1}'.format(url, attemption))
                parsed_page = self.__get_and_parse_page(url, FilmParser)
                film_data = parsed_page.get_film_data()
                if(film_data):
                    film_data['id'] = re.search('(\d+)', film_url).group(1)
                    print('Film data present: {0}'.format(film_data))
                    self.films.append(film_data)
                    break
                else:
                    print('DDos protection')
                    attemption += 1
                    continue
        return True
