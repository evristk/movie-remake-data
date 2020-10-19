# Defining a class for movie objects
class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return self.title + " (" + self.year + ")"

    def get_title(self):
        return self.title

    def get_year(self):
        return self.year

    def set_title(self, title):
        self.title = title

    def set_year(self, year):
        self.year = year

    def to_dict(self):
        return {
            'title': self.title,
            'year': self.year
        }


class MoviePair:
    def __init__(self, original, remake):
        self.original = original
        self.remake = remake

    def get_original(self):
        return self.original

    def get_remake(self):
        return self.remake

    def to_dict(self):
        return {
            'original_title': self.original.title,
            'original_year': self.original.year,
            'remake_title': self.remake.title,
            'remake_year': self.remake.year
        }
