# print("Book Recommender System")
from fastapi import FastAPI, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = FastAPI()

books = pd.read_csv("data/books.csv")

books["combined_text"] = books["genre"] + " " + books["description"]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(books["combined_text"])

similarity_matrix = cosine_similarity(tfidf_matrix)


def recommend_books(book_title):
    # Find the index of the selected books
    matching_books = books[books["title"].str.lower() == book_title.lower()]

    if matching_books.empty:
        raise HTTPException(status_code=404, detail="book not found")

    book_index = matching_books.index[0]

    # Get similarity score for the selected book
    similarity_scores = similarity_matrix[book_index]

    # Create pairs of (index, similarity score)
    book_scores = list(enumerate(similarity_scores))

    # Sort by similarity score from highest to lowest
    book_scores = sorted(book_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 similar books, excluding the selected book
    recommendation = []

    for index, score in book_scores[1:6]:
        book = books.iloc[index]
        recommendation.append({
            "title" : book["title"],
            "genre" : book["genre"],
            "description" : book["description"],
            "similarity" : round(float(score), 2)
        })

    return recommendation


@app.get("/")
def home():
    return {"msg" : "Book recommender System"}

@app.get("/books")
def view_books():
    data = books.to_dict(orient="records")
    return data

@app.get("/books/{book}")
def get_book(book : str):
    data = books.to_dict(orient="records")
    book = book.lower()

    for item in data:
        if item["title"].lower() == book:
            return item
        

    raise HTTPException(status_code=404, detail="book not found")


@app.get("/genres")
def genres():

    return list(books["genre"].unique())


@app.get("/recommend/{book}")
def recommend(book : str):

    data = recommend_books(book)

    return {
        "book" : book,
        "recommendations" : data
        }



    