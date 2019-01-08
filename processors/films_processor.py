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
        print('Calculation has been performed')
