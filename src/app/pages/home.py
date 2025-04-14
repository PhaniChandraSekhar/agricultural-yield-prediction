import streamlit as st

def show_home():
    st.header("Welcome to Crop Yield Prediction System")
    
    st.write("""
    This application helps farmers predict crop yields based on various environmental 
    and agricultural factors. Use the navigation menu to explore different features.
    """)
    
    st.subheader("Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Predict Crop Yields")
        st.write("Input your farm data to get yield predictions")
        
        st.markdown("### View Historical Data")
        st.write("Access and analyze past yield records")
    
    with col2:
        st.markdown("### Climate Analysis")
        st.write("See how climate factors affect crop production")
        
        st.markdown("### Recommendation System")
        st.write("Get personalized farming suggestions")
    
    st.info("Select an option from the sidebar to get started.") 