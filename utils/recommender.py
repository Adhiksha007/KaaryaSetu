import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def get_recommendations(user_input, model, tfidf_matrix, data):
    user_vec = model.transform([user_input])
    cosine_sim = cosine_similarity(user_vec, tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i for i, _ in sim_scores]
    matches = data.iloc[top_indices].copy()
    matches["match_percent"] = [round(score * 100, 2) for _, score in sim_scores]
    return matches
