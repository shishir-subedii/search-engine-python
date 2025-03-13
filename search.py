import pandas as pd
import nltk
import re
from collections import defaultdict

# Download stopwords from NLTK
nltk.download("stopwords")
from nltk.corpus import stopwords

CSV_FILE = "crawled_data.csv"

# Load Wikipedia data
def load_data():
    try:
        df = pd.read_csv(CSV_FILE)
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# Preprocess text (remove special characters, lowercase, remove stopwords)
def preprocess_text(text):
    stop_words = set(stopwords.words("english"))
    text = re.sub(r"[^\w\s]", "", str(text).lower())  # Remove punctuation
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    return words

# Create an inverted index from the dataset
def build_inverted_index(df):
    index = defaultdict(set)
    for i, row in df.iterrows():
        words = preprocess_text(row["Title"]) + preprocess_text(row["Meta Description"])
        for word in words:
            index[word].add(i)
    return index

# Search function
def search_wikipedia(prompt, df, inverted_index):
    query_words = preprocess_text(prompt)
    result_indices = set()

    for word in query_words:
        if word in inverted_index:
            result_indices.update(inverted_index[word])

    # Rank results by number of matched words
    ranked_results = sorted(result_indices, key=lambda x: len(set(preprocess_text(df.iloc[x]["Title"] + " " + df.iloc[x]["Meta Description"])) & set(query_words)), reverse=True)

    # Show top 10 results
    print("\n🔍 Top 10 Results:\n")
    for rank, idx in enumerate(ranked_results[:10], 1):
        print(f"{rank}. {df.iloc[idx]['Title']} ({df.iloc[idx]['URL']})")
    if not ranked_results:
        print("No results found.")

# Main function
def main():
    df = load_data()
    if df is None:
        return

    inverted_index = build_inverted_index(df)

    while True:
        query = input("\nEnter search query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        search_wikipedia(query, df, inverted_index)

if __name__ == "__main__":
    main()
