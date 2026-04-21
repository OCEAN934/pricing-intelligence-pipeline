from sqlalchemy import create_engine
import pandas as pd

def load_to_db():
    engine = create_engine("sqlite:///books.db")

    df = pd.read_csv("data/clean.csv")

    df.to_sql("books", engine, if_exists="replace", index=False)

    print("Data loaded to DB")

if __name__ == "__main__":
    load_to_db()