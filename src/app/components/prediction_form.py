import streamlit as st
import pandas as pd
import numpy as np
from src.ml.model import predict_yield

class PredictionForm:
    def __init__(self):
        self.crop_types = ["Rice", "Wheat", "Maize", "Potato", "Cotton", "Sugarcane"]
        self.soil_types = ["Clay", "Sandy", "Loamy", "Black", "Red", "Alluvial"]
        self.fertilizer_types = ["Nitrogen", "Phosphorus", "Potassium", "NPK Mix", "Organic"]
        self.irrigation_methods = ["Drip", "Sprinkler", "Flood", "Furrow", "Rainfed"]
        
    def show_form(self):
        """Display the prediction form and return the prediction result"""
        with st.form("prediction_form"):
            st.subheader("Enter Field Parameters")
            
            # Create a two-column layout for the form
            col1, col2 = st.columns(2)
            
            with col1:
                # Crop selection
                crop_type = st.selectbox("Crop Type", options=self.crop_types)
                
                # Environmental factors
                temperature = st.slider("Average Temperature (°C)", min_value=10.0, max_value=40.0, value=25.0, step=0.5)
                rainfall = st.slider("Annual Rainfall (mm)", min_value=500, max_value=5000, value=1200, step=50)
                humidity = st.slider("Average Humidity (%)", min_value=30, max_value=95, value=60, step=5)
                ph_value = st.slider("Soil pH", min_value=3.0, max_value=9.0, value=6.5, step=0.1)
            
            with col2:
                # Soil and farming practice details
                soil_type = st.selectbox("Soil Type", options=self.soil_types)
                fertilizer_type = st.selectbox("Fertilizer Type", options=self.fertilizer_types)
                irrigation_method = st.selectbox("Irrigation Method", options=self.irrigation_methods)
                
                # Additional parameters
                nitrogen = st.slider("Nitrogen Content (kg/ha)", min_value=0, max_value=200, value=80)
                phosphorus = st.slider("Phosphorus Content (kg/ha)", min_value=0, max_value=200, value=60)
                potassium = st.slider("Potassium Content (kg/ha)", min_value=0, max_value=200, value=40)
            
            # Area information
            area = st.number_input("Field Area (hectares)", min_value=0.1, max_value=1000.0, value=5.0, step=0.1)
            
            # Submit button
            submit_button = st.form_submit_button("Predict Yield")
            
            if submit_button:
                # Prepare input data for the model
                input_data = {
                    'crop_type': crop_type,
                    'temperature': temperature,
                    'rainfall': rainfall,
                    'humidity': humidity,
                    'ph': ph_value,
                    'soil_type': soil_type,
                    'fertilizer_type': fertilizer_type,
                    'irrigation_method': irrigation_method,
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium,
                    'area': area
                }
                
                # Call the prediction model
                try:
                    prediction_result = predict_yield(input_data)
                    # In a real application, prediction_result would come from the model
                    # For now, we'll simulate a result
                    
                    # Simulated result (should be replaced with actual model output)
                    simulated_result = {
                        'yield': 4.5 + np.random.normal(0, 0.5),  # Random value around 4.5
                        'confidence': 85 + np.random.normal(0, 5)  # Random value around 85%
                    }
                    
                    return simulated_result
                    
                except Exception as e:
                    st.error(f"Error making prediction: {str(e)}")
                    return None
                    
        # Return None if the form wasn't submitted
        return None 