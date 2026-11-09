from utility import *

DATA_FILENAME = "data.json"

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
    
    print("I recommend: ")
    for idx in recommend:
        print(f"- {reverse_labels_mapping[idx]}")
    
    print("\nI do not recommend")
    for idx in do_not_recommend:
        print(f"- {reverse_labels_mapping[idx]}")

if __name__ == "__main__":
    main()