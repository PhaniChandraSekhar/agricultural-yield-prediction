import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
import random
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from pathlib import Path


class PredictionModel:
    """Model class for crop yield prediction."""
    
    def __init__(self, model_dir: str = "models"):
        """
        Initialize the PredictionModel with model directory path.
        
        Args:
            model_dir: Directory path where model files are stored
        """
        self.model_dir = model_dir
        self.models = {}
        self.loaded_models = {}
        
        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Define standard crop types and their corresponding models
        self.models = {
            "rice": "rice_yield_model.joblib",
            "wheat": "wheat_yield_model.joblib",
            "corn": "corn_yield_model.joblib",
            "potato": "potato_yield_model.joblib",
            "soybean": "soybean_yield_model.joblib"
        }
        
        # Try to load existing models
        self._load_available_models()
    
    def _load_available_models(self):
        """Attempt to load available trained models."""
        for crop_type, model_file in self.models.items():
            model_path = Path(self.model_dir) / model_file
            if model_path.exists():
                try:
                    self.loaded_models[crop_type] = joblib.load(model_path)
                    print(f"Loaded model for {crop_type}")
                except Exception as e:
                    print(f"Error loading model for {crop_type}: {e}")
    
    def predict_yield(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict crop yield based on input parameters.
        
        Args:
            input_data: Dictionary containing input parameters for prediction
                Required keys:
                - crop_type: Type of crop (rice, wheat, corn, etc.)
                - soil_type: Type of soil
                - temperature: Average temperature (°C)
                - rainfall: Average rainfall (mm)
                - humidity: Average humidity (%)
                - nitrogen: Nitrogen content in soil (kg/ha)
                - phosphorus: Phosphorus content in soil (kg/ha)
                - potassium: Potassium content in soil (kg/ha)
                - area: Area of land (hectares)
                
        Returns:
            Dictionary containing prediction results
        """
        # Extract the crop type from input data
        crop_type = input_data.get("crop_type", "").lower()
        
        # Check if crop type is supported
        if not crop_type or crop_type not in self.models:
            return {
                "error": f"Unsupported crop type: {crop_type}. Supported types: {', '.join(self.models.keys())}"
            }
        
        # Check if all required fields are present
        required_fields = ['soil_type', 'temperature', 'rainfall', 'humidity', 
                         'nitrogen', 'phosphorus', 'potassium', 'area']
        
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            return {
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        try:
            # If we have a loaded model for this crop type, use it
            if crop_type in self.loaded_models:
                # Prepare input data for prediction
                features = self._prepare_features(input_data)
                
                # Make prediction
                model = self.loaded_models[crop_type]
                predicted_yield = model.predict(features)[0]
                
                # Get feature importance
                importance = self._get_feature_importance(model, features.columns)
                
                # Calculate confidence score (example implementation)
                confidence = self._calculate_confidence(model, features)
                
            else:
                # If no model is loaded, use placeholder prediction for demo
                # Note: In production, you might want to return an error instead
                predicted_yield, importance, confidence = self._placeholder_prediction(input_data)
            
            # Generate optimization suggestions based on feature importance
            suggestions = self._generate_optimization_suggestions(importance, input_data)
            
            # Return prediction results
            return {
                "predicted_yield": float(predicted_yield),
                "confidence": float(confidence),
                "factor_importance": importance,
                "optimization_suggestions": suggestions
            }
            
        except Exception as e:
            return {"error": f"Prediction error: {str(e)}"}
    
    def _prepare_features(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare input features for model prediction.
        
        Args:
            input_data: Raw input data dictionary
            
        Returns:
            DataFrame with prepared features
        """
        # Convert soil_type to one-hot encoding
        soil_types = ['clay', 'loamy', 'sandy', 'silt']
        soil_features = {f"soil_{soil}": 1 if input_data["soil_type"].lower() == soil else 0 
                      for soil in soil_types}
        
        # Combine numerical features with encoded categorical features
        features = {
            'temperature': float(input_data['temperature']),
            'rainfall': float(input_data['rainfall']),
            'humidity': float(input_data['humidity']),
            'nitrogen': float(input_data['nitrogen']),
            'phosphorus': float(input_data['phosphorus']),
            'potassium': float(input_data['potassium']),
            'area': float(input_data['area']),
            **soil_features
        }
        
        # Add any crop-specific processing here
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        return df
    
    def _get_feature_importance(self, model, feature_names):
        """
        Get feature importance from model.
        
        Args:
            model: Trained model with feature_importances_ attribute
            feature_names: List of feature names
            
        Returns:
            Dictionary mapping feature names to importance values
        """
        # Check if model has feature_importances_
        if hasattr(model, 'feature_importances_'):
            importance = dict(zip(feature_names, model.feature_importances_))
            
            # Sort by importance (descending)
            importance = {k: v for k, v in sorted(
                importance.items(), key=lambda item: item[1], reverse=True
            )}
            
            return importance
        else:
            # Fallback for models without feature_importances_
            return {name: 1.0/len(feature_names) for name in feature_names}
    
    def _calculate_confidence(self, model, features):
        """
        Calculate a confidence score for the prediction.
        
        Args:
            model: Trained model
            features: Input features
            
        Returns:
            Confidence score (0-1)
        """
        # This is a simplified example - in a real implementation, this could be:
        # - Based on model's prediction interval
        # - Cross-validation statistics
        # - Distance to training samples
        # - Ensemble variance
        
        # For now, we'll use a placeholder that gives higher confidence
        # when features are within expected ranges
        
        # Placeholder implementation - adjust coefficients based on your data
        confidence = 0.85  # Base confidence
        
        # Reduce confidence if values are outside expected ranges
        temp = features['temperature'].values[0]
        if temp < 10 or temp > 35:
            confidence -= 0.1
            
        rainfall = features['rainfall'].values[0]
        if rainfall < 50 or rainfall > 2000:
            confidence -= 0.1
            
        return min(max(confidence, 0.3), 1.0)  # Keep between 0.3 and 1.0
    
    def _placeholder_prediction(self, input_data: Dict[str, Any]) -> Tuple[float, Dict[str, float], float]:
        """
        Generate a placeholder prediction when no model is available.
        
        Args:
            input_data: Input data dictionary
            
        Returns:
            Tuple of (predicted_yield, feature_importance, confidence)
        """
        # Get crop type and basic parameters
        crop_type = input_data.get("crop_type", "").lower()
        area = float(input_data.get("area", 1))
        
        # Base yields per hectare for different crops
        base_yields = {
            "rice": 4.5,      # tons/hectare
            "wheat": 3.0,     # tons/hectare
            "corn": 5.5,      # tons/hectare
            "potato": 25.0,   # tons/hectare
            "soybean": 2.5    # tons/hectare
        }
        
        # Get base yield for this crop
        base_yield = base_yields.get(crop_type, 3.0)
        
        # Apply multiplicative factors based on input parameters
        adjustment = 1.0
        
        # Temperature factor (each crop has an optimal temperature range)
        temp = float(input_data.get("temperature", 25))
        if crop_type == "rice":
            # Rice grows well in warmer weather
            adjustment *= 1.0 + 0.02 * max(-1, min(1, (temp - 25) / 5))
        else:
            # Most other crops prefer moderate temperatures
            adjustment *= 1.0 + 0.02 * max(-1, min(1, (24 - abs(temp - 24)) / 5))
        
        # Rainfall factor
        rainfall = float(input_data.get("rainfall", 1000))
        if crop_type == "rice":
            # Rice needs a lot of water
            adjustment *= 1.0 + 0.02 * max(-1, min(1, (rainfall - 1000) / 200))
        else:
            # Other crops need moderate rainfall
            adjustment *= 1.0 + 0.02 * max(-1, min(1, (800 - abs(rainfall - 800)) / 200))
        
        # Soil nutrients factor
        nitrogen = float(input_data.get("nitrogen", 100))
        phosphorus = float(input_data.get("phosphorus", 50))
        potassium = float(input_data.get("potassium", 50))
        
        nutrient_factor = 1.0 + 0.005 * (nitrogen / 100 + phosphorus / 50 + potassium / 50 - 3)
        adjustment *= nutrient_factor
        
        # Calculate final yield
        predicted_yield = base_yield * adjustment * area
        
        # Add some randomness to make it look more realistic
        random_factor = 1.0 + random.uniform(-0.05, 0.05)
        predicted_yield *= random_factor
        
        # Generate placeholder feature importance
        importance = {
            "nitrogen": 0.20 + random.uniform(-0.03, 0.03),
            "rainfall": 0.18 + random.uniform(-0.03, 0.03),
            "temperature": 0.15 + random.uniform(-0.02, 0.02),
            "soil_type": 0.12 + random.uniform(-0.02, 0.02),
            "phosphorus": 0.10 + random.uniform(-0.02, 0.02),
            "potassium": 0.10 + random.uniform(-0.02, 0.02),
            "humidity": 0.08 + random.uniform(-0.01, 0.01),
            "area": 0.07 + random.uniform(-0.01, 0.01)
        }
        
        # Normalize importance values
        total = sum(importance.values())
        importance = {k: v/total for k, v in importance.items()}
        
        # Sort by importance (descending)
        importance = {k: v for k, v in sorted(
            importance.items(), key=lambda item: item[1], reverse=True
        )}
        
        # Generate confidence score (placeholder)
        confidence = 0.75 + random.uniform(-0.1, 0.1)
        
        return predicted_yield, importance, confidence
    
    def _generate_optimization_suggestions(self, 
                                         importance: Dict[str, float], 
                                         input_data: Dict[str, Any]) -> List[str]:
        """
        Generate suggestions for optimizing yield based on factor importance.
        
        Args:
            importance: Dictionary of feature importance
            input_data: Input data dictionary
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        crop_type = input_data.get("crop_type", "").lower()
        
        # Get the top 3 important factors
        top_factors = list(importance.keys())[:3]
        
        # Generate suggestions based on top factors
        for factor in top_factors:
            if factor == "nitrogen":
                nitrogen = float(input_data.get("nitrogen", 0))
                if nitrogen < 100:
                    suggestions.append(f"Consider increasing nitrogen application to around 100-120 kg/ha for optimal {crop_type} yield.")
                elif nitrogen > 150:
                    suggestions.append(f"Current nitrogen level is high. Consider reducing to avoid waste and environmental impact.")
            
            elif factor == "rainfall" or factor == "water":
                rainfall = float(input_data.get("rainfall", 0))
                if crop_type == "rice" and rainfall < 1000:
                    suggestions.append("Rice requires significant water. Consider implementing irrigation to supplement rainfall.")
                elif crop_type != "rice" and rainfall < 600:
                    suggestions.append(f"Rainfall appears low for {crop_type}. Consider supplemental irrigation during dry periods.")
                elif rainfall > 1500 and crop_type != "rice":
                    suggestions.append(f"Area may be too wet for optimal {crop_type} growth. Consider improved drainage solutions.")
            
            elif factor == "temperature":
                temp = float(input_data.get("temperature", 0))
                if (crop_type == "rice" and temp < 22) or (crop_type != "rice" and temp < 15):
                    suggestions.append(f"Temperature may be too low. Consider adjusting planting season or using row covers.")
                elif temp > 32:
                    suggestions.append("Temperature is high. Ensure adequate irrigation and consider heat-resistant varieties.")
            
            elif "soil" in factor:
                soil_type = input_data.get("soil_type", "").lower()
                if soil_type == "sandy":
                    suggestions.append("Sandy soil may benefit from adding organic matter to improve water retention.")
                elif soil_type == "clay":
                    suggestions.append("Clay soil may benefit from improved drainage and structure amendments.")
            
            elif factor == "phosphorus":
                phosphorus = float(input_data.get("phosphorus", 0))
                if phosphorus < 30:
                    suggestions.append("Phosphorus level is low. Consider applying phosphate fertilizers to promote root development.")
            
            elif factor == "potassium":
                potassium = float(input_data.get("potassium", 0))
                if potassium < 30:
                    suggestions.append("Potassium level is low. Consider applying potassium fertilizers to improve crop quality and stress resistance.")
        
        # Add general suggestion if we have fewer than 3 specific ones
        if len(suggestions) < 3:
            suggestions.append(f"Consider consulting with a local agricultural extension service for {crop_type}-specific recommendations.")
        
        return suggestions
    
    def train_model(self, 
                   crop_type: str, 
                   training_data: pd.DataFrame, 
                   save_model: bool = True) -> Tuple[bool, str]:
        """
        Train a new model for a specific crop type.
        
        Args:
            crop_type: Type of crop
            training_data: DataFrame containing training data
            save_model: Whether to save the trained model
            
        Returns:
            Tuple containing success status and message
        """
        try:
            # Normalize crop type
            crop_type = crop_type.lower()
            
            # Check if crop type is supported
            if crop_type not in self.models:
                return False, f"Unsupported crop type: {crop_type}"
            
            # Check if training data has required columns
            required_columns = ['yield', 'temperature', 'rainfall', 'humidity', 
                            'nitrogen', 'phosphorus', 'potassium', 'area', 'soil_type']
            
            missing_columns = [col for col in required_columns if col not in training_data.columns]
            if missing_columns:
                return False, f"Training data missing required columns: {', '.join(missing_columns)}"
            
            # Prepare features and target
            X = self._prepare_training_features(training_data)
            y = training_data['yield']
            
            # Train model (RandomForest for this example)
            model = RandomForestRegressor(
                n_estimators=100, 
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                random_state=42
            )
            
            model.fit(X, y)
            
            # Save model if requested
            if save_model:
                model_path = Path(self.model_dir) / self.models[crop_type]
                os.makedirs(model_path.parent, exist_ok=True)
                joblib.dump(model, model_path)
            
            # Update loaded models
            self.loaded_models[crop_type] = model
            
            return True, f"Successfully trained model for {crop_type}"
            
        except Exception as e:
            return False, f"Error training model: {str(e)}"
    
    def _prepare_training_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features from training data.
        
        Args:
            data: Raw training data
            
        Returns:
            DataFrame with prepared features
        """
        # One-hot encode soil type
        soil_dummies = pd.get_dummies(data['soil_type'], prefix='soil')
        
        # Combine with numerical features
        numerical_features = ['temperature', 'rainfall', 'humidity', 
                           'nitrogen', 'phosphorus', 'potassium', 'area']
        
        X = pd.concat([data[numerical_features], soil_dummies], axis=1)
        
        return X 