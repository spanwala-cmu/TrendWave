import praw
from datetime import datetime

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id="lRBcY04zo2E109eji9sa3g",
    client_secret="ZYDtmqLmxRjtSmEdZn3uyLGnmw990Q",
    user_agent="mac:myredditapp:v1.0",
    username="Honest-Protection997",
    password="Pass@1372#"
)

# Fetch and display trendy topics from r/all
print("Trendy topics from across Reddit:\n")
for i, post in enumerate(reddit.subreddit('all').hot(limit=20), 1):
    print(f"{i}. Title: {post.title}")
    print(f"   Subreddit: r/{post.subreddit}")
    print(f"   Subreddit Subscribers: {post.subreddit.subscribers}")
    print(f"   Author: {post.author}")
    print(f"   Score: {post.score}")
    print(f"   Upvote Ratio: {post.upvote_ratio}")
    print(f"   Number of Comments: {post.num_comments}")
    print(f"   Awards: {len(post.all_awardings)}")
    print(f"   URL: {post.url}")
    print(f"   Created: {datetime.fromtimestamp(post.created_utc)}")
    print(f"   Is Original Content: {post.is_original_content}")
    print(f"   Is Self Post: {post.is_self}")
    print(f"   Over 18: {post.over_18}")
    print("---")