import os

os.system("python scraper/scraper.py")
os.system("python processing/clean_data.py")
os.system("python database/db.py")