import pandas as pd
import json

def clean():
    with open("data/raw.json") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Safety check
    if df.empty:
        print("No data to clean")
        return

    # Clean price (robust extraction)
    df["price"] = df["price"].str.extract(r'(\d+\.\d+)').astype(float)

    # Clean availability
    df["availability"] = df["availability"].str.replace("\n", "").str.strip()

    # Handle missing values
    df.fillna("Unknown", inplace=True)

    df.to_csv("data/clean.csv", index=False)

    print("Data cleaned")

if __name__ == "__main__":
    clean()