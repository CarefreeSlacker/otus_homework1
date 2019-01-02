from lxml import html

class FilmParser:
    def __init__(self, page_html):
        self.tree = html.fromstring(page_html)

    def get_film_data(self):
        name = 'DDOS protected sorry'
        movie_name = self.tree.xpath('//div[@id="headerFilm"]//h1[@class="moviename-big"]')
        if movie_name:
            name = movie_name[0].text
        print('name ', name)
        return {
            'name': name
        }
