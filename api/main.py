from fastapi import FastAPI
import sqlite3
import os

app = FastAPI(
    title="Pricing Intelligence API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# 🔥 Ensure database exists (for deployment)
if not os.path.exists("books.db"):
    print("Database not found. Running pipeline...")
    os.system("python run_pipeline.py")


# Database connection
def get_db():
    return sqlite3.connect("books.db")


# Home route
@app.get("/")
def home():
    return {"message": "Pricing Intelligence API is running successfully"}


# Get all books
@app.get("/books")
def get_books():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT title, price, availability FROM books LIMIT 20")
    rows = cursor.fetchall()

    conn.close()

    return {
        "data": [
            {"title": r[0], "price": r[1], "availability": r[2]}
            for r in rows
        ]
    }


# Filter books by price range
@app.get("/books/filter")
def filter_books(min_price: float = 0, max_price: float = 1000):
    conn = get_db()
    cursor = conn.cursor()

    query = """
    SELECT title, price, availability 
    FROM books 
    WHERE price BETWEEN ? AND ?
    """

    cursor.execute(query, (min_price, max_price))
    rows = cursor.fetchall()

    conn.close()

    return {
        "data": [
            {"title": r[0], "price": r[1], "availability": r[2]}
            for r in rows
        ]
    }


# Sort books by price
@app.get("/books/sorted")
def sort_books(order: str = "asc"):
    conn = get_db()
    cursor = conn.cursor()

    if order == "desc":
        query = "SELECT title, price, availability FROM books ORDER BY price DESC"
    else:
        query = "SELECT title, price, availability FROM books ORDER BY price ASC"

    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()

    return {
        "data": [
            {"title": r[0], "price": r[1], "availability": r[2]}
            for r in rows
        ]
    }


# Insight: Average price
@app.get("/insights/avg-price")
def avg_price():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(price) FROM books")
    avg = cursor.fetchone()[0]

    conn.close()

    return {"average_price": round(avg, 2) if avg else 0}


# AI-lite: Price categorization
@app.get("/insights/price-category")
def price_category():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT title, price FROM books")
    rows = cursor.fetchall()

    conn.close()

    result = []

    for title, price in rows:
        if price < 20:
            category = "Budget"
        elif price < 40:
            category = "Mid-range"
        else:
            category = "Premium"

        result.append({
            "title": title,
            "price": price,
            "category": category
        })

    return {"data": result}


# AI-lite: Category summary
@app.get("/insights/category-summary")
def category_summary():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT price FROM books")
    rows = cursor.fetchall()

    conn.close()

    summary = {
        "Budget": 0,
        "Mid-range": 0,
        "Premium": 0
    }

    for (price,) in rows:
        if price < 20:
            summary["Budget"] += 1
        elif price < 40:
            summary["Mid-range"] += 1
        else:
            summary["Premium"] += 1

    return summary