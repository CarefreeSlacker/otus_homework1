from lxml import html

NO_FILMS_PLUG_TEXT = 'Фильмов не найдено. Попробуйте поменять условия в фильтре.'
NEXT_PAGE_XPATH_SELECTOR = '//div[@class="navigator"]//ul[@class="list"]//a[text()="»"]'

class FilmsListParser:
    def __init__(self, page_html):
        self.tree = html.fromstring(page_html)

    def has_next_page(self):
        return len(self.tree.xpath(NEXT_PAGE_XPATH_SELECTOR)) > 0

    def next_page_path(self):
        return self.tree.xpath(NEXT_PAGE_XPATH_SELECTOR)[0].get('href')

    def has_films_list(self):
        return len(self.tree.xpath('//table[@id="itemList"]//td[text()="{0}"]'.format(NO_FILMS_PLUG_TEXT))) == 0

    def film_paths_list(self):
        urls = []
        film_links = self.tree.xpath('//table[@id="itemList"]//tr/td[@class="news"]//a[@class="all"]')
        for link in film_links:
            urls.append(link.get('href'))
        return urls
