## Scrapping данных с веб страницы

Первая ДР для курса DataScience от OTUS.

## Для проверяющего

Тесты не написал. И так много времени ушло на решение задачи.
Решил парсить кинопоиск. Но он сильно защищён от DDOS атак, поэтмоу приходится отправлять запросы с 6 прокси серверов по всему миру. 
Настройки серверов прописанны в proxies.yml после проверки задания я поменяю пароли для прокси серверов.

## Общая идея
На кинопоиске есть множество фильмов по различным категориям.
Я решил взять топ 500 https://www.kinopoisk.ru/top/lists/1/
и все художественные фильмы из всех категорий в премии https://www.kinopoisk.ru/top/lists/awards/
и провести статистический анализ и выяснить следующие вопросы:

* Корреляция премиальности и рейтинга(средняя оценка по группам награждения)
* Количество награжденных фильмов в рейтинге топ 500
* Корреляция между бюджетом и оценкой
* Корреляция между сборами и оценкой
* Корреляция между оценкой на кинопоиске и IMDB
* Корреляция между бюджетом и сборами
* Окупаемость(отношение сборы / бюджет) где есть обе оценки. Какой процент фильмов окупился.
* Самые награждаемые страны
* Страны с самым высоким рейтингом
* Самые титулованные фильмы(Больше всего побед на конкурсах) по странам.

Каждому вопросу или нескольким вопросам соответствует вызов приватной функции в FilmsProcessor.perform()
В результате в консоль выводится статистика и где-то мои комментарии по поводу результатов анализа.

В некоторых случаях исследование не является корректным(например страны с самым высоким рейтингом)
но цель ведь не только провести исследование, но и попрактиковаться в использовании pandas.
Тоесть некоторые выявляемые вопросы созданы исключительно в целях практики в pandas. Так что не судите строго)


## Собираемые данные

