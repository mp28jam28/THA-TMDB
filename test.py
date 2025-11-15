def similar_movies(self, **kwargs):
        """
        Get a list of similar movies. This is not the same as the
        "Recommendation" system you see on the website.

        These items are assembled by looking at keywords and genres.

        Args:
            language: (optional) ISO 639-1 code.
            page: (optional) Minimum 1, maximum 1000, default 1.

        Returns:
            A dict representation of the JSON returned from the API.
        """
        path = self._get_id_path('similar_movies')

        response = self._GET(path, kwargs)
        self._set_attrs_to_values(response)
        return response

def recommendations(self, **kwargs):
        """
        Get a list of recommended movies for a movie.

        Args:
            language: (optional) ISO 639-1 code.
            page: (optional) Minimum 1, maximum 1000, default 1.

        Returns:
            A dict representation of the JSON returned from the API.
        """
        path = self._get_id_path('recommendations')

        response = self._GET(path, kwargs)
        self._set_attrs_to_values(response)
        return response

def reviews(self, **kwargs):
        """
        Get the user reviews for a movie.

        Args:
            language: (optional) ISO 639-1 code.
            page: (optional) Minimum 1, maximum 1000, default 1.

        Returns:
            A dict representation of the JSON returned from the API.
        """
        path = self._get_id_path('reviews')

        response = self._GET(path, kwargs)
        self._set_attrs_to_values(response)
        return response


# ✅✅✅
# Design an application that leverages the TMDB API that when provided a year can 
# retrieve the following information and saves them to a .csv file:
'release_dates': '/{id}/release_dates'

# year --> top 10 --> highest votes/name/nonname

# List the top 10 best movies from the year.

    # Sort by votes (highest votes first) and save the list to the csv file.

    # Sort by name (full name including ‘A’, ‘The’ in the title if present) and save 
    # the list to the same csv file.

    # Sort by name while ignoring ‘A’, ‘The’ if present in the beginning of the 
    # titles and save the list to the same csv file.


# ✅✅✅
# Additionally, for each of those top 10 movies, retrieve 3 other movies that 
# are similar to that movie (you decide what “similar” means). Save these 30 
# additional movies in a separate .csv file and include any other relevant information 
# that helped construct that list (e.g. similarity metrics).
'similar_movies': '/{id}/similar_movies'

# Besides these requirements, feel free to make any other assumptions or take 
# additional creative liberties. 
