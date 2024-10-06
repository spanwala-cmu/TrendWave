import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Data preprocessing function
def preprocess_data(reddit_data, instagram_data):
    # Processing Reddit data
    reddit_df = pd.DataFrame(reddit_data)
    reddit_df['Created'] = pd.to_datetime(reddit_df['Created'])
    reddit_df.fillna(method='ffill', inplace=True)
    reddit_df['Score'] = reddit_df['Score'].astype(int)

    # Processing Instagram data
    instagram_df = pd.DataFrame(instagram_data)
    instagram_df['Timestamp'] = pd.to_datetime(instagram_df['Timestamp'])

    return reddit_df, instagram_df

def get_trending_hashtags_by_frequency(instagram_df, ignore_hashtags=None):
    if ignore_hashtags is None:
        ignore_hashtags = []
    ignore_hashtags = [tag.lower() for tag in ignore_hashtags]

    hashtag_data = []
    for _, post in instagram_df.iterrows():
        hashtags = post['Post Hashtags']
        if isinstance(hashtags, str):
            hashtag_list = [tag.strip().lower() for tag in hashtags.split(',')]
            hashtag_data.extend([tag for tag in hashtag_list if tag not in ignore_hashtags])

    hashtag_df = pd.DataFrame(hashtag_data, columns=['Hashtag'])
    trending_hashtags = hashtag_df['Hashtag'].value_counts().reset_index()
    trending_hashtags.columns = ['Hashtag', 'Frequency']

    return trending_hashtags

def get_trending_hashtags_by_reach(instagram_df, ignore_hashtags=None):
    if ignore_hashtags is None:
        ignore_hashtags = []
    ignore_hashtags = [tag.lower() for tag in ignore_hashtags]

    hashtag_data = []
    for _, post in instagram_df.iterrows():
        hashtags = post['Post Hashtags']
        likes = post['Likes']
        comments = post['Comments']
        if isinstance(hashtags, str):
            hashtag_list = [tag.strip().lower() for tag in hashtags.split(',')]
            hashtag_data.extend([(tag, likes, comments) for tag in hashtag_list if tag not in ignore_hashtags])

    hashtag_df = pd.DataFrame(hashtag_data, columns=['Hashtag', 'Likes', 'Comments'])
    
    hashtag_counts = hashtag_df.groupby('Hashtag').agg({'Likes': 'sum', 'Comments': 'sum'}).reset_index()
    hashtag_counts['Occurrences'] = hashtag_df.groupby('Hashtag')['Likes'].count().values
    hashtag_counts['Reach'] = (hashtag_counts['Likes'] + hashtag_counts['Comments']) / hashtag_counts['Occurrences']
    
    sorted_hashtags = hashtag_counts.sort_values(by='Reach', ascending=False)
    
    return sorted_hashtags

# Reddit KPIs
def get_top_subreddits_by_engagement(reddit_df):
    subreddit_data = reddit_df.groupby('Subreddit').agg({
        'Score': 'sum', 
        'Upvote Ratio': 'mean', 
        'Number of Comments': 'sum'
    }).reset_index()
    subreddit_data['Engagement'] = (subreddit_data['Score'] + subreddit_data['Number of Comments']) / subreddit_data['Upvote Ratio']
    sorted_data = subreddit_data.sort_values(by='Engagement', ascending=False)
    return sorted_data[['Subreddit', 'Score', 'Engagement']].head(10)

def get_average_score_per_subreddit(reddit_df):
    return reddit_df.groupby('Subreddit')['Score'].mean().reset_index().sort_values(by='Score', ascending=False)

# Instagram KPIs
def get_average_likes_comments_per_post(instagram_df):
    return instagram_df[['Likes', 'Comments']].mean()

def get_top_posts_by_engagement(instagram_df):
    instagram_df['Total Engagement'] = instagram_df['Likes'] + instagram_df['Comments']
    return instagram_df.sort_values(by='Total Engagement', ascending=False).reset_index(drop=True)

# Visualization functions
def plot_top_subreddits(reddit_df):
    top_subreddits = get_top_subreddits_by_engagement(reddit_df).head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(top_subreddits['Subreddit'], top_subreddits['Engagement'])
    plt.title('Top 10 Subreddits by Engagement')
    plt.xlabel('Subreddit')
    plt.ylabel('Engagement Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_average_score_distribution(reddit_df):
    avg_scores = get_average_score_per_subreddit(reddit_df).head(5)
    plt.figure(figsize=(10, 10))
    plt.pie(avg_scores['Score'], labels=avg_scores['Subreddit'], autopct='%1.1f%%')
    plt.title('Average Score Distribution Among Top 5 Subreddits')
    plt.axis('equal')
    plt.show()

def plot_trending_hashtags(instagram_df, ignore_list):
    trending_by_frequency = get_trending_hashtags_by_frequency(instagram_df, ignore_hashtags=ignore_list)
    top_hashtags = trending_by_frequency.head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top_hashtags['Hashtag'], top_hashtags['Frequency'])
    plt.title('Top 10 Trending Hashtags by Frequency')
    plt.xlabel('Frequency')
    plt.ylabel('Hashtag')
    plt.tight_layout()
    plt.show()

