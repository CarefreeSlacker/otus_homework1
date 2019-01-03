import requests
import logging
from urllib import parse
import time
import random
from parsers.films_list_parser import FilmsListParser
from parsers.film_parser import FilmParser

logger = logging.getLogger("Scrapper")

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' , 'Cookie' : 'PHPSESSID=mdh8n5485r08luejmu4m4bm1m3; user_country=ru; yandex_gid=213; tc=1; mobile=no; _csrf_csrf_token=ounytzr6DTxDwrK1wmcyn4sqsh19Xuzg1YFODvT5DYs; i=k78a0k/Zrljiv8pyl5lMEB5OPiHRInmX9XYYgjv+m92ysYVrjJuNCA0sPNqC1l8l7T8586mQTehttgw05gZXyXS2FQ0=; rheftjdd=rheftjddVal; noflash=true; desktop_session_key=fa987128f9fca6fe56249c077e5fa4d2f3b951e799c9544f7ff41aa0ee3b0bf3f70657f62a211c1209fa1d29df3f2fe98c7892e937123b2b269803a1695b410319ee5c526402501d197df3c8add9f778c4302c375b2806a8947088473e0ec9da; desktop_session_key.sig=sbl72CUbFUYGMeebX4fJzyUzjrI; _ym_uid=1546508359505029845; _ym_d=1546508359; mda=0; yandex_plus_metrika_cookie=true; yandexuid=7701103071546508358; refresh_yandexuid=7701103071546508358; _ym_isad=2; _ym_visorc_22663942=b; watch-online-banner-hidden=1; my_perpages=%5B%5D'}

