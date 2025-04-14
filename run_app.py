#!/usr/bin/env python
import os
import sys
import streamlit.web.cli as stcli

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def main():
    """Run the Streamlit app."""
    sys.argv = ["streamlit", "run", "src/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main() 