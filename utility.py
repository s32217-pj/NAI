import json
import numpy as np
import math

RATING_MIN = 1
RATING_MAX = 10
EMPTY_VALUE = 0

def extract_json(filename: str):
    """Extracts data from json into dictionary"""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    #convert all films to lower case, users also
    return {
        user.strip().lower(): {
            movie.strip().lower(): rating
            for movie, rating in ratings.items()
        }
        for user, ratings in data.items()
    }


def get_all_unique_labels(data) -> list[str]:
    """Get all unique labels from data."""
    return list({
        name
        for ratings in data.values()
        for name in ratings.keys()
    })
    
def get_all_users(data) -> list[str]:
    """Get all unique usernames from data"""
    return list({ name for name in data.keys() })

def map_users(users: list[str]) -> dict[str, int]:
    """Create users mapped into matrix rows."""
    return {user: idx for idx, user in enumerate(users)}

def reverse_map_users(mapped_users: dict[str, int]) -> dict[int, str]:
    """Create reverse mapping from matrix rows to usernames"""
    return { idx : user for idx, user in mapped_users.items()}

def map_labels(labels: list[str]) -> dict[str, int]:
    """Create labels mapped into matrix columns."""
    return {label: idx for idx, label in enumerate(labels)}

def reverse_map_labels(mapped_labels: dict[str, int]) -> dict[int, str]:
    """Create reverse mapping from matrix columns to labels."""
    return {idx: label for label, idx in mapped_labels.items()}

def dot_product(vec1: list[int], vec2: list[int]) -> int:
    """Calculates dot product of 2 vectors, if vectors do not have the same length error is thrown"""
    assert len(vec1) == len(vec2), "Lengths of vectors must be the same"
    
    return sum(v1 * v2 for v1, v2 in zip(vec1, vec2))



def cosine_similarity(vec1: list[int], vec2: list[int]):
    """Calculates cosine similarity between 2 vectors of numbers, vectors must be of the same length"""
    
    dot = dot_product(vec1, vec2)
    lv1 = math.sqrt(sum(x**2 for x in vec1)) # length of vector 1 (Euclidean)
    lv2 = math.sqrt(sum(x**2 for x in vec2)) # length of vector 2 (Euclidean)
    
    return dot/(lv1*lv2)


def create_user_matrix(data: any):
    """Creates user matrix using data, data has to be in json. Empty values in user matrix are of type EMPTY_VALUE"""
    
    mapped_labels = map_labels(get_all_unique_labels(data))
    
    users = list(data.keys())
    
    user_matrix = np.full(
        (len(users), len(mapped_labels)), EMPTY_VALUE,  dtype=float)
    
    for user_idx, user in enumerate(users):
        for movie, rating in data[user].items():
            movie_idx = mapped_labels[movie]
            user_matrix[user_idx][movie_idx] = rating / RATING_MAX #map rating into value [0..1]
            
    return user_matrix
    
    
def create_similarity_matrix(user_matrix):
    similarity_matrix = np.zeros(
        (len(user_matrix), len(user_matrix)), dtype=float)
    
    for i, user_a in enumerate(user_matrix):
        for j, user_b in enumerate(user_matrix):
            similarity_matrix[i][j] = cosine_similarity(user_a, user_b)
            
    return similarity_matrix

def predict_rating(user_idx, movie_idx, user_matrix, similarity_matrix, top_k = 3, min_similarity = 0.5) -> int | None:
    """Predicts rating of movie for given user, using rating of top_k users (default 3) most simillar to the given user
       top_k users must have similarity score >= min_similarity to improve rating, you can set this to 0, to omit this.
       Returns None if prediction cannot be done (no similarities found for example)
    """
    
    assert top_k < len(user_matrix), "top_k must be less than len(user_matrix)"
    
    sim_vec = similarity_matrix[user_idx].copy()
    sim_vec[user_idx] = -10001000 #we do not want to compare ratings of ourselves
    
    top_k_users_idx = np.argsort(sim_vec, descending=True)[:top_k:]
    
    valid_ratings = [ (user_matrix[idx][movie_idx], sim_vec[idx])
                        for idx in top_k_users_idx
                        if sim_vec[idx] >= min_similarity
                        and user_matrix[idx][movie_idx] != EMPTY_VALUE ] #returns ratings and similarity score for each rating
    
    if not valid_ratings:
        return None
    
    ratings, similarities = zip(*valid_ratings)
    
    if np.sum(np.abs(similarities)) == 0:
        return None
    
    prediction = np.sum(np.array(ratings) * np.array(np.abs(similarities))) / np.sum(similarities)
    return prediction
    
    
def return_recommendations(user_idx,user_matrix, sim_matrix, min_similarity = 0.3) -> list[tuple[int, int]]:
    """Returns tuple containing recommended films and their prediction that they will match user"""
    user_vector = user_matrix[user_idx]
    
    recommendations = {} #id : prediction, choose top k
    
    for movie_idx, rating in enumerate(user_vector):
        if rating == EMPTY_VALUE:
            prediction = predict_rating(user_idx, movie_idx, user_matrix, sim_matrix, top_k=2, min_similarity=min_similarity)
            if prediction is not None:  recommendations[movie_idx] = prediction
            
    return recommendations

def return_best_recommendations(user_idx,user_matrix, sim_matrix, how_many=3, min_similarity = 0.3):
    recommendations_all = return_recommendations(user_idx, user_matrix, sim_matrix, min_similarity)
    
    top_recommendations = sorted(
        recommendations_all.items(),
        key=lambda item: item[1],
        reverse=True
    )[:how_many]

    return [movie_idx for movie_idx, _ in top_recommendations]

def return_worst_recommendations(user_idx,user_matrix, sim_matrix, how_many=3, min_similarity = 0.3):
    recommendations_all = return_recommendations(user_idx, user_matrix, sim_matrix, min_similarity)
    
    top_recommendations = sorted(
        recommendations_all.items(),
        key=lambda item: item[1],
        reverse=False
    )[:how_many]

    return [movie_idx for movie_idx, _ in top_recommendations]
    
     
     
            
    
            

    
    
    
    

    
    
    

        
