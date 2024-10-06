import requests
import json
from datetime import datetime
import time

def fetch_trending_topics(subreddit='all', time_filter='day'):
    url = f'https://www.reddit.com/r/{subreddit}/top/.json?t={time_filter}'
    headers = {'User-Agent': 'TrendPredictor/1.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        trending_topics = []
        for post in data['data']['children']:
            post_data = post['data']
            topic = {
                'title': post_data['title'],
                'subreddit': post_data['subreddit'],
                'score': post_data['score'],
                'num_comments': post_data['num_comments'],
                'created_utc': post_data['created_utc'],
                'url': post_data['url']
            }
            trending_topics.append(topic)
        
        return trending_topics
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending topics: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text[:200]}")  # Print first 200 characters
        return []

def fetch_comments(post_url):
    url = f'{post_url}.json'
    headers = {'User-Agent': 'TrendPredictor/1.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        comments = []
        for comment in data[1]['data']['children']:
            if comment['kind'] == 't1':
                comment_data = comment['data']
                comments.append({
                    'body': comment_data['body'],
                    'score': comment_data['score'],
                    'created_utc': comment_data['created_utc']
                })
        
        return comments
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text[:200]}")  # Print first 200 characters
        return []

def analyze_trends(trending_topics, comment_threshold=100):
    analyzed_trends = []
    for topic in trending_topics:
        if topic['num_comments'] > comment_threshold:
            comments = fetch_comments(topic['url'])
            topic['top_comments'] = sorted(comments, key=lambda x: x['score'], reverse=True)[:5]
            analyzed_trends.append(topic)
        time.sleep(1)  # Add a delay to avoid rate limiting
    
    return analyzed_trends

# Main execution
if __name__ == '__main__':
    trending_topics = fetch_trending_topics(subreddit='all', time_filter='day')
    if trending_topics:
        analyzed_trends = analyze_trends(trending_topics)
        print(json.dumps(analyzed_trends, indent=2))
    else:
        print("No trending topics fetched. Check the error messages above.")