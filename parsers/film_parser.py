from lxml import html

class FilmParser:
    COUNTRY_TEXT = 'страна'
    BUDGET_TEXT = 'бюджет'
    FEES_TEXT = 'сборы'

    def __init__(self, page_html):
        self.tree = html.fromstring(page_html)

    def get_film_data(self):
        name = self.get_name()
        if name:
            return {
                'name': name,
                'country': self.get_country(),
                'budget': self.get_budget(),
                'fees': self.get_fees(),
                'kinopoisk_rating': self.get_kinopoisk_rating(),
                'imdb_rating': self.get_imdb_rating()
            }
        else:
            return {}

    def get_name(self):
        movie_name_selector = self.tree.xpath('//div[@id="headerFilm"]//h1[@class="moviename-big"]')
        if movie_name_selector:
            return movie_name_selector[0].text
        else:
            return ''

    def get_country(self):
        country = []
        table_data = self.__get_table_row_data_or_default('text()="{0}"'.format(self.COUNTRY_TEXT))
        if table_data:
            for element in table_data[0].getnext().xpath('div/a'):
                country.append(element.text)
        return country

    def get_budget(self):
        budget = '0'
        table_data = self.__get_table_row_data_or_default('text()="{0}"'.format(self.BUDGET_TEXT))
        if table_data:
            budget_link = table_data[0].getnext().xpath('div/a')
            if budget_link:
                budget = budget_link[0].text
            else:
                budget = table_data[0].getnext().xpath('div')[0].text
        return budget.replace("\xa0", "")

    def get_fees(self):
        fees = {}
        table_data = self.__get_table_row_data_or_default('contains(text(), "{0}")'.format(self.FEES_TEXT))
        if table_data:
            for element in table_data:
                fees[element.text] = element.getnext().xpath('div/a')[0].text.replace("\xa0", "")
        return fees

    def get_kinopoisk_rating(self):
        return

    def get_imdb_rating(self):
        return

    def __get_table_row_data_or_default(self, text_selector):
        result = [] # Default value. If element does not exist returns empty array
        elements = self.tree.xpath('//*[@id="infoTable"]//table//tr//td[{0}]'.format(text_selector))

        if elements:
            result += elements
        return result


