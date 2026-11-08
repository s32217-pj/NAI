from utility import *

DATA_FILENAME = "data.json"

def main():
    data = extract_json(DATA_FILENAME)
    user_matrix = create_user_matrix(data)
    sim_matrix = create_similarity_matrix(user_matrix)
    
    all_labels = get_all_unique_labels(data)
    labels_mapped = map_labels(all_labels)
    reverse_labels_mapping = reverse_map_labels(labels_mapped)
    
    recommend = return_recommendations(0, user_matrix, sim_matrix, how_many=5, min_similarity=0.2)
    
    #print(all_labels)
    #print(sim_matrix)
    #print(labels_mapped)
    
    for rci in recommend:
        print(reverse_labels_mapping[rci])
    #print(reverse_labels_mapping[recommend[0]])
    print(recommend)

if __name__ == "__main__":
    main()