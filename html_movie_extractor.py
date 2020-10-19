import bs4
import re
from Moviecable import Movie


def extract_movie_data(td):
    # contents of <td> tag look like this:
    # <i><a>title</a></i>year<a>director</a><br> .... <i><a>title</a></i>year<a>director</a>
    movie_list = list()

    movie_title = ''
    movie_year = ''
    for content in td.contents:
        if type(content) is bs4.element.Tag:
            if content.get_text() is not None and movie_title == '':
                # when movie_title is not empty, we have already parsed the title.
                # So this string is something else, like the director. We can skip it.
                movie_title = content.get_text().strip()
            elif content.name == 'br':
                movie = Movie(movie_title, movie_year)
                movie_list.append(movie)
                # reset movie title & year
                movie_title = ''
                movie_year = ''
        elif type(content) is bs4.element.NavigableString:
            match = re.match(r'.*([1-2][0-9]{3})', content)
            if match is not None:
                movie_year = match.group(1)

    if movie_title != '' and movie_year != '':
        movie_list.append(Movie(movie_title, movie_year))

    return movie_list

