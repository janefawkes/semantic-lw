import requests
import json

def fetch_all_articles():
    url = "https://www.lesswrong.com/graphql"
    articles = []
    has_more = True
    offset = 0
    limit = 50
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    while has_more:
        query = f"""
        {{
          posts(input: {{limit: {limit}, offset: {offset}}}) {{
            results {{
              _id
              title
              contents {{
                html
              }}
              createdAt
            }}
            totalCount
          }}
        }}
        """
        
        response = requests.post(url, json={'query': query}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'posts' in data['data']:
                batch_articles = data['data']['posts']['results']
                articles.extend(batch_articles)
                offset += limit
                total_count = data['data']['posts'].get('totalCount', None)
                has_more = total_count is not None and offset < total_count
            else:
                print("Unexpected response structure:", data)
                break
        else:
            print(f"Failed to fetch articles. Status code: {response.status_code}")
            print(response.text)
            break
    
    return articles

def save_articles_to_json(articles, filename='articles.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    articles = fetch_all_articles()
    if articles:
        save_articles_to_json(articles)
        print(f"Fetched and saved {len(articles)} articles to articles.json")
    else:
        print("No articles fetched")
