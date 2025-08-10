import re
import string
from collections import Counter
from textblob import TextBlob
import textstat

# ------------------------------
# File Reading
# ------------------------------
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():
                print("Error: File is empty.")
                return ""
            return content
    except FileNotFoundError:
        print("Error: File not found. Please check the path.")
        return ""

# ------------------------------
# Text Cleaning
# ------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ------------------------------
# Word Frequency
# ------------------------------
def word_frequency(text, top_n=10):
    words = text.split()
    return Counter(words).most_common(top_n)

# ------------------------------
# Keyword Density
# ------------------------------
def keyword_density(text, keyword):
    words = text.split()
    count = words.count(keyword.lower())
    return round((count / len(words)) * 100, 2) if words else 0

# ------------------------------
# Readability Scores
# ------------------------------
def readability_scores(text):
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "SMOG Index": textstat.smog_index(text),
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(text),
        "Dale-Chall Score": textstat.dale_chall_readability_score(text)
    }

# ------------------------------
# Sentiment Analysis
# ------------------------------
def sentiment_analysis(text):
    blob = TextBlob(text)
    return {"Polarity": blob.sentiment.polarity, "Subjectivity": blob.sentiment.subjectivity}

# ------------------------------
# Pattern Matching
# ------------------------------
def find_pattern(text, pattern):
    return re.findall(pattern, text)

# ------------------------------
# Main Menu
# ------------------------------
def main():
    filepath = input("Enter the path to your text file: ").strip()
    raw = read_file(filepath)
    if not raw:
        return

    cleaned = clean_text(raw)

    while True:
        print("\n=== Advanced Text Processor ===")
        print("1. Show Top N Most Frequent Words")
        print("2. Check Keyword Density")
        print("3. Show Readability Scores")
        print("4. Perform Sentiment Analysis")
        print("5. Find Email Addresses")
        print("6. Show Cleaned Text")
        print("7. Exit")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            try:
                n = int(input("Enter N (number of top words): "))
                for word, count in word_frequency(cleaned, n):
                    print(f"{word}: {count}")
            except ValueError:
                print("Invalid number.")

        elif choice == "2":
            keyword = input("Enter the keyword: ").strip()
            print(f"Keyword Density of '{keyword}': {keyword_density(cleaned, keyword)}%")

        elif choice == "3":
            for name, score in readability_scores(raw).items():
                print(f"{name}: {score}")

        elif choice == "4":
            for name, val in sentiment_analysis(raw).items():
                print(f"{name}: {val}")

        elif choice == "5":
            emails = find_pattern(raw, r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}")
            if emails:
                print("Emails found:", ", ".join(emails))
            else:
                print("No emails found.")

        elif choice == "6":
            print("\nCleaned Text:\n", cleaned)

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select from 1-7.")

if __name__ == "__main__":
    main()
