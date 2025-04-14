import streamlit as st
# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Agricultural Yield Prediction",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import os
import sys
import random
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import components
from src.app.components.yield_form import YieldPredictionForm
from src.app.components.prediction_results import PredictionResults

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #388E3C;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #81C784;
    }
    .info-text {
        color: #1B5E20;
        font-size: 1.2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)


def mock_model_prediction(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock function to simulate model prediction.
    This will be replaced with actual model integration.
    
    Args:
        input_data: Dictionary containing form inputs
        
    Returns:
        Dictionary containing prediction results
    """
    # Generate a random yield prediction based on the crop type
    base_yield = {
        "Wheat": 3.5,
        "Rice": 4.0,
        "Maize": 5.5,
        "Potato": 25.0,
        "Tomato": 35.0,
        "Barley": 3.0,
        "Soybean": 2.5,
        "Cotton": 1.8,
        "Sugarcane": 70.0
    }.get(input_data["crop_type"], 4.0)
    
    # Add some random variation
    predicted_yield = base_yield * (0.8 + 0.4 * random.random()) * input_data["field_area"]
    
    # Generate confidence score
    confidence = random.uniform(65, 95)
    
    # Generate factor importance
    factors = [
        "Temperature", "Rainfall", "Humidity", 
        "Soil Type", "Soil pH", "Nitrogen", 
        "Phosphorus", "Potassium", "Fertilizer", "Irrigation"
    ]
    
    # Generate random importance scores
    factor_importance = {}
    total = 0
    for factor in factors:
        factor_importance[factor] = random.uniform(0.05, 0.2)
        total += factor_importance[factor]
    
    # Normalize to sum to 1
    for factor in factor_importance:
        factor_importance[factor] = factor_importance[factor] / total
    
    # Return results
    return {
        "predicted_yield": predicted_yield,
        "confidence": confidence,
        "factor_importance": factor_importance,
        "input_data": input_data
    }


def main():
    """Main function to run the Streamlit application."""
    # Display header
    st.markdown('<h1 class="main-header">Agricultural Yield Prediction System</h1>', unsafe_allow_html=True)
    st.markdown(
        """
        This application helps farmers predict crop yields based on various environmental and agricultural factors.
        Enter your field parameters below to get a yield prediction and recommendations for improvement.
        """
    )
    
    # Create tabs
    tabs = st.tabs(["Prediction", "About", "Help"])
    
    with tabs[0]:
        # Create prediction form
        st.markdown("---")
        yield_form = YieldPredictionForm()
        input_data, submitted = yield_form.show_form()
        
        # Handle form submission
        if submitted:
            # Show loading spinner
            with st.spinner("Processing your data..."):
                # In a real app, this would call your ML model
                prediction_results = mock_model_prediction(input_data)
            
            # Display results
            st.markdown("---")
            results_component = PredictionResults()
            results_component.show_results(
                prediction_results["predicted_yield"],
                prediction_results["confidence"],
                prediction_results["factor_importance"],
                prediction_results["input_data"]
            )
    
    with tabs[1]:
        st.markdown("## About This Application")
        st.markdown(
            """
            ### Agricultural Yield Prediction System

            This application uses machine learning algorithms to predict crop yields based on various environmental 
            and agricultural factors. It provides farmers with valuable insights to optimize their farming practices 
            and improve productivity.

            #### Key Features:
            - Accurate yield predictions for various crops
            - Analysis of factors affecting crop yield
            - Personalized recommendations for yield improvement
            - Easy-to-use interface for data input and visualization

            #### Technology Stack:
            - **Frontend**: Streamlit
            - **Backend**: Python
            - **Machine Learning**: Scikit-learn, TensorFlow
            - **Data Processing**: Pandas, NumPy
            - **Visualization**: Plotly, Matplotlib

            #### Dataset:
            The prediction model is trained on a comprehensive dataset that includes historical crop yield data, 
            weather patterns, soil characteristics, and farming practices from various agricultural regions.
            """
        )

    with tabs[2]:
        st.markdown("## Help & User Guide")
        st.markdown(
            """
            ### How to Use This Application

            #### Step 1: Enter Your Field Parameters
            - Select your crop type
            - Enter the area of your field
            - Provide climate information (temperature, rainfall, humidity)
            - Enter soil characteristics (type, pH, nutrient levels)
            - Specify your farming practices (fertilizer type, irrigation method)

            #### Step 2: Get Your Prediction
            - Click the "Predict Yield" button
            - Review the predicted yield and confidence level
            - Examine the factor analysis to understand what impacts your yield

            #### Step 3: Implement Recommendations
            - Review the personalized recommendations
            - Prioritize actions based on potential impact
            - Track your changes and compare predictions over time

            #### Tips for Accurate Predictions:
            - Provide as much accurate information as possible
            - Update your data regularly throughout the growing season
            - Compare predictions with actual yields to understand performance
            """
        )


if __name__ == "__main__":
    main() 