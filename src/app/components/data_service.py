import pandas as pd
import numpy as np
import json
import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class DataService:
    """Service for handling data operations for yield prediction."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the DataService with data directory path.
        
        Args:
            data_dir: Directory path where data files are stored
        """
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_prediction(self, 
                       input_data: Dict[str, Any], 
                       prediction_results: Dict[str, Any]) -> bool:
        """
        Save prediction inputs and results to a file.
        
        Args:
            input_data: Dictionary containing input parameters for prediction
            prediction_results: Dictionary containing prediction results
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            # Create a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Combine input and results data
            save_data = {
                "timestamp": timestamp,
                "inputs": input_data,
                "results": prediction_results
            }
            
            # Define the filename based on crop type and timestamp
            crop_type = input_data.get("crop_type", "unknown")
            filename = f"{crop_type.lower().replace(' ', '_')}_{timestamp}.json"
            
            # Full path to save file
            file_path = os.path.join(self.data_dir, filename)
            
            # Save to JSON file
            with open(file_path, 'w') as f:
                json.dump(save_data, f, indent=4)
            
            return True
        
        except Exception as e:
            print(f"Error saving prediction data: {e}")
            return False
    
    def load_saved_predictions(self, 
                              crop_type: Optional[str] = None, 
                              limit: int = 10) -> List[Dict[str, Any]]:
        """
        Load saved predictions from files.
        
        Args:
            crop_type: Optional filter by crop type
            limit: Maximum number of predictions to load
            
        Returns:
            List of dictionaries containing prediction data
        """
        predictions = []
        
        try:
            # List all JSON files in the data directory
            files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
            
            # Sort files by modification time (newest first)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.data_dir, x)), reverse=True)
            
            # Filter files by crop type if specified
            if crop_type:
                crop_str = crop_type.lower().replace(' ', '_')
                files = [f for f in files if f.startswith(crop_str)]
            
            # Load data from files (up to the limit)
            for file in files[:limit]:
                with open(os.path.join(self.data_dir, file), 'r') as f:
                    prediction_data = json.load(f)
                    predictions.append(prediction_data)
            
            return predictions
            
        except Exception as e:
            print(f"Error loading prediction data: {e}")
            return []
    
    def generate_summary_stats(self, crop_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate summary statistics from saved predictions.
        
        Args:
            crop_type: Optional filter by crop type
            
        Returns:
            Dictionary containing summary statistics
        """
        # Load saved predictions
        predictions = self.load_saved_predictions(crop_type=crop_type, limit=100)
        
        if not predictions:
            return {"error": "No prediction data available for analysis"}
        
        try:
            # Extract yield predictions
            yields = [p["results"]["predicted_yield"] for p in predictions if "results" in p and "predicted_yield" in p["results"]]
            
            # Calculate statistics
            stats = {
                "count": len(yields),
                "average_yield": np.mean(yields) if yields else 0,
                "median_yield": np.median(yields) if yields else 0,
                "min_yield": min(yields) if yields else 0,
                "max_yield": max(yields) if yields else 0,
                "std_dev": np.std(yields) if yields else 0
            }
            
            # Add crop type information
            if crop_type:
                stats["crop_type"] = crop_type
            else:
                # Count predictions by crop type
                crop_counts = {}
                for p in predictions:
                    if "inputs" in p and "crop_type" in p["inputs"]:
                        crop = p["inputs"]["crop_type"]
                        crop_counts[crop] = crop_counts.get(crop, 0) + 1
                stats["crop_type_distribution"] = crop_counts
            
            return stats
            
        except Exception as e:
            print(f"Error generating summary statistics: {e}")
            return {"error": f"Failed to generate statistics: {str(e)}"}
    
    def export_predictions_to_csv(self, filename: str, crop_type: Optional[str] = None) -> Tuple[bool, str]:
        """
        Export saved predictions to a CSV file.
        
        Args:
            filename: Name of CSV file to create
            crop_type: Optional filter by crop type
            
        Returns:
            Tuple containing success status and message
        """
        # Load saved predictions
        predictions = self.load_saved_predictions(crop_type=crop_type, limit=1000)
        
        if not predictions:
            return False, "No prediction data available to export"
        
        try:
            # Create a list to hold flattened data
            flattened_data = []
            
            # Process each prediction
            for p in predictions:
                if "inputs" in p and "results" in p:
                    # Combine inputs and results, flattening the structure
                    record = {"timestamp": p.get("timestamp", "")}
                    
                    # Add input fields
                    for key, value in p["inputs"].items():
                        record[f"input_{key}"] = value
                    
                    # Add result fields
                    for key, value in p["results"].items():
                        # Skip factor_importance as it's a nested structure
                        if key != "factor_importance":
                            record[f"result_{key}"] = value
                    
                    flattened_data.append(record)
            
            # Convert to DataFrame
            df = pd.DataFrame(flattened_data)
            
            # Ensure the file has a .csv extension
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            # Create full path
            file_path = os.path.join(self.data_dir, filename)
            
            # Save to CSV
            df.to_csv(file_path, index=False)
            
            return True, f"Successfully exported {len(flattened_data)} predictions to {filename}"
            
        except Exception as e:
            return False, f"Error exporting prediction data: {str(e)}"
    
    def clear_saved_predictions(self, crop_type: Optional[str] = None) -> Tuple[bool, str]:
        """
        Delete saved prediction files.
        
        Args:
            crop_type: Optional filter to delete only specific crop type predictions
            
        Returns:
            Tuple containing success status and message
        """
        try:
            # List all JSON files in the data directory
            files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
            
            # Filter files by crop type if specified
            if crop_type:
                crop_str = crop_type.lower().replace(' ', '_')
                files = [f for f in files if f.startswith(crop_str)]
            
            # Delete the files
            deleted_count = 0
            for file in files:
                os.remove(os.path.join(self.data_dir, file))
                deleted_count += 1
            
            if crop_type:
                return True, f"Successfully deleted {deleted_count} predictions for {crop_type}"
            else:
                return True, f"Successfully deleted {deleted_count} predictions"
            
        except Exception as e:
            return False, f"Error deleting prediction data: {str(e)}" 