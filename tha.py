import tmdbsimple as tmdb
import csv
# Design an application that leverages the TMDB API that when 
# provided a year can retrieve the following information and saves them to a .csv file:

# List the top 10 best movies from the year.

    # Sort by votes (highest votes first) and save the list to the csv file.

    # Sort by name (full name including ‘A’, ‘The’ in the title if present) 
    # and save the list to the same csv file.

    # Sort by name while ignoring ‘A’, ‘The’ if present in the beginning of the 
    # titles and save the list to the same csv file.

# Additionally, for each of those top 10 movies, retrieve 3 other movies that 
# are similar to that movie (you decide what “similar” means). Save these 30 additional 
# movies in a separate .csv file and include any other relevant information that helped 
# construct that list (e.g. similarity metrics).

class TMDBMovieAnalyzer:
    def __init__(self):
        tmdb.API_KEY = '1d87cc1267e1231a689a07717f22081a'
        self.year = None
        self.top_10_movies = []
        self.similar_movies_data = []

    def get_year(self):
        # Get year input from user
        year_input = input("Enter the year to search for top 10 movies: ")
        self.year = int(year_input)
            
        if self.year > 2025 or self.year < 1838:
            print("Invalid year! Please enter a valid number.")
            exit()
        else:
            print(f"\n\nSearching for movies from {self.year}...")
    
    # Sort by votes (highest votes first) and save the list to the csv file.
    def sort_top_10(self): 
        discover = tmdb.Discover()

        # Set filters to inputted year while sorting vote counts in descending order
        response = discover.movie(primary_release_year=self.year, 
                                       sort_by='vote_count.desc', 
                                        **{'vote_count.gte': 100})
 
        self.top_10_movies = response['results'][:10]

        for i, movie in enumerate(self.top_10_movies, 1):
            print(f"{i}.", movie['title'], '- ', movie['vote_count'] )

        return self.top_10_movies

    def sort_full_title(self): 
        self.sorted_full_name = sorted(self.top_10_movies, key=lambda x:x['title'].lower())

        for i, movie in enumerate(self.sorted_full_name, 1):
            print(f"{i}.", movie['title'], '- ', movie['vote_count'] )

    def sort_title_no_articles(self):  pass
    #     self.sorted_full_name = sorted(self.top_10_movies, key=lambda x:x['title'].lower())
    #     if str

    #     for i, movie in enumerate(self.sorted_full_name, 1):
    #         print(f"{i}.", movie['title'], '- ', movie['vote_count'] )


    def save_top_10_csv(self): 
        print("Saving to a csv file...")
        filename = f'top_10_movies{self.year}.csv'

        with open(filename, "w", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f'------- Top 10 Movies of {self.year} sorted by VOTES-------'])
            for i, movie in enumerate(self.top_10_movies, 1):
                writer.writerow([f"{i}. {movie['title']}, {movie['vote_count']}"])

            writer.writerow([f'\n------- Top 10 Movies of {self.year} sorted by Title-------'])
            for i, movie in enumerate(self.sorted_full_name, 1):
                writer.writerow([f"{i}. {movie['title']}, {movie['vote_count']}"])


    def save_top_10_name_csv(self): 
        print("Saving to a csv file...")
        filename = f'top_10_movies{self.year}.csv'

        with open(filename, "w", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f'------- Top 10 Movies of {self.year} -------'])
            for i, movie in enumerate(self.top_10_movies, 1):
                writer.writerow([f"{i}. {movie['title']}, {movie['vote_count']}"])

    def run(self):
        self.get_year()
        self.sort_top_10()
        self.sort_full_title()
        self.sort_title_no_articles()
        self.save_top_10_csv()
    
    
# write 269 lines
if __name__ == "__main__":
    analyzer = TMDBMovieAnalyzer()
    analyzer.run()