import tmdbsimple as tmdb

# Initialization function
class Movie_Search:
    def __init__(self):
        tmdb.API_KEY = '1d87cc1267e1231a689a07717f22081a'
        self.year = None
        self.movies = None
        # movie = tmdb.Movies(11)  # Star Wars
        # releases = movie.release_dates()


    def get_year(self):
    # Allow user to select the year
        year_input = input("Please select the year to search for the top 10 movies:")
        print(f"You entered:", year_input)
        self.year = year_input
        self.print_year()
        # search = tmdb.Search.movie(year_input)

    def get_movies(sef)

    def print_year(self):
        search_year = tmdb.Search()
        print(search_year.movie(year=self.year))

    def run(self): 
        self.print_year()

searching = Movie_Search()
searching.run()


# year_of_movie = search.movie('release_date'= self.year)
# 'release_dates': '/{id}/release_dates'

# print(year_of_movie) 


# year --> top 10 --> highest votes/name/nonname
# def release_dates(self, **kwargs):
#         """
#         Get the release date along with the certification for a movie.

#         Release dates support different types:

#             1. Premiere
#             2. Theatrical (limited)
#             3. Theatrical
#             4. Digital
#             5. Physical
#             6. TV

#         Args:
#             None

#         Returns:
#             A dict representation of the JSON returned from the API.
#         """
#         path = self._get_id_path('release_dates')

#         response = self._GET(path, kwargs)
#         self._set_attrs_to_values(response)

