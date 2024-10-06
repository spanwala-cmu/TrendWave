import requests
import pandas as pd
import json
import time

def scrape_google_trends():
    url = "https://trends.google.com/trends/api/dailytrends?hl=en-GB&tz=-480&geo=US&ns=15"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

    json_data = response.text[5:]
    data = json.loads(json_data)

    trends = []
    for topic in data['default']['trendingSearchesDays'][0]['trendingSearches']:
        title = topic['title']['query']
        search_volume = topic['formattedTraffic']
        trend_breakdown = ", ".join([article['title'] for article in topic.get('articles', [])])
        trends.append({
            "Title": title, 
            "Search Volume": search_volume,
            "Trend Breakdown": trend_breakdown
        })

    return trends

def export_to_csv(trends):
    df = pd.DataFrame(trends)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"google_trends_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

if __name__ == "__main__":
    try:
        trends_data = scrape_google_trends()
        if trends_data:
            export_to_csv(trends_data)
        else:
            print("No trend data found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")