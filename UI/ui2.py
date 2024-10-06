import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from Analysis.most_trending_hash import *

class SocialMediaAnalyzerUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Social Media Analyzer")
        self.master.geometry("800x600")

        self.reddit_df = None
        self.instagram_df = None

        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.master, text="Load Reddit Data", command=self.load_reddit_data).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Load Instagram Data", command=self.load_instagram_data).grid(row=0, column=1, padx=5, pady=5)

        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.reddit_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reddit_tab, text="Reddit Analysis")
        ttk.Button(self.reddit_tab, text="Plot Top Subreddits", command=self.plot_top_subreddits).pack(pady=5)
        ttk.Button(self.reddit_tab, text="Plot Average Score Distribution", command=self.plot_average_score_distribution).pack(pady=5)

        self.instagram_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.instagram_tab, text="Instagram Analysis")
        ttk.Button(self.instagram_tab, text="Plot Trending Hashtags", command=self.plot_trending_hashtags).pack(pady=5)
        ttk.Button(self.instagram_tab, text="Plot Hashtag Reach vs Frequency", command=self.plot_hashtag_reach_vs_frequency).pack(pady=5)

        self.trending_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trending_tab, text="Trending Probability")
        ttk.Label(self.trending_tab, text="Enter caption:").pack(pady=5)
        self.caption_entry = ttk.Entry(self.trending_tab, width=50)
        self.caption_entry.pack(pady=5)
        ttk.Button(self.trending_tab, text="Check Trending Probability", command=self.check_trending_probability).pack(pady=5)
        self.probability_label = ttk.Label(self.trending_tab, text="")
        self.probability_label.pack(pady=5)

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def load_reddit_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.reddit_df = pd.read_csv(file_path)
            messagebox.showinfo("Success", "Reddit data loaded successfully")

    def load_instagram_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.instagram_df = pd.read_csv(file_path)
            messagebox.showinfo("Success", "Instagram data loaded successfully")

    def plot_top_subreddits(self):
        if self.reddit_df is None:
            messagebox.showerror("Error", "Please load Reddit data first")
            return
        fig = plot_top_subreddits(self.reddit_df)
        self.show_plot(fig)

    def plot_average_score_distribution(self):
        if self.reddit_df is None:
            messagebox.showerror("Error", "Please load Reddit data first")
            return
        fig = plot_average_score_distribution(self.reddit_df)
        self.show_plot(fig)

    def plot_trending_hashtags(self):
        if self.instagram_df is None:
            messagebox.showerror("Error", "Please load Instagram data first")
            return
        ignore_list = ['instagram', 'reelsinstagram', 'trending', 'viral', 'trend', 'new']
        fig = plot_trending_hashtags(self.instagram_df, ignore_list)
        self.show_plot(fig)

    def plot_hashtag_reach_vs_frequency(self):
        if self.instagram_df is None:
            messagebox.showerror("Error", "Please load Instagram data first")
            return
        ignore_list = ['instagram', 'reelsinstagram', 'trending', 'viral', 'trend', 'new']
        fig = plot_hashtag_reach_vs_frequency(self.instagram_df, ignore_list)
        self.show_plot(fig)

    def check_trending_probability(self):
        if self.instagram_df is None:
            messagebox.showerror("Error", "Please load Instagram data first")
            return
        caption = self.caption_entry.get()
        if not caption:
            messagebox.showerror("Error", "Please enter a caption")
            return
        trending_probability = check_trending_probability(caption, self.instagram_df)
        self.probability_label.config(text=f"Trending Probability: {trending_probability:.2f}")

    def show_plot(self, fig):
        plot_window = tk.Toplevel(self.master)
        plot_window.title("Plot")
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaAnalyzerUI(root)
    root.mainloop()