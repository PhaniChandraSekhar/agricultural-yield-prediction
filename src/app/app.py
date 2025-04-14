import streamlit as st

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Agricultural Yield Prediction",
    page_icon="🌾",
    layout="wide"
)

# Other imports
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def main():
    st.title("Streamlit App")
    st.write("Welcome to my Streamlit application!")
    
    # Add sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox("Choose a page", ["Home", "About", "Data"])
    
    # Display different content based on page selection
    if page == "Home":
        st.header("Home")
        st.write("This is the home page of the application.")
    elif page == "About":
        st.header("About")
        st.write("This application was created as part of a capstone project.")
    elif page == "Data":
        st.header("Data")
        st.write("Data visualization will be displayed here.")

if __name__ == "__main__":
    main() 