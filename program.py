from utility import *
import requests
import textwrap

DATA_FILENAME = "data.json"
OMDB_API_KEY = "67bf71c0" #DO NOT STEAL PLS

def main():
    data = extract_json(DATA_FILENAME)
    user_matrix = create_user_matrix(data)
    sim_matrix = create_similarity_matrix(user_matrix)
    
    all_labels = get_all_unique_labels(data)
    labels_mapped = map_labels(all_labels)
    reverse_labels_mapping = reverse_map_labels(labels_mapped)
    
    all_users = get_all_users(data)
    users_mapped = map_users(all_users)
    reverse_users_mapping = reverse_map_users(users_mapped)
    
    #recommend = return_recommendations(0, user_matrix, sim_matrix, how_many=5, min_similarity=0.2)
    
    username = input("Jak się nazywasz?\n").strip().lower()
    
    if username not in data:
        print(f"Sory Dolores, takiego imienia jak \"{username}\" nie ma w naszej bazie danych")
        exit(0)
        
    user_idx = users_mapped[username]
    recommend = return_best_recommendations(user_idx, user_matrix, sim_matrix, how_many=5, min_similarity=0.2)
    do_not_recommend = return_worst_recommendations(user_idx, user_matrix, sim_matrix, how_many=5, min_similarity=0.2)
    
    print("Polecam: ")
    for idx in recommend:
        print(f"- {reverse_labels_mapping[idx]}")
        print_movie_info(search_movie(reverse_labels_mapping[idx]))
        print("\n", '-'*50, "\n")
    
    print("\nNie polecam:")
    for idx in do_not_recommend:
        print(f"- {reverse_labels_mapping[idx]}")
        print_movie_info(search_movie(reverse_labels_mapping[idx]))
        print("\n", '-'*50, "\n")
        
def search_movie(movie_name: str):
    response = requests.get(
        "https://www.omdbapi.com/",
        params={
            "apikey": OMDB_API_KEY,
            "t": movie_name,
            "plot": "full"
        }
    )

    response.raise_for_status()
    data = response.json()

    if data.get("Response") == "False":
        return None

    return data

#Funkcja wygenerowana przez AI
def print_movie_info(movie: dict | None):
    if movie is None:
        print("Nie znaleziono filmu. Być może film ma literówka, lub jego tytuł jest po polsku?")
        return

    width = 65

    def print_field(label: str, value: str):
        print(f"  {label:<17} {value}")

    def print_section(title: str):
        print(f"\n  [{title}]")

    title = movie.get("Title", "Brak tytułu")
    year = movie.get("Year", "N/A")

    print("\n" + "=" * width)
    print(f"  {title.upper()} ({year})")
    print("=" * width)

    print_section("INFORMACJE")

    print_field("Gatunek:", movie.get("Genre", "N/A"))
    print_field("Czas trwania:", movie.get("Runtime", "N/A"))
    print_field("Reżyser:", movie.get("Director", "N/A"))
    print_field("Scenariusz:", movie.get("Writer", "N/A"))
    print_field("Kraj:", movie.get("Country", "N/A"))
    print_field("Premiera:", movie.get("Released", "N/A"))

    print_section("OBSADA")
    print(textwrap.fill(
        movie.get("Actors", "Brak danych"),
        width=width - 4,
        initial_indent="  ",
        subsequent_indent="  "
    ))

    print_section("OCENY")

    imdb_rating = movie.get("imdbRating", "N/A")
    imdb_votes = movie.get("imdbVotes", "N/A")

    print_field("IMDb:", f"{imdb_rating}/10")
    print_field("Liczba głosów:", imdb_votes)

    ratings = movie.get("Ratings", [])

    for rating in ratings:
        print_field(
            rating.get("Source", "Inne"),
            rating.get("Value", "N/A")
        )

    print_section("OPIS")

    plot = movie.get("Plot", "Brak opisu")

    print(textwrap.fill(
        plot,
        width=width - 4,
        initial_indent="  ",
        subsequent_indent="  "
    ))

    awards = movie.get("Awards", "N/A")

    if awards != "N/A":
        print_section("NAGRODY")
        print(textwrap.fill(
            awards,
            width=width - 4,
            initial_indent="  ",
            subsequent_indent="  "
        ))

    print("\n" + "=" * width)

if __name__ == "__main__":
    main()