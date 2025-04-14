import numpy as np
import pandas as pd
import random
from typing import Dict, Any, Tuple

def predict_yield(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict crop yield based on input parameters.
    
    This is a mock implementation that will be replaced with an actual ML model.
    
    Args:
        input_data: Dictionary containing input parameters
        
    Returns:
        Dictionary containing prediction results
    """
    try:
        # Base yield values for different crops (tons/hectare)
        base_yields = {
            "Rice": 4.5,
            "Wheat": 3.0,
            "Maize": 5.5,
            "Potato": 25.0,
            "Cotton": 2.2,
            "Sugarcane": 70.0
        }
        
        # Get base yield for the crop type
        crop_type = input_data.get('crop_type', 'Wheat')
        base_yield = base_yields.get(crop_type, 3.5)
        
        # Apply modifiers based on input parameters
        # Temperature modifier
        temp = input_data.get('temperature', 25.0)
        temp_modifier = 1.0
        if temp < 15.0 or temp > 35.0:
            temp_modifier = 0.8
        
        # Rainfall modifier
        rainfall = input_data.get('rainfall', 1000)
        rainfall_modifier = 1.0
        if rainfall < 600 or rainfall > 3000:
            rainfall_modifier = 0.9
        
        # Soil pH modifier
        ph = input_data.get('ph', 6.5)
        ph_modifier = 1.0
        if ph < 5.0 or ph > 8.0:
            ph_modifier = 0.85
        
        # Nutrient modifiers
        nitrogen = input_data.get('nitrogen', 50)
        phosphorus = input_data.get('phosphorus', 30)
        potassium = input_data.get('potassium', 40)
        
        nutrient_modifier = 0.7 + (0.3 * (
            min(nitrogen / 100, 1.0) + 
            min(phosphorus / 80, 1.0) + 
            min(potassium / 80, 1.0)
        ) / 3.0)
        
        # Calculate predicted yield with all modifiers
        predicted_yield = base_yield * temp_modifier * rainfall_modifier * ph_modifier * nutrient_modifier
        
        # Add some random variation (±15%)
        predicted_yield *= (0.85 + random.random() * 0.3)
        
        # Generate a confidence level (65-95%)
        confidence = 65 + random.random() * 30
        
        return {
            'yield': round(predicted_yield, 2),
            'confidence': round(confidence, 1)
        }
    
    except Exception as e:
        print(f"Error in yield prediction: {str(e)}")
        # Return a fallback prediction in case of errors
        return {
            'yield': 0.0,
            'confidence': 0.0,
            'error': str(e)
        }

def gaussian_effect(value, optimal, width):
    """
    Calculate effect based on a Gaussian curve.
    Maximum effect (1.0) at the optimal value, decreasing as value moves away.
    
    Args:
        value: Input value
        optimal: Value at which effect is maximized
        width: Controls how quickly effect drops off
        
    Returns:
        Effect value between 0 and 1
    """
    return np.exp(-((value - optimal) ** 2) / (2 * width ** 2))

def sigmoid_effect(value, threshold, steepness):
    """
    Calculate effect based on a sigmoid curve.
    Effect increases as value increases, with most rapid change near threshold.
    
    Args:
        value: Input value
        threshold: Value at which effect is 0.5
        steepness: Controls how quickly effect changes near threshold
        
    Returns:
        Effect value between 0 and 1
    """
    return 1 / (1 + np.exp(-steepness * (value - threshold))) 