class KinopoiskScrapper(object):

    AWAIT_TIME = 2
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    PROXIES = [
        'http://46.188.82.57:38108',
        'http://81.198.119.241:42126',
        'http://177.234.2.58:54782',
        'http://62.174.66.61:48870',
        'http://80.90.88.147:44547',
        'http://212.3.210.61:38445',
        'http://46.252.41.155:53281',
        'http://82.114.68.58:46451',
        'http://181.209.78.38:45318',
        'http://190.210.15.194:32302',
        'http://202.136.89.150:46413',
        'http://202.5.42.133:35082',
        'http://181.115.168.69:61385',
        'http://191.5.177.84:30723',
        'http://189.81.185.92:8080',
        'http://186.225.220.154:50770',
        'http://177.85.117.189:38885',
        'http://177.46.147.94:30588',
        'http://201.27.31.184:46626',
        'http://177.53.8.103:39272',
        'http://200.236.216.205:34064',
        'http://87.252.252.169:58896',
        'http://86.57.177.8:57784',
        'http://69.70.25.172:31881',
        'http://200.58.223.146:36287',
        'http://190.25.45.134:41766',
        'http://31.209.104.52:32051',
        'http://77.48.246.20:51504',
        'http://193.86.25.202:49353',
        'http://62.174.66.61:48870',
        'http://190.149.216.74:51363',
        'http://138.59.178.154:35675',
        'http://195.228.173.245:21231',
        'http://202.93.113.4:31821',
        'http://203.77.252.250:31988',
        'http://203.153.108.237:52089',
        'http://27.50.18.42:23500',
        'http://202.52.12.221:34337',
        'http://123.231.244.141:45609',
        'http://36.66.149.42:61773',
        'http://45.116.158.37:43445',
        'http://36.255.158.62:61669',
        'http://14.141.173.171:50187',
        'http://95.170.208.42:8080',
        'http://62.201.253.42:47695',
        'http://31.47.55.66:46591',
        'http://84.38.96.169:49795',
        'http://91.231.27.60:8080',
        'http://77.252.41.56:61689',
        'http://37.98.217.138:45265',
        'http://77.252.26.69:35376',
        'http://95.31.252.16:36250',
        'http://31.135.241.124:37716',
        'http://185.15.90.82:61870',
        'http://195.144.219.155:54857',
        'http://95.181.58.170:30383',
        'http://85.15.189.121:46366',
        'http://128.74.175.248:36207',
        'http://93.80.226.165:4550',
        'http://5.167.54.233:31438',
        'http://81.163.65.51:30416',
        'http://176.192.65.34:33940',
        'http://195.190.100.90:34640',
        'http://5.140.164.173:60011',
        'http://94.232.11.178:53960',
        'http://188.235.2.218:59647',
        'http://128.0.25.161:61281',
        'http://79.120.32.114:52107',
        'http://94.41.92.22:61485',
        'http://95.181.37.114:52617',
        'http://171.25.164.123:32385',
        'http://83.171.99.160:43269',
        'http://95.31.1.50:53847',
        'http://217.76.47.29:34944',
        'http://88.87.85.220:51602',
        'http://178.219.157.187:43354',
        'http://176.101.89.226:33470',
        'http://109.174.98.138:3128',
        'http://195.69.218.198:39832',
        'http://158.58.130.222:53281',
        'http://109.68.187.21:3128',
        'http://85.174.227.52:59280',
        'http://84.52.79.166:43548',
        'http://109.167.224.198:51919',
        'http://213.115.49.165:60727',
        'http://80.68.121.217:32271',
        'http://5.178.58.113:54533',
        'http://85.109.140.178:31326',
        'http://85.99.100.37:46517',
        'http://85.98.95.59:59470',
        'http://93.175.198.138:38401',
        'http://217.12.198.34:32863',
        'http://31.202.197.10:41258',
        'http://213.160.150.239:56637',
        'http://31.41.68.118:61280',
        'http://37.25.3.253:35512',
        'http://46.219.14.37:41063',
        'http://109.237.92.86:34432',
        'http://185.46.223.198:23500',
        'http://77.122.66.215:51656',
        'http://91.225.226.39:58550',
        'http://77.121.71.55:51679',
        'http://176.98.75.143:55458',
        'http://91.214.128.243:23500',
        'http://91.218.47.128:8080'
    ]
    RESOURCE_URL = 'https://kinopoisk.ru'

    def __init__(self, url):
        if (url == ''):
            logger.error('KinopoiskScrapper No url given')
        else:
            parsed_url = parse.urlparse(url)
            self.host_url = '{scheme}://{host}'.format(scheme=parsed_url.scheme, host=parsed_url.netloc)
            self.start_url = url
            self.request_configs = []
            self.film_urls = []
            self.films = []

    def perform(self):
        self.__get_request_configs()
        self.__get_film_urls()
        self.__get_films()
        return self.films

    def __get_request_configs(self):
        for proxy in self.PROXIES:
            try:
                proxies = dict.fromkeys(['http', 'https'], proxy)
                response = requests.get(self.RESOURCE_URL, proxies=proxies)
                configuration = {
                    'proxies': proxies,
                    'headers': {
                        'User-Agent': self.USER_AGENT,
                        'Cookie': response.headers['Set-Cookie']
                    }
                }
                print('Proxy {0} is reachable'.format(proxy, configuration))
                self.request_configs.append(configuration)
            except:
                logger.error('Proxy {0} is not reachable'.format(proxy))
        return True

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
        request_configurations = self.__get_random_configuration()
        attemption = 1
        while True:
            time.sleep(self.AWAIT_TIME)
            try:
                print('Get and parse page with url: {0} proxy: {1} attemption {2}'.format(url, request_configurations['proxies'], attemption))
                request = requests.get(url, headers=request_configurations['headers'], proxies=request_configurations['proxies'])
                print('RequestResult {0}'.format(request))
                text = request.text
                break
            except:
                request_configurations = self.__get_random_configuration()
                attemption += 1
                continue

        return parser(text)

    def __get_random_configuration(self):
        return random.choice(self.request_configs)

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
                    print('Film data present: {0}'.format(film_data))
                    self.films.append(film_data)
                    break
                else:
                    print('DDos protection')
                    attemption += 1
                    continue
        return True
