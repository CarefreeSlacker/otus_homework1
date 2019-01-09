import pandas as pd

class FilmsProcessor:
    def __init__(self):
        self.best_five_hundreds = pd.read_csv('data/best_500.csv', delimiter=';')
        self.best_rewards = pd.read_csv('data/rewards.csv', delimiter=';')

    def perform(self):
        self.__calculate_awarding_average_rating()
        self.__calculate_awarding_in_best_hundreds()
        self.__calculate_budget_rating_correlation()
        self.__calculate_fee_rating_correlation()
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
        return

    @__wrap_function_output
    def __calculate_budget_rating_correlation(self):
        return

    @__wrap_function_output
    def __calculate_fee_rating_correlation(self):
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
