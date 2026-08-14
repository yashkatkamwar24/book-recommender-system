# print("Book Recommender System")

import pandas as pd

books = pd.read_csv("data/books.csv")

# print(books)
print(books.shape)
print(books.head())
print(books.columns)
print(books.isnull().sum())

import nltk

nltk.download("punkt")
nltk.download("punkt_tab")

from nltk.tokenize import word_tokenize

text = "I want adventure books"

words = word_tokenize(text)

print(words)