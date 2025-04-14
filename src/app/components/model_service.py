import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, List, Optional
import random


class ModelService:
    """Service for handling yield prediction model functionality."""
    
    def __init__(self):
        """Initialize the ModelService."""
        # Model would typically be loaded here in a real application
        self.model_loaded = True
        self.crop_factor_weights = {
            # Sample factor weights for different crops
            "Wheat": {
                "temperature": 0.7, "rainfall": 0.8, "soil_ph": 0.6, 
                "nitrogen_level": 0.75, "phosphorus_level": 0.6, "potassium_level": 0.5,
                "organic_matter": 0.4, "humidity": 0.3, "irrigation_method": 0.65,
                "soil_type": 0.55, "sunlight": 0.45
            },
            "Rice": {
                "temperature": 0.65, "rainfall": 0.9, "soil_ph": 0.5, 
                "nitrogen_level": 0.8, "phosphorus_level": 0.7, "potassium_level": 0.6,
                "organic_matter": 0.3, "humidity": 0.75, "irrigation_method": 0.85,
                "soil_type": 0.6, "sunlight": 0.5
            },
            "Maize": {
                "temperature": 0.75, "rainfall": 0.7, "soil_ph": 0.55, 
                "nitrogen_level": 0.85, "phosphorus_level": 0.65, "potassium_level": 0.55,
                "organic_matter": 0.5, "humidity": 0.4, "irrigation_method": 0.6,
                "soil_type": 0.5, "sunlight": 0.7
            },
            # Default weights for other crops
            "default": {
                "temperature": 0.7, "rainfall": 0.7, "soil_ph": 0.5, 
                "nitrogen_level": 0.7, "phosphorus_level": 0.6, "potassium_level": 0.5,
                "organic_matter": 0.4, "humidity": 0.4, "irrigation_method": 0.6,
                "soil_type": 0.5, "sunlight": 0.6
            }
        }
        
        # Optimal ranges for different parameters by crop
        self.optimal_ranges = {
            "Wheat": {
                "temperature": (15, 24), "rainfall": (450, 650), "soil_ph": (6.0, 7.0),
                "nitrogen_level": (40, 80), "phosphorus_level": (25, 50), "potassium_level": (35, 70),
                "organic_matter": (2.0, 5.0), "humidity": (50, 70)
            },
            "Rice": {
                "temperature": (20, 30), "rainfall": (1000, 1500), "soil_ph": (5.5, 6.5),
                "nitrogen_level": (60, 100), "phosphorus_level": (30, 60), "potassium_level": (40, 80),
                "organic_matter": (2.0, 4.0), "humidity": (60, 80)
            },
            "Maize": {
                "temperature": (18, 27), "rainfall": (500, 800), "soil_ph": (5.8, 7.0),
                "nitrogen_level": (50, 90), "phosphorus_level": (25, 55), "potassium_level": (30, 65),
                "organic_matter": (2.5, 5.0), "humidity": (45, 65)
            },
            # Default optimal ranges
            "default": {
                "temperature": (15, 28), "rainfall": (500, 1000), "soil_ph": (5.5, 7.0),
                "nitrogen_level": (40, 80), "phosphorus_level": (25, 50), "potassium_level": (35, 70),
                "organic_matter": (2.0, 5.0), "humidity": (50, 70)
            }
        }
    
    def predict_yield(self, input_data: Dict[str, Any]) -> Tuple[float, float, Dict[str, float]]:
        """
        Predict crop yield based on input parameters.
        
        Args:
            input_data: Dictionary containing all input parameters
            
        Returns:
            Tuple containing:
                - Predicted yield (tons/acre)
                - Confidence score (0-100)
                - Dictionary of factor importance scores
        """
        # In a real application, this would use a trained ML model
        # For this demo, we'll use a simplified approach with some randomness
        
        # Get crop type and its factor weights
        crop_type = input_data["crop_type"]
        factor_weights = self.crop_factor_weights.get(
            crop_type, self.crop_factor_weights["default"]
        )
        
        # Get optimal ranges for this crop
        optimal_ranges = self.optimal_ranges.get(
            crop_type, self.optimal_ranges["default"]
        )
        
        # Calculate base yield based on ideal conditions for the crop
        base_yields = {
            "Wheat": 3.5, "Rice": 4.2, "Maize": 5.8, "Soybean": 3.0, 
            "Potato": 15.0, "Tomato": 25.0, "Cotton": 1.5, "Sugarcane": 35.0,
            "Barley": 3.2, "Sorghum": 2.8
        }
        base_yield = base_yields.get(crop_type, 4.0)
        
        # Calculate factor scores based on how close each parameter is to its optimal range
        factor_scores = {}
        factor_impacts = {}
        
        # Temperature impact
        temp = input_data["temperature"]
        opt_temp_min, opt_temp_max = optimal_ranges["temperature"]
        if opt_temp_min <= temp <= opt_temp_max:
            factor_scores["temperature"] = 1.0
        else:
            if temp < opt_temp_min:
                dist_from_opt = (opt_temp_min - temp) / opt_temp_min
            else:
                dist_from_opt = (temp - opt_temp_max) / opt_temp_max
            factor_scores["temperature"] = max(0, 1 - dist_from_opt)
        
        # Rainfall impact
        rain = input_data["rainfall"]
        opt_rain_min, opt_rain_max = optimal_ranges["rainfall"]
        if opt_rain_min <= rain <= opt_rain_max:
            factor_scores["rainfall"] = 1.0
        else:
            if rain < opt_rain_min:
                dist_from_opt = (opt_rain_min - rain) / opt_rain_min
            else:
                dist_from_opt = (rain - opt_rain_max) / opt_rain_max
            factor_scores["rainfall"] = max(0, 1 - dist_from_opt)
        
        # Soil pH impact
        ph = input_data["soil_ph"]
        opt_ph_min, opt_ph_max = optimal_ranges["soil_ph"]
        if opt_ph_min <= ph <= opt_ph_max:
            factor_scores["soil_ph"] = 1.0
        else:
            if ph < opt_ph_min:
                dist_from_opt = (opt_ph_min - ph) / 3  # pH scale is small
            else:
                dist_from_opt = (ph - opt_ph_max) / 3
            factor_scores["soil_ph"] = max(0, 1 - dist_from_opt)
        
        # Nitrogen impact
        nitrogen = input_data["nitrogen_level"]
        opt_n_min, opt_n_max = optimal_ranges["nitrogen_level"]
        if opt_n_min <= nitrogen <= opt_n_max:
            factor_scores["nitrogen_level"] = 1.0
        else:
            if nitrogen < opt_n_min:
                dist_from_opt = (opt_n_min - nitrogen) / opt_n_min
            else:
                dist_from_opt = (nitrogen - opt_n_max) / opt_n_max
            factor_scores["nitrogen_level"] = max(0, 1 - dist_from_opt)
        
        # Phosphorus impact
        phosphorus = input_data["phosphorus_level"]
        opt_p_min, opt_p_max = optimal_ranges["phosphorus_level"]
        if opt_p_min <= phosphorus <= opt_p_max:
            factor_scores["phosphorus_level"] = 1.0
        else:
            if phosphorus < opt_p_min:
                dist_from_opt = (opt_p_min - phosphorus) / opt_p_min
            else:
                dist_from_opt = (phosphorus - opt_p_max) / opt_p_max
            factor_scores["phosphorus_level"] = max(0, 1 - dist_from_opt)
        
        # Potassium impact
        potassium = input_data["potassium_level"]
        opt_k_min, opt_k_max = optimal_ranges["potassium_level"]
        if opt_k_min <= potassium <= opt_k_max:
            factor_scores["potassium_level"] = 1.0
        else:
            if potassium < opt_k_min:
                dist_from_opt = (opt_k_min - potassium) / opt_k_min
            else:
                dist_from_opt = (potassium - opt_k_max) / opt_k_max
            factor_scores["potassium_level"] = max(0, 1 - dist_from_opt)
        
        # Organic matter impact
        organic = input_data["organic_matter"]
        opt_org_min, opt_org_max = optimal_ranges["organic_matter"]
        if opt_org_min <= organic <= opt_org_max:
            factor_scores["organic_matter"] = 1.0
        else:
            if organic < opt_org_min:
                dist_from_opt = (opt_org_min - organic) / opt_org_min
            else:
                dist_from_opt = (organic - opt_org_max) / opt_org_max
            factor_scores["organic_matter"] = max(0, 1 - dist_from_opt)
        
        # Humidity impact
        humidity = input_data["humidity"]
        opt_hum_min, opt_hum_max = optimal_ranges["humidity"]
        if opt_hum_min <= humidity <= opt_hum_max:
            factor_scores["humidity"] = 1.0
        else:
            if humidity < opt_hum_min:
                dist_from_opt = (opt_hum_min - humidity) / opt_hum_min
            else:
                dist_from_opt = (humidity - opt_hum_max) / opt_hum_max
            factor_scores["humidity"] = max(0, 1 - dist_from_opt)
        
        # Irrigation method impact
        irrigation_scores = {
            "Drip": 0.95, "Sprinkler": 0.85, "Flood": 0.7, 
            "Furrow": 0.75, "Rainfed": 0.6, "Center Pivot": 0.9,
            "Micro-irrigation": 0.93, None: 0.5
        }
        factor_scores["irrigation_method"] = irrigation_scores.get(
            input_data["irrigation_method"], 0.7
        )
        
        # Soil type impact
        soil_scores = {
            "Sandy": 0.6, "Clay": 0.7, "Loam": 0.9, "Silt": 0.8, 
            "Sandy Loam": 0.85, "Clay Loam": 0.8, "Silty Clay": 0.75, 
            "Sandy Clay": 0.65, "Peaty": 0.7
        }
        factor_scores["soil_type"] = soil_scores.get(input_data["soil_type"], 0.7)
        
        # Sunlight impact (assuming optimal is around 8-10 hours)
        sunlight = input_data["sunlight"]
        if 8 <= sunlight <= 10:
            factor_scores["sunlight"] = 1.0
        else:
            if sunlight < 8:
                dist_from_opt = (8 - sunlight) / 8
            else:
                dist_from_opt = (sunlight - 10) / 6  # Max is 16
            factor_scores["sunlight"] = max(0, 1 - dist_from_opt)
        
        # Calculate weighted yield modification
        yield_modifier = 0
        for factor, score in factor_scores.items():
            factor_weight = factor_weights.get(factor, 0.5)
            yield_modifier += score * factor_weight
            factor_impacts[factor] = score * factor_weight
        
        # Normalize yield modifier
        yield_modifier = yield_modifier / sum(factor_weights.values())
        
        # Calculate predicted yield with some randomness for realism
        randomness = random.uniform(0.9, 1.1)
        predicted_yield = base_yield * yield_modifier * randomness
        
        # Calculate confidence based on how many factors are in optimal range
        optimal_count = sum(1 for score in factor_scores.values() if score > 0.8)
        confidence = (optimal_count / len(factor_scores)) * 100
        
        # Add some randomness to confidence (real models have uncertainty)
        confidence = min(95, confidence * random.uniform(0.9, 1.05))
        
        # Sort factors by importance
        factor_importance = {k: v for k, v in sorted(
            factor_impacts.items(), key=lambda item: item[1], reverse=True
        )}
        
        return predicted_yield, confidence, factor_importance
    
    def get_historical_data(self, crop_type: str) -> pd.DataFrame:
        """
        Get historical yield data for comparison.
        
        Args:
            crop_type: Type of crop to get historical data for
            
        Returns:
            DataFrame with historical yield data
        """
        # In a real app, this would fetch from a database
        # For now, generate some sample data
        years = list(range(2018, 2024))
        
        base_yields = {
            "Wheat": 3.2, "Rice": 4.0, "Maize": 5.5, "Soybean": 2.8, 
            "Potato": 14, "Tomato": 23, "Cotton": 1.3, "Sugarcane": 32,
            "Barley": 3.0, "Sorghum": 2.5
        }
        
        base = base_yields.get(crop_type, 4.0)
        
        # Generate some realistic trends with randomness
        yields = [
            base * random.uniform(0.85, 1.15) for _ in years
        ]
        
        return pd.DataFrame({
            'Year': years,
            'Yield (tons/acre)': yields
        })
    
    def check_model_status(self) -> bool:
        """Check if the prediction model is loaded and ready."""
        return self.model_loaded 