* ID (integer) фильма (http://kinopoisk.ru/films/<id>)
* country (array or strings) страна или страны, в которых осуществлялась съёмка
* budget (string) - бюджет. Может быть пустым. Содержит валюту и сумму например "$12300000" пред записью в CSV конвертируется в рубли.
* fees (dictionary) - сборы. Может быть пустым. Для разных фильмов есть различные значения сборы в США, сборы в России
Сборы в мире. Поэтому возвращает словарь вида {'Сборы в россии': '$123', 'Сборы в мире': '+$400=$523'}. В конечном итоге используется самое большое число.
Перез записью в CSV конвертируется в рубли
* kinopoisk_rating (float) - рейтинг на кинопоиске. Может быть пустым. 
* imdb_rating (float) - рейтинг на IMDB.

## Архитектура решения

Каждый отдельый класс отвечает за свою ускую задачу. После инициации вызывается метод perform() который осуществляет работу класса.
Может возаращать или не возаращать значение.

KinopoiskScrapper - принимает URL страницы категории (https://www.kinopoisk.ru/top/lists/1/, https://www.kinopoisk.ru/top/lists/17/).
После запуска #perform() проходит по всем страницам, собирает все ссылки на фильмы. 
А затем начинает через прокси сервера делать запросы к страницам фильмов, парсить страницы и собирать данные.
Для парсинга сипользует парсеры FilmParser и FilmsListParser.
KinopoiskScrapper.perform() Возвращает сырые даные по фильмам в виде хеша.

FilmParser - используется для парсинга страницы фильма.
FilmsListParser - используется для парсинга списка фильмов.

FilmToCsvConverter - принимает один единственный словарь, содержащий сырые данные по фильму и преобразует в данные, которые будут записанны в CSV

IntermediateDataWriter - используется для сохранения промежуточных данных в raw_data/*.py файл. т.к. необходимо собрать данные по нескольким категориям прежде чем объединить их в один CSV файл.
FilmsToCsvWriter - принимает название файла и позволяет осуществлять построчную запись данных полученных с помошью FilmToCsvConverter в файл.

FilmsProcessor - считает статистику по фильмам. 

WriteRewards, WriteBestHundreds - вспомогательные модули инкапсулирующие запись сохранённых данных из промежуточных файлов в конченые CSV. 

## Тестирование


### Тестирование gather

Суммарно я собрал данные по приблизительно ~2400 записей. Некоторые из фильмов повторяются. Учитывая что запросы отправляются каждые 10 секунд это достаточно много времени.
У меня на это ушло несколько часов. Думаю вам не захочется тратить столько времени. 
Но можете запустить для тестирования сбор данных по нескольким группам:

`python3 -m gathering gather https://www.kinopoisk.ru/top/lists/173/ best_cartoon`
`python3 -m gathering gather https://www.kinopoisk.ru/top/lists/20/ best_cannes`
`python3 -m gathering gather https://www.kinopoisk.ru/top/lists/193/ best_mmkf`

### Тестирование transform

После сбора сырых данных их необходимо преобразовать в CSV

`python3 -m gathering transform`

После этого в папке data/ появится два файла best_500.csv и rewards.csv

### Тестирование stats


После преобразования данных к CSV можно посчитать статистику

`python3 -m gathering stats`

После запуска команды - статистика будет выведена в консоль.

## Важные замечания

Как разделитель в файлах используется ";" т.к. в названиях фильмов встречаются запятые. А также есть поля значения которых содержат число с плавающей точкой.


## Список зависимостей в conda

# Name                    Version                   Build  Channel
alabaster                 0.7.12                   py36_0  
anaconda                  custom           py36hbbc8b67_0  
anaconda-client           1.7.2                    py36_0  
anaconda-project          0.8.2                    py36_0  
asn1crypto                0.24.0                   py36_0  
astroid                   2.1.0                    py36_0  
astropy                   3.0.5            py36h470a237_0    conda-forge
atomicwrites              1.2.1                    py36_0  
attrs                     18.2.0           py36h28b3542_0  
babel                     2.6.0                    py36_0  
backcall                  0.1.0                    py36_0  
backports                 1.0                      py36_1  
backports.os              0.1.1                    py36_0  
backports.shutil_get_terminal_size 1.0.0                    py36_2  
beautifulsoup4            4.6.3                 py36_1000    conda-forge
bitarray                  0.8.3            py36h14c3975_0  
bkcharts                  0.2              py36h735825a_0  
blas                      1.0                         mkl  
blaze                     0.11.3                   py36_0  
bleach                    3.0.2                    py36_0  
blosc                     1.14.4               hdbcaa40_0  
bokeh                     1.0.2                    py36_0  
boto                      2.49.0                   py36_0  
bottleneck                1.2.1            py36h035aef0_1  
brewer2mpl                1.4.1                      py_3    conda-forge
bzip2                     1.0.6                h14c3975_5  
ca-certificates           2018.11.29           ha4d7672_0    conda-forge
cairo                     1.14.6                        4    conda-forge
certifi                   2018.11.29            py36_1000    conda-forge
cffi                      1.11.5           py36he75722e_1  
chardet                   3.0.4                    py36_1  
click                     7.0                      py36_0  
cloudpickle               0.6.1                    py36_0  
clyent                    1.2.2                    py36_1  
colorama                  0.4.1                    py36_0  
conda                     4.5.12                   py36_0  
conda-build               3.17.6                   py36_0  
conda-env                 2.6.0                         1  
contextlib2               0.5.5            py36h6c84a62_0  
cryptography              2.3.1            py36hdffb7b8_0    conda-forge
cryptography-vectors      2.3.1                 py36_1000    conda-forge
curl                      7.61.0               h93b3f91_2    conda-forge
cycler                    0.10.0           py36h93f1223_0  
cython                    0.29.2           py36he6710b0_0  
cytoolz                   0.9.0.1          py36h14c3975_1  
dask                      1.0.0                    py36_0  
dask-core                 1.0.0                    py36_0  
datashape                 0.5.4                    py36_1  
dbus                      1.13.0               h3a4f0e9_0    conda-forge
decorator                 4.3.0                    py36_0  
defusedxml                0.5.0                    py36_1  
distributed               1.25.1                   py36_0  
docutils                  0.14             py36hb0f60f5_0  
entrypoints               0.2.3                    py36_2  
et_xmlfile                1.0.1            py36hd6bccc3_0  
expat                     2.2.6                he6710b0_0  
fastcache                 1.0.2            py36h14c3975_2  
filelock                  3.0.10                   py36_0  
flask                     1.0.2                    py36_1  
flask-cors                3.0.7                    py36_0  
fontconfig                2.12.1                        4    conda-forge
freetype                  2.7                           1    conda-forge
fribidi                   1.0.5                h7b6447c_0  
get_terminal_size         1.0.0                haa9412d_0  
gettext                   0.19.8.1             h5e8e0c9_1    conda-forge
gevent                    1.3.7            py36h7b6447c_1  
ggplot                    0.11.5                     py_3    conda-forge
glib                      2.51.4                        0    conda-forge
glob2                     0.6                      py36_1  
gmp                       6.1.2                h6c8ec71_1  
gmpy2                     2.0.8            py36h10f8cd9_2  
graphite2                 1.3.12               h23475e2_2  
greenlet                  0.4.15           py36h7b6447c_0  
gst-plugins-base          1.8.0                         0    conda-forge
gstreamer                 1.8.0                         2    conda-forge
h5py                      2.8.0            py36h989c5e5_3  
harfbuzz                  1.4.3                         0    conda-forge
hdf5                      1.10.2               hba1933b_1  
heapdict                  1.0.0                    py36_2  
html5lib                  1.0.1                    py36_0  
icu                       58.2                 h9c2bf20_1  
idna                      2.8                      py36_0  
imageio                   2.4.1                    py36_0  
imagesize                 1.1.0                    py36_0  
importlib_metadata        0.6                      py36_0  
intel-openmp              2019.1                      144  
ipykernel                 5.1.0            py36h39e3cac_0  
ipython                   7.2.0            py36h39e3cac_0  
ipython_genutils          0.2.0            py36hb52b0d5_0  
ipywidgets                7.4.2                    py36_0  
isort                     4.3.4                    py36_0  
itsdangerous              1.1.0                    py36_0  
jbig                      2.1                  hdba287a_0  
jdcal                     1.4                      py36_0  
jedi                      0.13.2                   py36_0  
jeepney                   0.4                      py36_0  
jinja2                    2.10                     py36_0  
jpeg                      9b                   h024ee3a_2  
jsonschema                2.6.0            py36h006f8b5_0  
jupyter                   1.0.0                    py36_7  
jupyter_client            5.2.4                    py36_0  
jupyter_console           6.0.0                    py36_0  
jupyter_core              4.4.0                    py36_0  
jupyterlab                0.35.3                   py36_0  
jupyterlab_server         0.2.0                    py36_0  
keyring                   17.0.0                   py36_0  
kiwisolver                1.0.1            py36hf484d3e_0  
krb5                      1.14.6                        0    conda-forge
lazy-object-proxy         1.3.1            py36h14c3975_2  
libarchive                3.3.3                h823be47_0    conda-forge
libcurl                   7.61.1               heec0ca6_0  
libedit                   3.1.20170329         h6b74fdf_2  
libffi                    3.2.1                hd88cf55_4  
libgcc-ng                 8.2.0                hdf63c60_1  
libgfortran-ng            7.3.0                hdf63c60_0  
libiconv                  1.15                 h470a237_3    conda-forge
liblief                   0.9.0                h7725739_1  
libpng                    1.6.35               hbc83047_0  
libsodium                 1.0.16               h1bed415_0  
libssh2                   1.8.0                h5b517e9_3    conda-forge
libstdcxx-ng              8.2.0                hdf63c60_1  
libtiff                   4.0.9                he85c1e1_2  
libtool                   2.4.6                h7b6447c_5  
libuuid                   1.0.3                h1bed415_2  
libxcb                    1.13                 h1bed415_1  
libxml2                   2.9.8                h26e45fe_1  
libxslt                   1.1.32               h1312cb7_0  
llvmlite                  0.26.0           py36hd408876_0  
locket                    0.2.0            py36h787c0ad_1  
lxml                      4.2.5            py36hefd8a0e_0  
lz4-c                     1.8.1.2              h14c3975_0  
lzo                       2.10                 h49e0be7_2  
markupsafe                1.1.0            py36h7b6447c_0  
matplotlib                2.0.0               np111py36_2    conda-forge
mccabe                    0.6.1                    py36_1  
mistune                   0.8.4            py36h7b6447c_0  
mkl                       2019.1                      144  
mkl-service               1.1.2            py36he904b0f_5  
mkl_fft                   1.0.6            py36hd81dba3_0  
mkl_random                1.0.2            py36hd81dba3_0  
more-itertools            4.3.0                    py36_0  
mpc                       1.1.0                h10f8cd9_1  
mpfr                      4.0.1                hdf1c602_3  
mpmath                    1.1.0                    py36_0  
msgpack-python            0.5.6            py36h6bb024c_1  
multipledispatch          0.6.0                    py36_0  
nbconvert                 5.4.0                    py36_1  
nbformat                  4.4.0            py36h31c9010_0  
ncurses                   6.1                  he6710b0_1  
networkx                  2.2                      py36_1  
nltk                      3.4                      py36_1  
nose                      1.3.7                    py36_2  
notebook                  5.7.4                    py36_0  
numba                     0.41.0           py36h962f231_0  
numexpr                   2.6.9            py36hf8a1672_0    conda-forge
numpy                     1.11.3           py36h3dfced4_4  
numpy-base                1.15.4           py36hde5b4d6_0  
numpydoc                  0.8.0                    py36_0  
odo                       0.5.1            py36h90ed295_0  
olefile                   0.46                     py36_0  
openpyxl                  2.5.12                   py36_0  
openssl                   1.0.2p               h470a237_1    conda-forge
packaging                 18.0                     py36_0  
pandas                    0.22.0                   py36_1    conda-forge
pandoc                    1.19.2.1             hea2e7c5_1  
pandocfilters             1.4.2                    py36_1  
pango                     1.40.4                        0    conda-forge
parso                     0.3.1                    py36_0  
partd                     0.3.9                    py36_0  
patchelf                  0.9                  he6710b0_3  
path.py                   11.5.0                   py36_0  
pathlib2                  2.3.3                    py36_0  
patsy                     0.5.1                    py36_0  
pcre                      8.42                 h439df22_0  
pep8                      1.7.1                    py36_0  
pexpect                   4.6.0                    py36_0  
pickleshare               0.7.5                    py36_0  
pillow                    4.2.1                    py36_0    conda-forge
pip                       18.1                     py36_0  
pixman                    0.34.0               hceecf20_3  
pkginfo                   1.4.2                    py36_1  
pluggy                    0.8.0                    py36_0  
ply                       3.11                     py36_0  
prometheus_client         0.5.0                    py36_0  
prompt_toolkit            2.0.7                    py36_0  
psutil                    5.4.8            py36h7b6447c_0  
ptyprocess                0.6.0                    py36_0  
py                        1.7.0                    py36_0  
py-lief                   0.9.0            py36h7725739_1  
pycodestyle               2.4.0                    py36_0  
pycosat                   0.6.3            py36h14c3975_0  
pycparser                 2.19                     py36_0  
pycrypto                  2.6.1            py36h14c3975_9  
pycurl                    7.43.0.2         py36hb7f436b_0  
pyflakes                  2.0.0                    py36_0  
pygments                  2.3.1                    py36_0  
pylint                    2.2.2                    py36_0  
pyodbc                    4.0.25           py36he6710b0_0  
pyopenssl                 18.0.0                   py36_0  
pyparsing                 2.3.0                    py36_0  
pyqt                      4.11.4                   py36_3    conda-forge
pysocks                   1.6.8                    py36_0  
pytables                  3.4.4            py36ha205bf6_0  
pytest                    4.0.2                    py36_0  
pytest-arraydiff          0.3              py36h39e3cac_0  
pytest-astropy            0.5.0                    py36_0  
pytest-doctestplus        0.2.0                    py36_0  
pytest-openfiles          0.3.1                    py36_0  
pytest-remotedata         0.3.1                    py36_0  
python                    3.6.2                         0  
python-dateutil           2.7.5                    py36_0  
python-libarchive-c       2.8                      py36_6  
pytz                      2018.7                   py36_0  
pywavelets                1.0.1            py36hdd07704_0  
pyyaml                    3.13             py36h14c3975_0  
pyzmq                     17.1.2           py36h14c3975_0  
qt                        4.8.7                         7    conda-forge
qtawesome                 0.5.3                    py36_0  
qtconsole                 4.4.3                    py36_0  
qtpy                      1.5.2                    py36_0  
readline                  6.2                           2  
requests                  2.21.0                   py36_0  
rope                      0.11.0                   py36_0  
ruamel_yaml               0.15.46          py36h14c3975_0  
scikit-image              0.13.1                   py36_0    conda-forge
scikit-learn              0.20.1           py36hd81dba3_0  
scipy                     1.1.0            py36h7c811a0_2  
seaborn                   0.9.0                    py36_0  
secretstorage             3.1.0                    py36_0  
send2trash                1.5.0                    py36_0  
setuptools                40.6.3                   py36_0  
simplegeneric             0.8.1                    py36_2  
singledispatch            3.4.0.3          py36h7a266c3_0  
sip                       4.18                     py36_1    conda-forge
six                       1.12.0                   py36_0  
snappy                    1.1.7                hbae5bb6_3  
snowballstemmer           1.2.1            py36h6febd40_0  
sortedcollections         1.0.1                    py36_0  
sortedcontainers          2.1.0                    py36_0  
sphinx                    1.8.2                    py36_0  
sphinxcontrib             1.0                      py36_1  
sphinxcontrib-websupport  1.1.0                    py36_1  
spyder                    3.3.0                    py36_0    conda-forge
spyder-kernels            0.3.0                    py36_0  
sqlalchemy                1.2.15           py36h7b6447c_0  
sqlite                    3.13.0                        1    conda-forge
statsmodels               0.9.0            py36h035aef0_0  
sympy                     1.3                      py36_0  
tblib                     1.3.2            py36h34cf8b6_0  
terminado                 0.8.1                    py36_1  
testpath                  0.4.2                    py36_0  
tk                        8.5.18                        0  
toolz                     0.9.0                    py36_0  
tornado                   5.1.1            py36h7b6447c_0  
tqdm                      4.28.1           py36h28b3542_0  
traitlets                 4.3.2            py36h674d592_0  
typed-ast                 1.1.0            py36h14c3975_0  
unicodecsv                0.14.1           py36ha668878_0  
unixodbc                  2.3.7                h14c3975_0  
urllib3                   1.24.1                   py36_0  
wcwidth                   0.1.7            py36hdf4376a_0  
webencodings              0.5.1                    py36_1  
werkzeug                  0.14.1                   py36_0  
wheel                     0.32.3                   py36_0  
widgetsnbextension        3.4.2                    py36_0  
wrapt                     1.10.11          py36h14c3975_2  
wurlitzer                 1.0.2                    py36_0  
xlrd                      1.2.0                    py36_0  
xlsxwriter                1.1.2                    py36_0  
xlwt                      1.3.0            py36h7b00a1f_0  
xz                        5.2.4                h14c3975_4  
yaml                      0.1.7                had09818_2  
zeromq                    4.2.5                hf484d3e_1  
zict                      0.1.3                    py36_0  
zlib                      1.2.11               h7b6447c_3  
zstd                      1.3.7                h0b5b093_0  
