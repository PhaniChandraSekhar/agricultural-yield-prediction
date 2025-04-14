import streamlit as st
import numpy as np
import pandas as pd
from src.app.components.prediction_form import PredictionForm

def show_prediction():
    st.header("Crop Yield Prediction")
    
    st.write("""
    Use this tool to predict crop yields based on environmental conditions and farming practices.
    Fill in the form below with your data to get a prediction.
    """)
    
    # Initialize the prediction form component
    prediction_form = PredictionForm()
    
    # Display the form and get prediction results
    prediction_result = prediction_form.show_form()
    
    # Display prediction results if available
    if prediction_result is not None:
        st.subheader("Prediction Results")
        
        # Display the predicted yield
        st.metric(label="Predicted Yield (tons/hectare)", 
                  value=f"{prediction_result['yield']:.2f}")
        
        # Show additional details or confidence metrics
        st.write(f"Prediction Confidence: {prediction_result['confidence']:.1f}%")
        
        # Show a bar chart of factors influencing the prediction
        st.subheader("Factors Influencing Prediction")
        
        # Example chart using dummy data - in a real app, this would come from the model
        influence_data = pd.DataFrame({
            'Factor': ['Temperature', 'Rainfall', 'Soil Quality', 'Fertilizer'],
            'Importance': [0.35, 0.25, 0.20, 0.20]
        })
        
        st.bar_chart(influence_data.set_index('Factor'))
        
        # Additional recommendation based on the prediction
        if prediction_result['yield'] < 3.0:
            st.warning("Your predicted yield is below average. Consider adjusting your farming practices.")
        else:
            st.success("Your predicted yield looks good!") 