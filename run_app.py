#!/usr/bin/env python
import os
import sys
import streamlit.web.cli as stcli

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def main():
    """Run the Streamlit app."""
    # Using a different port to avoid conflicts
    port = os.environ.get("PORT", "8502")  # Use env variable or default to 8502
    
    # Set command line arguments for Streamlit
    sys.argv = ["streamlit", "run", "src/app/main.py", 
                f"--server.port={port}", 
                "--server.address=0.0.0.0",
                "--server.headless=true"]
    
    # Exit with Streamlit CLI's exit code
    sys.exit(stcli.main())

if __name__ == "__main__":
    main() 