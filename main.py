# print("Book Recommender System")
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List

app = FastAPI()

books = pd.read_csv("data/books.csv")

books["combined_text"] = books["title"] + " " + books["genre"] + " " + books["description"]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(books["combined_text"])

similarity_matrix = cosine_similarity(tfidf_matrix)

threshold = 0.10

class Book_Recommendation(BaseModel):

    title: str
    genre: str
    description: str
    similarity: float

class Recommendation_Response(BaseModel):

    book: str
    recommendations: List[Book_Recommendation]

class Query_Recommendation_Response(BaseModel):

    query: str
    recommendations: List[Book_Recommendation]
    message: str | None = None

def recommend_books(book_title):
    # Find the index of the selected books
    matching_books = books[books["title"].str.lower() == book_title.lower()]

    if matching_books.empty:
        raise HTTPException(status_code=404, detail=f"book '{book_title}' not found")

    book_index = matching_books.index[0]

    # Get similarity score for the selected book
    similarity_scores = similarity_matrix[book_index]

    # Create pairs of (index, similarity score)
    book_scores = list(enumerate(similarity_scores))

    # Sort by similarity score from highest to lowest
    book_scores = sorted(book_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 similar books, excluding the selected book
    recommendation = []

    for index, score in book_scores[1:]:
        if score >= threshold:
            book = books.iloc[index]
            recommendation.append({
                "title" : book["title"],
                "genre" : book["genre"],
                "description" : book["description"],
                "similarity" : round(float(score), 2)
            })

        if len(recommendation) == 5:
            break


    return recommendation

def recommend_by_query(query):

    query_vector = vectorizer.transform([query])

    similarity_scores = cosine_similarity(
        query_vector,
        tfidf_matrix
    )[0]

    book_scores = list(enumerate(similarity_scores))

    book_scores = sorted(
        book_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendation = []

    for index, score in book_scores:
        if score >= threshold:
            book = books.iloc[index]

            recommendation.append({
                "title": book["title"],
                "genre": book["genre"],
                "description": book["description"],
                "similarity": round(float(score), 2)
            })

        if len(recommendation) == 5:
            break

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
    original_book = book
    book = book.lower()

    for item in data:
        if item["title"].lower() == book:
            return item
        

    raise HTTPException(status_code=404, detail=f"book '{original_book}' not found")


@app.get("/genres")
def genres():

    return list(books["genre"].unique())


@app.get("/recommend/{book}",response_model=Recommendation_Response)
def recommend(book : str):

    data = recommend_books(book)

    return {
        "book" : book,
        "recommendations" : data
        }

@app.get("/recommend",response_model=Query_Recommendation_Response)
def recommend_by_user_query(query : str = Query(..., min_length=3, description="Minimum 3 characters are required")):
    data = recommend_by_query(query)

    if not data:
        return {
            "query" : query,
            "recommendations" : [],
            "message" : "No suitable books found for this query."
        }

    return {
        "query" : query,
        "recommendations" : data,
        "message" : "Books found successfully."
    }

    