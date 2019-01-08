import re

class FilmToCsvConverter:
    JOIN_CHARACTER = ', '
    MONEY_REGEX = '[€\$£ITL]\d+'
    CURRENCIES = '(€|\$|£|ITL)'
    NUMBER_REGEX = '\d+'
    COURSES = {
        '€': 76,
        '$': 67,
        '£': 85,
        'ITL': 14
    }

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def perform(self):
        return {
            'id': self.dictionary['id'],
            'name': self.dictionary['name'],
            'country': self.__join_countries(self.dictionary['country']),
            'budget': self.__safe_find_budget(self.dictionary['budget']),
            'fees': self.__find_maximum_fee(self.dictionary['fees']),
            'kinopoisk_rating': float(self.dictionary['kinopoisk_rating']),
            'imdb_rating': float(self.dictionary['imdb_rating'])
        }

    def __find_maximum_fee(self, fees):
        fee_values = []
        for fee in fees.values():
            fee_values += re.findall(self.MONEY_REGEX, fee)
        fee_values = [self.__convert_currency(fee_value) for fee_value in fee_values]
        fee_values.sort()
        return fee_values[-1] if fee_values else 0

    def __convert_currency(self, money_amount):
        currency = re.search(self.CURRENCIES, money_amount)
        if currency:
            amount = int(re.search(self.NUMBER_REGEX, money_amount).group())
            return self.COURSES[currency.group()] * amount
        else:
            return 0

    def __join_countries(self, countries):
        return self.JOIN_CHARACTER.join(countries)

    def __safe_find_budget(self, budget):
        budget_value = re.search(self.MONEY_REGEX, budget)
        return (self.__convert_currency(budget_value.group()) if budget_value else 0)
