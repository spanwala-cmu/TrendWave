import requests
import pandas as pd
import json
import time

def scrape_google_trends():
    base_url = "https://trends.google.com/trends/api/dailytrends"
    params = {
        "hl": "en-GB",
        "tz": "-480",
        "geo": "US",
        "ns": "15"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    all_trends = []
    date = None

    while True:
        if date:
            params["ed"] = date

        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break

        json_data = response.text[5:]
        data = json.loads(json_data)

        if not data['default']['trendingSearchesDays']:
            break

        for day in data['default']['trendingSearchesDays']:
            date = day['date']
            for topic in day['trendingSearches']:
                title = topic['title']['query']
                search_volume = topic['formattedTraffic']
                trend_breakdown = ", ".join([article['title'] for article in topic.get('articles', [])])
                all_trends.append({
                    "Date": date,
                    "Title": title, 
                    "Search Volume": search_volume,
                    "Trend Breakdown": trend_breakdown
                })

        print(f"Fetched data for {date}")
        time.sleep(1)  # Add a delay to avoid rate limiting

    return all_trends

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