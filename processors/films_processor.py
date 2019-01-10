import pandas as pd

class FilmsProcessor:
    def __init__(self):
        self.best_five_hundreds = pd.read_csv('data/best_500.csv', delimiter=';')
        self.best_rewards = pd.read_csv('data/rewards.csv', delimiter=';')
        self.unique_films = self.__get_unique_films()

    def __get_unique_films(self):
        ids_set1 = set(self.best_rewards['id'])
        ids_set2 = set(self.best_five_hundreds['id'])
        ids_set3 = ids_set1 | ids_set2

        raw_films_set = pd.concat([self.best_five_hundreds, self.best_rewards])
        raw_films_set = raw_films_set.reindex(columns=['id', 'name', 'budget', 'fees', 'kinopoisk_rating', 'imdb_rating'])
        films_list = []
        for id in ids_set3:
            films_list.append(raw_films_set[raw_films_set.id == id].head(1))
        return pd.concat(films_list)

    def perform(self):
        self.__calculate_awarding_average_rating()
        self.__calculate_awarding_in_best_hundreds()
        self.__calculate_correlations()
        self.__calculate_payback()
        self.__calculate_most_rewarded_countries()
        self.__calculate_rating_by_countries()
        self.__calculate_most_rewarded_films()

    def __wrap_function_output(func):
        def wrapper(*args):
            print('--> {0}\n'.format(func.__name__.replace('__', '')))
            func(*args)
            print('--------------------------\n')
        return wrapper

    @__wrap_function_output
    def __calculate_awarding_average_rating(self):
        average_ratings = []
        for reward in self.best_rewards['reward'].unique():
            selected = self.best_rewards[self.best_rewards.reward == reward]
            average_ratings.append((
                reward,
                selected['kinopoisk_rating'].mean().__round__(2),
                selected['imdb_rating'].mean().__round__(2)
            ))
        self.ratings_table = pd.DataFrame.from_records(average_ratings, columns=['Reward', 'avg_kinopoisk', 'avg_imdb'])
        pd.set_option('display.max_columns', 3)
        print(self.ratings_table)

    @__wrap_function_output
    def __calculate_awarding_in_best_hundreds(self):
        five_hundreds_set = set(self.best_five_hundreds.get('id'))
        best_rewards_set = set(self.best_rewards.get('id'))
        intersection = five_hundreds_set & best_rewards_set
        intersection_percent = round(len(intersection) / len(five_hundreds_set) * 100, 2)
        print('{0} % из топ {1} были награждены премиями'.format(intersection_percent, len(five_hundreds_set)))
        return

    @__wrap_function_output
    def __calculate_correlations(self):
        correlation_columns = self.unique_films.reindex(columns=['budget', 'fees', 'kinopoisk_rating', 'imdb_rating'])
        correlation = correlation_columns.corr(method='pearson')
        print('Корреляция между бюджетом и оценкой. Кинопоиск: {0}, IMDB: {1}'.format(round(correlation['budget']['kinopoisk_rating'], 2), round(correlation['budget']['imdb_rating'], 2)))
        print('Корреляция между сборами и оценкой. Кинопоиск: {0}, IMDB: {1}'.format(round(correlation['fees']['kinopoisk_rating'], 2), round(correlation['fees']['imdb_rating'], 2)))
        print('Как видно. Нет корреляции между вложенными средствами и оценкой зрителей.')
        print('Людям может понравится фильм как с малым, так и с большим бюджетом. Это вполне закономерно.\n')
        print('Корреляция между сборами и бюджетом {0}'.format(round(correlation['budget']['fees'], 2)))
        print('С другой стороны есть корреляция между бюджетом и сборами. Иными словами - хотите много заработать, нужно много потратить.\n')
        print('Корреляция между оценками. Кинопоиск - IMDB: {0}'.format(round(correlation['imdb_rating']['kinopoisk_rating'], 2)))
        print('Оценки на кинопоиске частично коррелируют с оценками IMDB.')
        print('На основании этого можно преположить что:')
        print('Вкусовые предпочтения жителей России отличаются от среднемировых. Если вы русский, стоит больше обращать внимание на оценки на Кинопоиске.')
        return

    @__wrap_function_output
    def __calculate_payback(self):
        return

    @__wrap_function_output
    def __calculate_most_rewarded_countries(self):
        return

    @__wrap_function_output
    def __calculate_rating_by_countries(self):
        return

    @__wrap_function_output
    def __calculate_most_rewarded_films(self):
        return