def plot_hashtag_reach_vs_frequency(instagram_df, ignore_list):
    trending_by_reach = get_trending_hashtags_by_reach(instagram_df, ignore_hashtags=ignore_list)
    plt.figure(figsize=(12, 8))
    plt.scatter(trending_by_reach['Occurrences'], trending_by_reach['Reach'])
    plt.title('Hashtag Reach vs. Frequency')
    plt.xlabel('Frequency (Occurrences)')
    plt.ylabel('Reach')
    plt.xscale('log')
    plt.yscale('log')
    for i, txt in enumerate(trending_by_reach['Hashtag'].head(10)):
        plt.annotate(txt, (trending_by_reach['Occurrences'].iloc[i], trending_by_reach['Reach'].iloc[i]))
    plt.tight_layout()
    plt.show()
    
def check_trending_probability(caption, instagram_df):
    # Extract hashtags from the caption
    hashtags = re.findall(r'#[\w]+', caption)
    
    # Clean the caption by removing hashtags
    clean_caption = re.sub(r'#[\w]+', '', caption).strip()
    
    # Get the top posts by engagement
    top_posts = instagram_df.sort_values(by='Likes', ascending=False).head(10)
    top_captions = top_posts['Caption'].fillna('')
    
    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    all_texts = [clean_caption] + top_captions.tolist()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Compute cosine similarity between the clean caption and the top captions
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    caption_correlation_score = np.max(cosine_similarities)
    
    # Get trending hashtags
    trending_hashtags = get_trending_hashtags_by_reach(instagram_df)
    top_trending_hashtags = set(trending_hashtags['Hashtag'].head(10).tolist())
    
    # Calculate hashtag score
    relevant_hashtags = len(set(hashtags) & top_trending_hashtags)
    irrelevant_hashtags = len(set(hashtags) - top_trending_hashtags)
    hashtag_score = relevant_hashtags / len(hashtags) if hashtags else 0
    
    # Deduct score for irrelevant hashtags
    deduction = 0.1 * irrelevant_hashtags  # Penalty for each irrelevant hashtag
    hashtag_score = max(hashtag_score - deduction, 0)
    
    # Combine scores with weights
    caption_weight = 0.6
    hashtag_weight = 0.4
    combined_score = (caption_correlation_score * caption_weight) + (hashtag_score * hashtag_weight)
    
    # Ensure the score is between 0 and 1
    combined_score = np.clip(combined_score, 0, 1)
    
    return combined_score

# Main execution
if __name__ == "__main__":
    # Reading the CSV files
    reddit_df = pd.read_csv("Reddit/trendy_reddit_topics.csv")
    instagram_df = pd.read_csv("instagram_posts.csv")

    # Preprocess the data
    preprocessed_reddit, preprocessed_instagram = preprocess_data(reddit_df, instagram_df)

    # List of hashtags to ignore (example)
    ignore_list = ['instagram', 'reelsinstagram', 'trending', 'viral', 'trend', 'new']

    # # Generate visualizations
    # plot_top_subreddits(preprocessed_reddit)
    # plot_average_score_distribution(preprocessed_reddit)
    # plot_trending_hashtags(preprocessed_instagram, ignore_list)
    # plot_hashtag_reach_vs_frequency(preprocessed_instagram, ignore_list)

    # Print KPIs
    print("Reddit KPIs:")
    print("\nTop Subreddits by Engagement:")
    print(get_top_subreddits_by_engagement(preprocessed_reddit).head())

    print("\nAverage Score per Subreddit:")
    print(get_average_score_per_subreddit(preprocessed_reddit).head())

    print("\nInstagram KPIs:")
    trending_by_frequency = get_trending_hashtags_by_frequency(preprocessed_instagram, ignore_hashtags=ignore_list)
    print("Top 10 Trending Hashtags by Frequency:")
    print(trending_by_frequency.head(10))

    trending_by_reach = get_trending_hashtags_by_reach(preprocessed_instagram, ignore_hashtags=ignore_list)
    print("\nTop 10 Trending Hashtags by Reach:")
    print(trending_by_reach.head(10))

    print("\nAverage Likes and Comments per Post:")
    print(get_average_likes_comments_per_post(preprocessed_instagram))

    print("\nTop Posts by Engagement:")
    print(get_top_posts_by_engagement(preprocessed_instagram).head())
    
    # Example usage of check_trending_probability function
    print("\nTrending Probability Check:")
    example_caption = "Enjoying a beautiful sunset at the beach #nature #sunset #beachlife"
    trending_probability = check_trending_probability(example_caption, preprocessed_instagram)
    print(f"Caption: {example_caption}")
    print(f"Trending Probability: {trending_probability:.2f}")
    
        # You can also test multiple captions
    test_captions = [
        "Delicious homemade pizza for dinner tonight! #foodie #homecooking",
        "Just finished my first marathon! Feeling accomplished #fitness #running",
        "New tech gadget unboxing video coming soon #technology #unboxing",
        "Breathtaking sunset at the beach! #nature #beach #sunset #instagood"
    ]

    print("\nTesting Multiple Captions:")
    for caption in test_captions:
        prob = check_trending_probability(caption, preprocessed_instagram)
        print(f"Caption: {caption}")
        print(f"Trending Probability: {prob:.2f}\n")