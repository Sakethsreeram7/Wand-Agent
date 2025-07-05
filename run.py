#!/usr/bin/env python3
"""
Wand Agent - Main Entry Point

This script serves as the main entry point for the Wand Agent application.
It can run either the FastAPI backend server or the Streamlit web interface.
"""

import sys
import os
import argparse

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_api_server():
    """Run the FastAPI backend server"""
    import uvicorn
    from app.main import app
    
    print("🚀 Starting Wand Agent API Server...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_streamlit_app():
    """Run the Streamlit web interface"""
    import subprocess
    import sys
    
    print("🌍 Starting Wand Agent Web Interface...")
    print("📍 Web app will be available at: http://localhost:8501")
    
    # Run streamlit with the app file
    cmd = [sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py"]
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="Wand Agent Application")
    parser.add_argument(
        "mode", 
        choices=["api", "web", "streamlit"], 
        help="Run mode: 'api' for FastAPI server, 'web' or 'streamlit' for Streamlit interface"
    )
    
    args = parser.parse_args()
    
    if args.mode == "api":
        run_api_server()
    elif args.mode in ["web", "streamlit"]:
        run_streamlit_app()

if __name__ == "__main__":
    main()
