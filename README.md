# Competitor Pricing Intelligence Pipeline

## Overview

Businesses constantly need visibility into competitor pricing to make informed decisions on strategy, positioning, and market response. However, such data is rarely available in a structured, ready-to-use format.

This project builds an **end-to-end automated data pipeline** that collects, processes, and delivers pricing data in a way that is directly usable by businesses.

## Project Highlights

- End-to-end automated data pipeline  
- Real-time API with business insights  
- Deployed live on cloud (Render)  
- Production-style logging and modular design  

## Problem Statement

Organizations often lack:

* Real-time access to competitor pricing
* Structured datasets for analysis
* Automated systems to continuously gather and update market data

This results in **inefficient decision-making** and missed opportunities.



## Solution

This project implements a **Pricing Intelligence Pipeline** that:

1. **Scrapes** publicly available product data (including pricing)
2. **Cleans and standardizes** raw data for consistency
3. **Stores** processed data in a structured database
4. **Exposes** the data through an API for real-world usage
5. **Adds insights** to help businesses interpret pricing trends



## Architecture


Scraper → Raw Data (JSON) → Data Cleaning → Database (SQLite) → FastAPI → Business API Endpoints

This pipeline ensures smooth data flow from raw extraction to actionable business insights.


## Features

- Automated web scraping with pagination support  
- Data cleaning and normalization pipeline  
- SQLite-based structured data storage  
- REST API built with FastAPI  
- Filtering and sorting capabilities  
- Business insights (average price, segmentation)  
- Lightweight intelligence layer for price categorization  
- Fully deployed and accessible via public URL  

### API Preview

Below are sample responses and endpoints demonstrating the functionality of the deployed API:

#### Swagger UI

Shows all the available endpoints


<img width="1350" height="566" alt="image" src="https://github.com/user-attachments/assets/b5227b09-e901-4384-8ced-86cdaf91727d" />


#### Fetch Books Endpoint

Returns structured product data.


<img width="1293" height="441" alt="image" src="https://github.com/user-attachments/assets/dd148690-4754-4777-b476-95e8d0fbbf40" />


#### Price Filtering

Demonstrates filtering based on price range.


<img width="1298" height="388" alt="image" src="https://github.com/user-attachments/assets/74ff504e-42db-426a-834a-e6d1ff179c76" />


#### Sorted Results

Displays books sorted in ascending or descending order


<img width="1301" height="323" alt="image" src="https://github.com/user-attachments/assets/fcf9e66f-36a1-41ce-89cd-39f9a72adbde" />


#### Price Category

Categorizes books based on price segments

<img width="1289" height="441" alt="image" src="https://github.com/user-attachments/assets/1ee2c0a0-189e-4b5d-94ca-a232ec50ef30" />


#### Insights Endpoint

Provides business insights from data.

<img width="1292" height="165" alt="image" src="https://github.com/user-attachments/assets/6775c1a7-4d25-4448-bee1-c6469b15818e" />


## Data Collection

* Handles pagination across multiple pages
* Extracts product title, price, and availability
* Gracefully handles scraping errors

## Data Cleaning

* Removes encoding inconsistencies
* Standardizes price formats
* Handles missing or inconsistent values

## Data Storage

* Stores cleaned data in SQLite database
* Structured schema for efficient querying

## API Layer

Built using FastAPI with the following endpoints:

* `/` → Health check
* `/books` → Fetch product data
* `/books/filter` → Filter products by price range
* `/insights/avg-price` → Average pricing insight
* `/insights/price-category` → Categorized pricing segments
* `/insights/category-summary` → Distribution of pricing tiers

## Intelligent Layer (AI-lite)

A lightweight intelligence layer categorizes products into:

* Budget
* Mid-range
* Premium

This helps simulate **market segmentation analysis** used in real-world business scenarios.

---

## Design Decisions & Trade-offs

* **SQLite over Postgres**: Chosen for simplicity and quick setup within time constraints
* **Limited pagination scope**: Ensures faster execution while demonstrating scalability
* **Regex-based cleaning**: More robust than simple string replacement for handling encoding issues
* **API over UI**: Prioritized backend usability over frontend due to time constraints



## Automation

The pipeline is fully automated and can be executed using a single command:

```bash
python run_pipeline.py
```

It can be further scheduled using cron jobs or task schedulers to ensure continuous data updates.

---

## Tech Stack

* Python
* BeautifulSoup (Web Scraping)
* Pandas (Data Processing)
* SQLite (Database)
* FastAPI (API Layer)

---

## How to Run Locally

# 1. Clone the repository

```bash
git clone <your-repo-link>
cd pricing-intelligence-pipeline
```

# 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

# 3. Install dependencies

```bash
pip install -r requirements.txt
```

# 4. Run the pipeline

```bash
python run_pipeline.py
```

# 5. Start the API

```bash
uvicorn api.main:app --reload
```

# 6. Access API

* Swagger UI: http://127.0.0.1:8000/docs
* Base URL: http://127.0.0.1:8000



# Example Use Cases

* Competitor price tracking
* Market positioning analysis
* Pricing trend monitoring
* Product segmentation



# Future Improvements

* Expand to multiple data sources
* Add historical price tracking
* Build a frontend dashboard for visualization


# **Live API Links**

- **Base URL:** https://pricing-intelligence-pipeline.onrender.com  
- **API Documentation (Swagger UI):** https://pricing-intelligence-pipeline.onrender.com/docs


# Conclusion

This project demonstrates the design and implementation of a **practical, production-oriented data pipeline**. It focuses not only on data collection but also on **usability, automation, and business value delivery**.



