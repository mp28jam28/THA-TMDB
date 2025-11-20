import tmdbsimple as tmdb
import csv

class TMDBMovieAnalyzer:
    def __init__(self):
        tmdb.API_KEY = '1d87cc1267e1231a689a07717f22081a'
        self.year = None
        self.top_10_movies = []
        self.similar_movies_data = []
    
    def get_year_from_user(self):
        """Get year input from user"""
        year_input = input("Enter the year to search for top 10 movies: ")
        try:
            self.year = int(year_input)
            print(f"Searching for movies from {self.year}...")
        except ValueError:
            print("Invalid year! Please enter a valid number.")
            exit()
    
    def fetch_top_10_movies(self):
        """Fetch top 10 best movies from the given year"""
        discover = tmdb.Discover()
        
        # Fetch movies from the year, sorted by rating
        all_movies = []
        for page in range(1, 6):  # Get first 5 pages to have enough options
            response = discover.movie(
                primary_release_year=self.year,
                sort_by='vote_average.desc',
                page=page,
                **{'vote_count.gte': 100}  # Minimum 100 votes to filter quality
            )
            all_movies.extend(response['results'])
        
        if len(all_movies) == 0:
            print(f"No movies found for year {self.year}")
            exit()
        
        # Get detailed info for top movies
        for movie_data in all_movies[:10]:
            movie = tmdb.Movies(movie_data['id'])
            info = movie.info()
            
            self.top_10_movies.append({
                'id': info['id'],
                'title': info['title'],
                'release_date': info.get('release_date', ''),
                'year': info.get('release_date', '')[:4] if info.get('release_date') else '',
                'vote_average': info.get('vote_average', 0),
                'vote_count': info.get('vote_count', 0),
                'genres': ', '.join([g['name'] for g in info.get('genres', [])]),
                'overview': info.get('overview', '')
            })
        
        print(f"Found top 10 movies from {self.year}")
    
    def remove_leading_articles(self, title):
        """Remove leading articles (A, An, The) for sorting"""
        articles = ['The ', 'A ', 'An ']
        for article in articles:
            if title.startswith(article):
                return title[len(article):]
        return title
    
    def fetch_similar_movies(self):
        """Fetch 3 similar movies for each of the top 10"""
        print("Fetching similar movies...")
        
        for original_movie in self.top_10_movies:
            movie = tmdb.Movies(original_movie['id'])
            
            try:
                similar_response = movie.similar()
                similar_results = similar_response.get('results', [])
                
                # Get top 3 similar movies
                for sim_data in similar_results[:3]:
                    # Get detailed info for similar movie
                    sim_movie = tmdb.Movies(sim_data['id'])
                    sim_info = sim_movie.info()
                    
                    # Calculate similarity metrics
                    original_genres = set(original_movie['genres'].split(', '))
                    similar_genres = set([g['name'] for g in sim_info.get('genres', [])])
                    
                    genre_overlap = len(original_genres.intersection(similar_genres))
                    total_unique_genres = len(original_genres.union(similar_genres))
                    genre_similarity = (genre_overlap / total_unique_genres * 100) if total_unique_genres > 0 else 0
                    
                    rating_diff = abs(original_movie['vote_average'] - sim_info.get('vote_average', 0))
                    
                    original_year = int(original_movie['year']) if original_movie['year'] else 0
                    similar_year = int(sim_info.get('release_date', '0000')[:4]) if sim_info.get('release_date') else 0
                    year_diff = abs(original_year - similar_year)
                    
                    # Overall similarity score (0-100)
                    # Based on: genre overlap (50%), rating similarity (30%), year proximity (20%)
                    similarity_score = (
                        (genre_similarity * 0.5) +
                        ((10 - min(rating_diff, 10)) / 10 * 100 * 0.3) +
                        ((20 - min(year_diff, 20)) / 20 * 100 * 0.2)
                    )
                    
                    self.similar_movies_data.append({
                        'original_movie': original_movie['title'],
                        'original_year': original_movie['year'],
                        'original_rating': original_movie['vote_average'],
                        'original_genres': original_movie['genres'],
                        'similar_movie': sim_info['title'],
                        'similar_year': sim_info.get('release_date', '')[:4] if sim_info.get('release_date') else '',
                        'similar_rating': sim_info.get('vote_average', 0),
                        'similar_genres': ', '.join([g['name'] for g in sim_info.get('genres', [])]),
                        'similarity_score': round(similarity_score, 2),
                        'genre_overlap_count': genre_overlap,
                        'genre_similarity_percent': round(genre_similarity, 2),
                        'rating_difference': round(rating_diff, 2),
                        'year_difference': year_diff,
                        'vote_count': sim_info.get('vote_count', 0)
                    })
            except Exception as e:
                print(f"Error fetching similar movies for {original_movie['title']}: {e}")
        
        print(f"Found {len(self.similar_movies_data)} similar movies")
    
    def save_top_10_to_csv(self):
        """Save top 10 movies with three different sorting methods to one CSV"""
        filename = f'top_10_movies_{self.year}.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Section 1: Sorted by Votes (highest first)
            writer.writerow([f'TOP 10 BEST MOVIES FROM {self.year} - SORTED BY VOTES (HIGHEST FIRST)'])
            writer.writerow(['Rank', 'Title', 'Year', 'Rating', 'Votes', 'Genres'])
            
            sorted_by_votes = sorted(self.top_10_movies, key=lambda x: x['vote_count'], reverse=True)
            for rank, movie in enumerate(sorted_by_votes, 1):
                writer.writerow([
                    rank,
                    movie['title'],
                    movie['year'],
                    movie['vote_average'],
                    movie['vote_count'],
                    movie['genres']
                ])
            
            writer.writerow([])  # Blank line separator
            
            # Section 2: Sorted by Name (full name including 'A', 'The')
            writer.writerow([f'TOP 10 BEST MOVIES FROM {self.year} - SORTED BY NAME (FULL TITLE)'])
            writer.writerow(['Rank', 'Title', 'Year', 'Rating', 'Votes', 'Genres'])
            
            sorted_by_name_full = sorted(self.top_10_movies, key=lambda x: x['title'].lower())
            for rank, movie in enumerate(sorted_by_name_full, 1):
                writer.writerow([
                    rank,
                    movie['title'],
                    movie['year'],
                    movie['vote_average'],
                    movie['vote_count'],
                    movie['genres']
                ])
            
            writer.writerow([])  # Blank line separator
            
            # Section 3: Sorted by Name (ignoring 'A', 'The')
            writer.writerow([f'TOP 10 BEST MOVIES FROM {self.year} - SORTED BY NAME (IGNORING A, AN, THE)'])
            writer.writerow(['Rank', 'Title', 'Sortable Title', 'Year', 'Rating', 'Votes', 'Genres'])
            
            # Add sortable title for each movie
            for movie in self.top_10_movies:
                movie['sortable_title'] = self.remove_leading_articles(movie['title'])
            
            sorted_by_name_no_articles = sorted(self.top_10_movies, key=lambda x: x['sortable_title'].lower())
            for rank, movie in enumerate(sorted_by_name_no_articles, 1):
                writer.writerow([
                    rank,
                    movie['title'],
                    movie['sortable_title'],
                    movie['year'],
                    movie['vote_average'],
                    movie['vote_count'],
                    movie['genres']
                ])
        
        print(f"✓ Saved top 10 movies to: {filename}")
    
    def save_similar_movies_to_csv(self):
        """Save 30 similar movies to a separate CSV file"""
        filename = f'similar_movies_{self.year}.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow([f'SIMILAR MOVIES FOR TOP 10 FROM {self.year} (30 Total - 3 per movie)'])
            writer.writerow([
                'Original Movie',
                'Original Year',
                'Original Rating',
                'Original Genres',
                'Similar Movie',
                'Similar Year',
                'Similar Rating',
                'Similar Genres',
                'Similarity Score (%)',
                'Genre Overlap Count',
                'Genre Similarity (%)',
                'Rating Difference',
                'Year Difference',
                'Vote Count'
            ])
            
            for sim_movie in self.similar_movies_data:
                writer.writerow([
                    sim_movie['original_movie'],
                    sim_movie['original_year'],
                    sim_movie['original_rating'],
                    sim_movie['original_genres'],
                    sim_movie['similar_movie'],
                    sim_movie['similar_year'],
                    sim_movie['similar_rating'],
                    sim_movie['similar_genres'],
                    sim_movie['similarity_score'],
                    sim_movie['genre_overlap_count'],
                    sim_movie['genre_similarity_percent'],
                    sim_movie['rating_difference'],
                    sim_movie['year_difference'],
                    sim_movie['vote_count']
                ])
        
        print(f"✓ Saved similar movies to: {filename}")
    
    def run(self):
        """Main execution method"""
        print("=" * 60)
        print("TMDB Movie Analyzer")
        print("=" * 60)
        
        self.get_year_from_user()
        self.fetch_top_10_movies()
        self.fetch_similar_movies()
        self.save_top_10_to_csv()
        self.save_similar_movies_to_csv()
        
        print("\n" + "=" * 60)
        print("Analysis Complete!")
        print(f"Files created:")
        print(f"  - top_10_movies_{self.year}.csv (with 3 different sortings)")
        print(f"  - similar_movies_{self.year}.csv (30 similar movies)")
        print("=" * 60)
# Run the application
if __name__ == "__main__":
    analyzer = TMDBMovieAnalyzer()
    analyzer.run()

