import json
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import unicodedata

def load_articles_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    return articles

def clean_text(text):
    # Remove HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text(separator=' ')

    # Remove ambiguous UNICODE characters
    clean_text = unicodedata.normalize('NFKD', clean_text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    return clean_text

def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens

def main():
    articles_file = 'articles.json'
    cleaned_articles = []

    articles = load_articles_from_file(articles_file)
    for article in articles:
        if article.get('contents') and isinstance(article['contents'], dict) and 'html' in article['contents']:
            cleaned_contents = clean_text(article['contents']['html'])
            cleaned_article = {
                '_id': article['_id'],
                'title': article['title'],
                'createdAt': article['createdAt'],
                'clean_contents': cleaned_contents,
                'tokens': tokenize_text(cleaned_contents)
            }
            cleaned_articles.append(cleaned_article)

    with open('cleaned_articles.json', 'w') as f:
        json.dump(cleaned_articles, f, indent=4)

if __name__ == "__main__":
    main()
