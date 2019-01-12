import pandas as pd
import warnings

class FilmsProcessor:
    TOP_CHART_COUNT = 30

    def __init__(self):
        self.best_five_hundreds = pd.read_csv('data/best_500.csv', delimiter=';')
        self.best_rewards = pd.read_csv('data/rewards.csv', delimiter=';')
        self.unique_films = self.__get_unique_films()
        warnings.filterwarnings("ignore", 'This pattern has match groups')
        pd.set_option('display.max_columns', 10)

    def __get_unique_films(self):
        ids_set1 = set(self.best_rewards['id'])
        ids_set2 = set(self.best_five_hundreds['id'])
        ids_set3 = ids_set1 | ids_set2

        raw_films_set = pd.concat([self.best_five_hundreds, self.best_rewards])
        raw_films_set = raw_films_set.reindex(columns=['id', 'name', 'country', 'budget', 'fees', 'kinopoisk_rating', 'imdb_rating'])
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
            result = func(*args)
            print('--------------------------\n')
            return result
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
        films_with_money_data = self.unique_films[(self.unique_films.fees > 0) & (self.unique_films.budget > 0)]
        payed_back = films_with_money_data[films_with_money_data.fees > films_with_money_data.budget]
        payback_percent = round(len(payed_back) / len(films_with_money_data) * 100, 2)
        print('{0} % фильмов окупились. Данные по {1} фильмам.'.format(payback_percent, len(films_with_money_data)))
        return

    @__wrap_function_output
    def __calculate_most_rewarded_countries(self):
        countries = self.__get_countries_set(self.best_rewards)

        countries_frequencies = []
        for country in countries:
            frequency = len(self.__filter_films_by_country(self.best_rewards, country))
            countries_frequencies.append((country, frequency))

        countries_frequencies = sorted(countries_frequencies, key=lambda row: -row[1])
        frequencies_data_frame = pd.DataFrame.from_records(countries_frequencies, columns=['Country', 'Frequency'])
        print('{0} наиболее награждаемых стран'.format(self.TOP_CHART_COUNT))
        print(frequencies_data_frame.head(self.TOP_CHART_COUNT))
        print('\nЗдесь список лидеров вполне очевиден\n')
        return

    @__wrap_function_output
    def __calculate_rating_by_countries(self):
        countries = self.__get_countries_set(self.unique_films)

        countries_ratings = []
        for country in countries:
            filtered_films = self.__filter_films_by_country(self.unique_films, country)
            countries_ratings.append((
                country,
                round(filtered_films['kinopoisk_rating'].mean(), 2)
            ))

        countries_ratings = sorted(countries_ratings, key=lambda row: -row[1])
        countries_ratings_data_frame = pd.DataFrame.from_records(countries_ratings, columns=['Country', 'kinopoisk_rating'])
        print('{0} стран с самым высоким рейтингом по версии Kinopoisk\n'.format(self.TOP_CHART_COUNT))
        print(countries_ratings_data_frame.head(self.TOP_CHART_COUNT))
        print('\n')

        countries_ratings = []
        for country in countries:
            filtered_films = self.__filter_films_by_country(self.unique_films, country)
            countries_ratings.append((
                country,
                round(filtered_films['imdb_rating'].mean(), 2)
            ))

        countries_ratings = sorted(countries_ratings, key=lambda row: -row[1])
        countries_ratings_data_frame = pd.DataFrame.from_records(countries_ratings, columns=['Country', 'imdb_rating'])
        print('{0} стран с самым высоким рейтингом по версии IMDB'.format(self.TOP_CHART_COUNT))
        print(countries_ratings_data_frame.head(self.TOP_CHART_COUNT))
        print('\n')

        print('''
        Рейтинг по странам даёт нам интересный результат. В списке лидеров нет ни США ни Великобритании ни Франции.
        Мировых лидеров как по уровню жизни, так и в производстве визуального искусства.
        Скорее всего это связанно с тем, что подсчёт ведётся некорректно. Считается статистика по каждоый отдельной стране.
        Но в действительности фильм может быть снят в нескольких странах. Но производство инициируется в одной из стран лидеров.
        Для проверки этой гипотезы выберем фильмы которые снимались в одной из 5 стран лидеров по рейтингу IMDB:
        Бангладеш, ОАЭ, Эстония, Македония, Индия\n
        ''')

        for country in countries_ratings_data_frame.head()['Country']:
            films_for_county = self.__filter_films_by_country(self.unique_films, country)
            print('Фильмы снятые в {0}\n'.format(country))
            print(films_for_county)
            print('\n-------------------\n')

        print('''
        Гипотеза подтверждена. В странах лидерах по оценкам было снято по большей части небольшое количество фильмов с высоким рейтингом.
        Кроме того, зачастую мировые лидеры экономического развития принимали участие в съёмках, что говорит о том, что на самом деле именно они инициировали съёмки фильма.

        Инсайт: Страны попавшие в список лидеров попали туда потому, что там снято небольшое количество фильмов, с выоский рейтингом.
        В действительности лидерами являются всё те же США, Франция, Испания, Германия, Великобритания\n
        ''')
        return

    def __get_countries_set(self, data_frame):
        countries = []
        for row in data_frame['country']:
            countries += row.split(', ')
        return set(countries)

    def __filter_films_by_country(self, data_frame, country):
        return data_frame[data_frame.country.str.contains(country)]

    @__wrap_function_output
    def __calculate_most_rewarded_films(self):
        film_ids = self.unique_films.get('id')

        films_frequencies = []
        for film_id in film_ids:
            awards_count = len(self.best_rewards[self.best_rewards.id == film_id])
            films_frequencies.append((film_id, awards_count))

        films_frequencies = sorted(films_frequencies, key=lambda row: -row[1])
        most_awarding_ids = films_frequencies[0:self.TOP_CHART_COUNT]
        most_awarding_films = []
        for (film_id, awards_count) in most_awarding_ids:
            film = self.unique_films[self.unique_films.id == film_id]
            most_awarding_films.append(self.__make_film_tuple(film, awards_count))
        most_awarding_films_data_frame = pd.DataFrame.from_records(most_awarding_films, columns=['name', 'awards_count', 'country', 'kinopoisk_rating', 'imdb_rating'])
        print('{0} наиболее награждаемых фильмов\n'.format(self.TOP_CHART_COUNT))
        print(most_awarding_films_data_frame)
        print('\n')
        print('''
        В списке наиболее награждаемых фильмов  мы видим всё те же страны.
        У большинства фильмов, в топ рейтинге - высокий рейтинг. Следовательно они попали туда не случайно.
        Так что если вы думаете что посмотреть - теперь вы знаете)
        ''')
        return

    def __make_film_tuple(self, film, frequency):
        return (
            film['name'].values[0],
            frequency,
            film['country'].values[0],
            float(film['kinopoisk_rating']),
            float(film['imdb_rating'])
        )
