import streamlit as st
from typing import Dict, Any, Callable, Optional, List, Tuple


class YieldForm:
    """Component for collecting user input for yield prediction."""
    
    def __init__(self):
        """Initialize the YieldForm component with default values."""
        self.crop_types = [
            "Wheat", "Rice", "Maize", "Soybean", "Potato", 
            "Tomato", "Cotton", "Sugarcane", "Barley", "Sorghum"
        ]
        
        self.soil_types = [
            "Sandy", "Clay", "Loam", "Silt", "Sandy Loam", 
            "Clay Loam", "Silty Clay", "Sandy Clay", "Peaty"
        ]
        
        self.irrigation_methods = [
            "Drip", "Sprinkler", "Flood", "Furrow", "Rainfed", 
            "Center Pivot", "Micro-irrigation"
        ]
        
        self.fertilizer_types = [
            "Organic", "NPK", "Urea", "Ammonium Nitrate", 
            "Single Super Phosphate", "Potassium Sulfate", "None"
        ]
    
    def collect_input(self, on_submit: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
        """
        Display the yield prediction form and collect user input.
        
        Args:
            on_submit: Optional callback function to execute when form is submitted
            
        Returns:
            Dictionary containing all user inputs
        """
        with st.form("yield_prediction_form"):
            st.markdown("<h2 class='sub-header'>Yield Prediction Form</h2>", unsafe_allow_html=True)
            
            # Create form layout with columns
            col1, col2 = st.columns(2)
            
            # Basic crop information (left column)
            with col1:
                self._display_section_header("Crop Information")
                
                crop_type = st.selectbox(
                    "Crop Type", 
                    self.crop_types, 
                    index=0,
                    help="Select the type of crop you are growing"
                )
                
                variety = st.text_input(
                    "Crop Variety/Cultivar", 
                    value="",
                    help="Enter the specific variety or cultivar of your crop"
                )
                
                field_area = st.number_input(
                    "Field Area (acres)", 
                    min_value=0.1, 
                    max_value=10000.0, 
                    value=5.0, 
                    step=0.5,
                    help="Enter the total area of your field in acres"
                )
                
                planting_date = st.date_input(
                    "Planting Date",
                    help="Select the date when the crop was planted"
                )
                
                # Soil parameters
                self._display_section_header("Soil Parameters")
                
                soil_type = st.selectbox(
                    "Soil Type", 
                    self.soil_types, 
                    index=2,
                    help="Select the predominant soil type in your field"
                )
                
                soil_ph = st.slider(
                    "Soil pH", 
                    min_value=4.0, 
                    max_value=9.0, 
                    value=6.5, 
                    step=0.1,
                    help="Enter the pH level of your soil"
                )
                
                organic_matter = st.slider(
                    "Organic Matter (%)", 
                    min_value=0.0, 
                    max_value=10.0, 
                    value=2.5, 
                    step=0.1,
                    help="Enter the percentage of organic matter in your soil"
                )
            
            # Environmental factors (right column)
            with col2:
                self._display_section_header("Environmental Factors")
                
                temperature = st.slider(
                    "Average Temperature (°C)", 
                    min_value=-5.0, 
                    max_value=45.0, 
                    value=25.0, 
                    step=0.5,
                    help="Enter the average temperature during the growing season"
                )
                
                rainfall = st.slider(
                    "Annual Rainfall (mm)", 
                    min_value=0, 
                    max_value=3000, 
                    value=750, 
                    step=50,
                    help="Enter the average annual rainfall in your area"
                )
                
                humidity = st.slider(
                    "Average Humidity (%)", 
                    min_value=0, 
                    max_value=100, 
                    value=65, 
                    step=5,
                    help="Enter the average humidity during the growing season"
                )
                
                sunlight = st.slider(
                    "Daily Sunlight (hours)", 
                    min_value=0, 
                    max_value=16, 
                    value=8, 
                    step=1,
                    help="Enter the average daily sunlight hours"
                )
                
                # Farming practices
                self._display_section_header("Farming Practices")
                
                irrigation_method = st.selectbox(
                    "Irrigation Method", 
                    self.irrigation_methods, 
                    index=0,
                    help="Select the irrigation method used in your field"
                )
                
                fertilizer_type = st.multiselect(
                    "Fertilizer Types", 
                    self.fertilizer_types, 
                    default=["NPK"],
                    help="Select the types of fertilizers you use"
                )
                
                # Optional: Get nutrient levels if the user has them
                with st.expander("Nutrient Levels (Optional)"):
                    nitrogen_level = st.slider(
                        "Nitrogen (N) Level (ppm)", 
                        min_value=0, 
                        max_value=200, 
                        value=50, 
                        step=5,
                        help="Enter the nitrogen level in your soil in parts per million"
                    )
                    
                    phosphorus_level = st.slider(
                        "Phosphorus (P) Level (ppm)", 
                        min_value=0, 
                        max_value=200, 
                        value=30, 
                        step=5,
                        help="Enter the phosphorus level in your soil in parts per million"
                    )
                    
                    potassium_level = st.slider(
                        "Potassium (K) Level (ppm)", 
                        min_value=0, 
                        max_value=200, 
                        value=40, 
                        step=5,
                        help="Enter the potassium level in your soil in parts per million"
                    )
            
            # Show previous yields if available (optional)
            with st.expander("Previous Yields (Optional)"):
                previous_yields = []
                for i in range(3):
                    col_year, col_yield = st.columns(2)
                    with col_year:
                        year = st.number_input(
                            f"Year {i+1}", 
                            min_value=2010, 
                            max_value=2023, 
                            value=2023-i, 
                            step=1,
                            key=f"year_{i}"
                        )
                    with col_yield:
                        yield_value = st.number_input(
                            f"Yield {i+1} (tons/acre)", 
                            min_value=0.0, 
                            max_value=100.0, 
                            value=0.0, 
                            step=0.1,
                            key=f"yield_{i}"
                        )
                    
                    if yield_value > 0:
                        previous_yields.append((year, yield_value))
            
            # Submit button
            submit_button = st.form_submit_button(
                "Predict Yield", 
                use_container_width=True,
                type="primary"
            )
            
            # Collect all form values
            form_data = {
                # Crop information
                "crop_type": crop_type,
                "variety": variety,
                "field_area": field_area,
                "planting_date": planting_date,
                
                # Soil parameters
                "soil_type": soil_type,
                "soil_ph": soil_ph,
                "organic_matter": organic_matter,
                
                # Environmental factors
                "temperature": temperature,
                "rainfall": rainfall,
                "humidity": humidity,
                "sunlight": sunlight,
                
                # Farming practices
                "irrigation_method": irrigation_method,
                "fertilizer_type": fertilizer_type,
                
                # Nutrient levels
                "nitrogen_level": nitrogen_level,
                "phosphorus_level": phosphorus_level,
                "potassium_level": potassium_level,
                
                # Previous yields
                "previous_yields": previous_yields
            }
            
            # Call submit callback if form is submitted
            if submit_button and on_submit:
                on_submit(form_data)
        
        return form_data
    
    def _display_section_header(self, title: str):
        """Display a formatted section header in the form."""
        st.markdown(
            f"""
            <div style="margin-top: 15px; margin-bottom: 5px;">
                <p style="font-weight: bold; color: #2E7D32; border-bottom: 1px solid #E0E0E0; 
                padding-bottom: 5px;">{title}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )


class YieldPredictionForm(YieldForm):
    """Form specifically tailored for the main application interface."""
    
    def show_form(self) -> Tuple[Dict[str, Any], bool]:
        """
        Display the yield prediction form and return the input data and submission status.
        
        Returns:
            Tuple containing:
                - Dictionary with form input data
                - Boolean indicating if the form was submitted
        """
        with st.form("yield_prediction_form"):
            st.markdown("<h2 class='sub-header'>Enter Your Field Parameters</h2>", unsafe_allow_html=True)
            
            # Create form layout with columns
            col1, col2 = st.columns(2)
            
            # Crop and field information (left column)
            with col1:
                crop_type = st.selectbox(
                    "Crop Type", 
                    self.crop_types, 
                    help="Select the type of crop you are growing"
                )
                
                field_area = st.number_input(
                    "Field Area (acres)", 
                    min_value=0.1, 
                    max_value=10000.0, 
                    value=5.0, 
                    step=0.5
                )
                
                soil_type = st.selectbox(
                    "Soil Type", 
                    self.soil_types
                )
                
                soil_ph = st.slider(
                    "Soil pH", 
                    min_value=4.0, 
                    max_value=9.0, 
                    value=6.5, 
                    step=0.1
                )
                
                irrigation_method = st.selectbox(
                    "Irrigation Method", 
                    self.irrigation_methods
                )
            
            # Environmental and nutrient factors (right column)
            with col2:
                temperature = st.slider(
                    "Average Temperature (°C)", 
                    min_value=-5.0, 
                    max_value=45.0, 
                    value=25.0, 
                    step=0.5
                )
                
                rainfall = st.slider(
                    "Annual Rainfall (mm)", 
                    min_value=0, 
                    max_value=3000, 
                    value=750, 
                    step=50
                )
                
                humidity = st.slider(
                    "Average Humidity (%)", 
                    min_value=0, 
                    max_value=100, 
                    value=65, 
                    step=5
                )
                
                # Nutrient levels
                nitrogen = st.slider(
                    "Nitrogen (N) Level (kg/ha)", 
                    min_value=0, 
                    max_value=200, 
                    value=50
                )
                
                phosphorus = st.slider(
                    "Phosphorus (P) Level (kg/ha)", 
                    min_value=0, 
                    max_value=200, 
                    value=30
                )
                
                potassium = st.slider(
                    "Potassium (K) Level (kg/ha)", 
                    min_value=0, 
                    max_value=200, 
                    value=40
                )
            
            # Submit button
            submitted = st.form_submit_button(
                "Predict Yield", 
                use_container_width=True,
                type="primary"
            )
            
            # Prepare input data
            input_data = {
                "crop_type": crop_type,
                "field_area": field_area,
                "soil_type": soil_type,
                "soil_ph": soil_ph,
                "irrigation_method": irrigation_method,
                "temperature": temperature,
                "rainfall": rainfall,
                "humidity": humidity,
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium
            }
            
        return input_data, submitted 