import os

os.system("python -m scraper.scraper")
os.system("python -m processing.clean_data")
os.system("python -m database.db")