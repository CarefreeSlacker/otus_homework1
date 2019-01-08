from storages.films_to_csv_writer import FilmsToCsvWriter
from raw_data.best_adapted_script import MOVIES as MOVIES_1, NAME as NAME_1
from raw_data.best_bafta import MOVIES as MOVIES_2, NAME as NAME_2
from raw_data.best_berlin import MOVIES as MOVIES_3, NAME as NAME_3
from raw_data.best_cannes import MOVIES as MOVIES_4, NAME as NAME_4
from raw_data.best_cartoon import MOVIES as MOVIES_5, NAME as NAME_5
from raw_data.best_comedy import MOVIES as MOVIES_6, NAME as NAME_6
from raw_data.best_director import MOVIES as MOVIES_7, NAME as NAME_7
from raw_data.best_dramatic import MOVIES as MOVIES_8, NAME as NAME_8
from raw_data.best_european import MOVIES as MOVIES_9, NAME as NAME_9
from raw_data.best_foreign_language_movie import MOVIES as MOVIES_10, NAME as NAME_10
from raw_data.best_globe import MOVIES as MOVIES_11, NAME as NAME_11
from raw_data.best_golden_leopard import MOVIES as MOVIES_12, NAME as NAME_12
from raw_data.best_golden_shell import MOVIES as MOVIES_13, NAME as NAME_13
from raw_data.best_goya import MOVIES as MOVIES_14, NAME as NAME_14
from raw_data.best_mmkf import MOVIES as MOVIES_15, NAME as NAME_15
from raw_data.best_movies import MOVIES as MOVIES_16, NAME as NAME_16
from raw_data.best_music import MOVIES as MOVIES_17, NAME as NAME_17
from raw_data.best_operator import MOVIES as MOVIES_18, NAME as NAME_18
from raw_data.best_sanders import MOVIES as MOVIES_19, NAME as NAME_19
from raw_data.best_saturn import MOVIES as MOVIES_20, NAME as NAME_20
from raw_data.best_script import MOVIES as MOVIES_21, NAME as NAME_21
from raw_data.best_sezar import MOVIES as MOVIES_22, NAME as NAME_22
from raw_data.best_short_cartoon import MOVIES as MOVIES_23, NAME as NAME_23
from raw_data.best_short_film import MOVIES as MOVIES_24, NAME as NAME_24
from raw_data.best_vinece import MOVIES as MOVIES_25, NAME as NAME_25
from raw_data.best_visuals import MOVIES as MOVIES_26, NAME as NAME_26
from raw_data.best_white_eliphant import MOVIES as MOVIES_27, NAME as NAME_27


if __name__ == '__main__':
    converter = FilmsToCsvWriter('data/rewards.csv')
    converter.write_data(MOVIES_1, NAME_1)
    converter.append_data(MOVIES_2, NAME_2)
    converter.append_data(MOVIES_3, NAME_3)
    converter.append_data(MOVIES_4, NAME_4)
    converter.append_data(MOVIES_5, NAME_5)
    converter.append_data(MOVIES_6, NAME_6)
    converter.append_data(MOVIES_7, NAME_7)
    converter.append_data(MOVIES_8, NAME_8)
    converter.append_data(MOVIES_9, NAME_9)
    converter.append_data(MOVIES_10, NAME_10)
    converter.append_data(MOVIES_11, NAME_11)
    converter.append_data(MOVIES_12, NAME_12)
    converter.append_data(MOVIES_13, NAME_13)
    converter.append_data(MOVIES_14, NAME_14)
    converter.append_data(MOVIES_15, NAME_15)
    converter.append_data(MOVIES_16, NAME_16)
    converter.append_data(MOVIES_17, NAME_17)
    converter.append_data(MOVIES_18, NAME_18)
    converter.append_data(MOVIES_19, NAME_19)
    converter.append_data(MOVIES_20, NAME_20)
    converter.append_data(MOVIES_21, NAME_21)
    converter.append_data(MOVIES_22, NAME_22)
    converter.append_data(MOVIES_23, NAME_23)
    converter.append_data(MOVIES_24, NAME_24)
    converter.append_data(MOVIES_25, NAME_25)
    converter.append_data(MOVIES_26, NAME_26)
    converter.append_data(MOVIES_27, NAME_27)
