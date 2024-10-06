import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import StringIO
from Analysis.most_trending_hash import *

# Import all functions from the original code
# (Assuming all the functions from the original code are available)

class SocialMediaAnalyzerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Social Media Analyzer")
        self.master.geometry("800x600")

        # Load and preprocess data
        reddit_df = pd.read_csv("Reddit/trendy_reddit_topics.csv")
        instagram_df = pd.read_csv("instagram_posts.csv")
        self.preprocessed_reddit, self.preprocessed_instagram = preprocess_data(reddit_df, instagram_df)
        self.ignore_list = ['instagram', 'reelsinstagram', 'trending', 'viral', 'trend', 'new']

        # Create tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.reddit_tab = ttk.Frame(self.notebook)
        self.instagram_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reddit_tab, text="Reddit")
        self.notebook.add(self.instagram_tab, text="Instagram")

        self.create_reddit_tab()
        self.create_instagram_tab()

    def create_reddit_tab(self):
        # KPIs
        kpi_frame = ttk.LabelFrame(self.reddit_tab, text="Reddit KPIs")
        kpi_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        top_subreddits = get_top_subreddits_by_engagement(self.preprocessed_reddit).head()
        avg_scores = get_average_score_per_subreddit(self.preprocessed_reddit).head()

        self.create_table(kpi_frame, "Top Subreddits by Engagement", top_subreddits)
        self.create_table(kpi_frame, "Average Score per Subreddit", avg_scores)

        # Plots
        plot_frame = ttk.Frame(self.reddit_tab)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(plot_frame, text="Show Top Subreddits Plot", command=self.show_top_subreddits_plot).pack(pady=5)
        ttk.Button(plot_frame, text="Show Average Score Distribution", command=self.show_avg_score_distribution).pack(pady=5)

    def create_instagram_tab(self):
        # KPIs
        kpi_frame = ttk.LabelFrame(self.instagram_tab, text="Instagram KPIs")
        kpi_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        trending_by_frequency = get_trending_hashtags_by_frequency(self.preprocessed_instagram, ignore_hashtags=self.ignore_list).head(10)
        trending_by_reach = get_trending_hashtags_by_reach(self.preprocessed_instagram, ignore_hashtags=self.ignore_list).head(10)
        avg_likes_comments = get_average_likes_comments_per_post(self.preprocessed_instagram)
        top_posts = get_top_posts_by_engagement(self.preprocessed_instagram).head()

        self.create_table(kpi_frame, "Top 10 Trending Hashtags by Frequency", trending_by_frequency)
        self.create_table(kpi_frame, "Top 10 Trending Hashtags by Reach", trending_by_reach)
        self.create_table(kpi_frame, "Average Likes and Comments per Post", pd.DataFrame([avg_likes_comments]))
        self.create_table(kpi_frame, "Top Posts by Engagement", top_posts)

        # Plots
        plot_frame = ttk.Frame(self.instagram_tab)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(plot_frame, text="Show Trending Hashtags Plot", command=self.show_trending_hashtags_plot).pack(pady=5)
        ttk.Button(plot_frame, text="Show Hashtag Reach vs Frequency Plot", command=self.show_hashtag_reach_vs_frequency_plot).pack(pady=5)

    def create_table(self, parent, title, data):
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tree = ttk.Treeview(frame, columns=list(data.columns), show="headings")
        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for _, row in data.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill=tk.BOTH, expand=True)

    def show_plot(self, plot_func, *args):
        plot_window = tk.Toplevel(self.master)
        plot_window.title("Plot")
        plot_window.geometry("800x600")

        fig, ax = plt.subplots(figsize=(10, 6))
        plot_func(*args)
        
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_top_subreddits_plot(self):
        self.show_plot(plot_top_subreddits, self.preprocessed_reddit)

    def show_avg_score_distribution(self):
        self.show_plot(plot_average_score_distribution, self.preprocessed_reddit)

    def show_trending_hashtags_plot(self):
        self.show_plot(plot_trending_hashtags, self.preprocessed_instagram, self.ignore_list)

    def show_hashtag_reach_vs_frequency_plot(self):
        self.show_plot(plot_hashtag_reach_vs_frequency, self.preprocessed_instagram, self.ignore_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaAnalyzerUI(root)
    root.mainloop()