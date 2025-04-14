import os
import json
import csv
import datetime
import numpy as np
from typing import Dict, Any, List, Optional, Union
import shutil


class DataService:
    """Service class for handling data operations for predictions."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the DataService with data directory path.
        
        Args:
            data_dir: Directory path where data files are stored
        """
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_prediction(self, input_data: Dict[str, Any], prediction_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save input data and prediction result to a JSON file.
        
        Args:
            input_data: Dictionary containing input parameters used for prediction
            prediction_result: Dictionary containing prediction results
            
        Returns:
            Dictionary containing status and filename of saved prediction
        """
        try:
            # Extract crop type from input data
            crop_type = input_data.get("crop_type", "unknown").lower()
            
            # Create timestamp for filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create filename based on crop type and timestamp
            filename = f"{crop_type}_prediction_{timestamp}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            # Combine input data and prediction result
            prediction_data = {
                "input_data": input_data,
                "prediction_result": prediction_result,
                "timestamp": timestamp
            }
            
            # Save to JSON file
            with open(filepath, 'w') as f:
                json.dump(prediction_data, f, indent=4)
            
            return {
                "status": "success",
                "filename": filename
            }
            
        except Exception as e:
            print(f"Error saving prediction: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to save prediction: {str(e)}"
            }
    
    def load_saved_predictions(self, crop_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Load saved predictions from JSON files.
        
        Args:
            crop_type: Optional filter for crop type
            limit: Maximum number of predictions to load
            
        Returns:
            List of dictionaries containing saved predictions
        """
        predictions = []
        
        try:
            # List all JSON files in data directory
            all_files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
            
            # Sort files by timestamp (descending, most recent first)
            all_files.sort(reverse=True)
            
            # Filter by crop type if specified
            if crop_type:
                crop_type = crop_type.lower()
                filtered_files = [f for f in all_files if f.startswith(f"{crop_type}_prediction_")]
            else:
                filtered_files = all_files
            
            # Load files up to the limit
            count = 0
            for filename in filtered_files:
                if count >= limit:
                    break
                
                filepath = os.path.join(self.data_dir, filename)
                
                try:
                    with open(filepath, 'r') as f:
                        prediction_data = json.load(f)
                        
                    # Add filename to the prediction data
                    prediction_data["filename"] = filename
                    
                    predictions.append(prediction_data)
                    count += 1
                    
                except Exception as e:
                    print(f"Error loading prediction file {filename}: {str(e)}")
                    continue
            
            return predictions
            
        except Exception as e:
            print(f"Error loading saved predictions: {str(e)}")
            return []
    
    def generate_summary_stats(self, crop_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate summary statistics from saved predictions.
        
        Args:
            crop_type: Optional filter for crop type
            
        Returns:
            Dictionary containing summary statistics
        """
        try:
            # Load all relevant predictions
            predictions = self.load_saved_predictions(crop_type=crop_type, limit=100)
            
            if not predictions:
                return {
                    "status": "error",
                    "message": f"No predictions found for analysis" if not crop_type else f"No predictions found for crop type: {crop_type}"
                }
            
            # Extract predicted yield values
            yields = []
            for prediction in predictions:
                try:
                    yield_value = prediction.get("prediction_result", {}).get("predicted_yield")
                    if yield_value is not None:
                        yields.append(float(yield_value))
                except (TypeError, ValueError) as e:
                    print(f"Error extracting yield from prediction: {str(e)}")
                    continue
            
            if not yields:
                return {
                    "status": "error",
                    "message": "No valid yield values found in predictions"
                }
            
            # Calculate statistics
            yields_array = np.array(yields)
            stats = {
                "count": len(yields),
                "average": float(np.mean(yields_array)),
                "median": float(np.median(yields_array)),
                "min": float(np.min(yields_array)),
                "max": float(np.max(yields_array)),
                "std_dev": float(np.std(yields_array))
            }
            
            return {
                "status": "success",
                "crop_type": crop_type,
                "statistics": stats
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating summary statistics: {str(e)}"
            }
    
    def export_predictions_to_csv(self, filepath: str, crop_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Export saved predictions to a CSV file.
        
        Args:
            filepath: Path for the output CSV file
            crop_type: Optional filter for crop type
            
        Returns:
            Dictionary containing status and path of exported file
        """
        try:
            # Ensure filename has .csv extension
            if not filepath.lower().endswith('.csv'):
                filepath += '.csv'
            
            # Load predictions
            predictions = self.load_saved_predictions(crop_type=crop_type, limit=100)
            
            if not predictions:
                return {
                    "status": "error",
                    "message": f"No predictions found to export" if not crop_type else f"No predictions found for crop type: {crop_type}"
                }
            
            # Prepare CSV data
            # We'll flatten the nested structure for easier CSV access
            csv_data = []
            
            for prediction in predictions:
                try:
                    # Extract data
                    input_data = prediction.get("input_data", {})
                    prediction_result = prediction.get("prediction_result", {})
                    timestamp = prediction.get("timestamp", "")
                    
                    # Create flattened row
                    row = {
                        "timestamp": timestamp,
                        "crop_type": input_data.get("crop_type", ""),
                        "soil_type": input_data.get("soil_type", ""),
                        "temperature": input_data.get("temperature", ""),
                        "rainfall": input_data.get("rainfall", ""),
                        "humidity": input_data.get("humidity", ""),
                        "nitrogen": input_data.get("nitrogen", ""),
                        "phosphorus": input_data.get("phosphorus", ""),
                        "potassium": input_data.get("potassium", ""),
                        "area": input_data.get("area", ""),
                        "predicted_yield": prediction_result.get("predicted_yield", ""),
                        "confidence": prediction_result.get("confidence", "")
                    }
                    
                    csv_data.append(row)
                    
                except Exception as e:
                    print(f"Error processing prediction for CSV: {str(e)}")
                    continue
            
            if not csv_data:
                return {
                    "status": "error",
                    "message": "No valid data found to export"
                }
            
            # Write to CSV file
            with open(filepath, 'w', newline='') as csvfile:
                # Get all unique field names from all rows
                fieldnames = set()
                for row in csv_data:
                    fieldnames.update(row.keys())
                
                fieldnames = sorted(list(fieldnames))
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            
            return {
                "status": "success",
                "filepath": filepath,
                "rows_exported": len(csv_data)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error exporting predictions to CSV: {str(e)}"
            }
    
    def clear_saved_predictions(self, crop_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete saved prediction files.
        
        Args:
            crop_type: Optional filter for crop type
            
        Returns:
            Dictionary containing status and count of deleted files
        """
        try:
            # List all JSON files in data directory
            all_files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
            
            # Filter by crop type if specified
            if crop_type:
                crop_type = crop_type.lower()
                files_to_delete = [f for f in all_files if f.startswith(f"{crop_type}_prediction_")]
            else:
                files_to_delete = all_files
            
            # Delete files
            deleted_count = 0
            for filename in files_to_delete:
                try:
                    filepath = os.path.join(self.data_dir, filename)
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting file {filename}: {str(e)}")
                    continue
            
            return {
                "status": "success",
                "deleted_count": deleted_count,
                "message": f"Deleted {deleted_count} prediction files"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error clearing saved predictions: {str(e)}"
            } 