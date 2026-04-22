#!/bin/bash
python run_pipeline.py
uvicorn api.main:app --host 0.0.0.0 --port 10000