#!/bin/bash

# Start FastAPI in background
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit
streamlit run src/ui/app.py --server.port 8501 --server.address 0.0.0.0
