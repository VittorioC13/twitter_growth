"""
Vercel serverless function entry point
This wraps the Flask app for Vercel deployment
"""
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import web_interface
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the Flask app
from web_interface import app

# Vercel expects the app to be named 'app' or to have a handler
# The Flask app is already named 'app' so we're good
