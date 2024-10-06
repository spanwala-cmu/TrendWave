import requests
from bs4 import BeautifulSoup

def scrape_trending_topics():
    # URL of the trends24.in website for US trends
    url = "https://trends24.in/united-states/"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the list of trending topics
        trending_list = soup.find('ol', class_='trend-card__list')
        
        # Extract and print the trending topics
        if trending_list:
            trends = trending_list.find_all('a')
            print("Current trending topics in the US:")
            for i, trend in enumerate(trends, 1):
                print(f"{i}. {trend.text.strip()}")
        else:
            print("No trending topics found.")
    else:
        print("Failed to retrieve the webpage.")

# Run the scraping function
scrape_trending_topics()