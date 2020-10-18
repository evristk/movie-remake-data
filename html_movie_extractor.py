import bs4
import re


def get_movie_titles(td):
    # contents of <td> tag look like this:
    # <i><a>title</a></i>year<a>director</a><br> .... <i><a>title</a></i>year<a>director</a>
    movie_list = list()

    movie_title = ''
    movie_year = ''
    for content in td.contents:
        if type(content) is bs4.element.Tag:
            if content.name == 'i':
                movie_title = content.find('a').contents[0].strip()
            elif content.name == 'br':
                movie_list.append(Movie(movie_title, movie_year))
                # reset movie title & year
                movie_title = ''
                movie_year = ''
        elif type(content) is bs4.element.NavigableString:
            match = re.match(r'.*([1-2][0-9]{3})', content)
            if match is not None:
                movie_year = match.group(1)

    if movie_title != '' and movie_year != '':
        movie_list.append(Movie(movie_title, movie_year))

    for movie in movie_list:
        print("%s %s" % (movie.get_title(), movie.get_year()))


# Defining a class for movie objects
class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def get_title(self):
        return self.title

    def get_year(self):
        return self.year

    def set_title(self, title):
        self.title = title

    def set_year(self, year):
        self.year = year