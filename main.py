# print("Book Recommender System")
from fastapi import FastAPI, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

app = FastAPI()

books = pd.read_csv("data/books.csv")

books["combined_text"] = books["genre"] + " " + books["description"]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(books["combined_text"])
print(tfidf_matrix.shape)

print(books[["title", "combined_text"]])

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

