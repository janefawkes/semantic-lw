import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_cleaned_articles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        cleaned_articles = json.load(f)
    return cleaned_articles

def semantic_search(query, cleaned_articles, top_k=5):
    corpus = [article['clean_contents'] for article in cleaned_articles]

    # Vectorize the corpus using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Vectorize the query
    query_vector = vectorizer.transform([query])

    # Calculate cosine similarity between query and documents
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)

    # Get indices of top-k most similar documents
    top_indices = similarity_scores.argsort()[0][-top_k:][::-1]

    # Return top-k most relevant articles
    top_articles = [cleaned_articles[i] for i in top_indices]
    return top_articles

def main():
    cleaned_articles_file = 'cleaned_articles.json'
    cleaned_articles = load_cleaned_articles(cleaned_articles_file)

    query = "probability"

    top_articles = semantic_search(query, cleaned_articles)

    print(f"Query: {query}")

    for idx, article in enumerate(top_articles, start=1):
        print(f"Rank {idx}: {article['title']} (ID: {article['_id']})")

if __name__ == "__main__":
    main()
