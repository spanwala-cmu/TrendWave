import praw
from datetime import datetime
import pandas as pd

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id="lRBcY04zo2E109eji9sa3g",
    client_secret="ZYDtmqLmxRjtSmEdZn3uyLGnmw990Q",
    user_agent="mac:myredditapp:v1.0",
    username="Honest-Protection997",
    password="Pass@1372#"
)

# Fetch trendy topics from r/all
print("Fetching trendy topics from across Reddit...")
records = []

for post in reddit.subreddit('all').hot(limit=1000):
    record = {
        "Title": post.title,
        "Subreddit": str(post.subreddit),
        "Subreddit Subscribers": post.subreddit.subscribers,
        "Author": str(post.author),
        "Score": post.score,
        "Upvote Ratio": post.upvote_ratio,
        "Number of Comments": post.num_comments,
        "Awards": len(post.all_awardings),
        "URL": post.url,
        "Created": datetime.fromtimestamp(post.created_utc),
        "Is Self Post": post.is_self,
        "Over 18": post.over_18
    }
    records.append(record)
    
    if len(records) % 100 == 0:
        print(f"Fetched {len(records)} records...")

# Convert records to a DataFrame
records_df = pd.DataFrame(records)

# Save to CSV
csv_filename = 'trendy_reddit_topics.csv'
try:
    records_df.to_csv(csv_filename, index=False)
    print(f'Successfully saved {len(records)} records to {csv_filename}')
except Exception as e:
    print(f'Error saving CSV: {e}')