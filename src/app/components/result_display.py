import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, Any, List, Tuple, Optional


class ResultDisplay:
    """Component for displaying yield prediction results."""
    
    def __init__(self):
        """Initialize the ResultDisplay component."""
        # Set plot style
        sns.set_style("whitegrid")
        plt.rcParams.update({'font.size': 10})
    
    def display_results(self, 
                        predicted_yield: float, 
                        confidence: float, 
                        factor_importance: Dict[str, float],
                        input_data: Dict[str, Any],
                        historical_data: Optional[pd.DataFrame] = None):
        """
        Display the prediction results with visualizations.
        
        Args:
            predicted_yield: Predicted yield in tons/acre
            confidence: Confidence score (0-100)
            factor_importance: Dictionary of factor importance scores
            input_data: Dictionary of input parameters used for prediction
            historical_data: Optional historical yield data for comparison
        """
        self._display_main_results(predicted_yield, confidence, input_data)
        self._display_factor_importance(factor_importance)
        
        # Display historical comparison if data is provided
        if historical_data is not None:
            self._display_historical_comparison(predicted_yield, historical_data, input_data['crop_type'])
        
        # Display optimization suggestions
        self._display_optimization_suggestions(factor_importance, input_data)
    
    def _display_main_results(self, predicted_yield: float, confidence: float, input_data: Dict[str, Any]):
        """Display the main prediction results."""
        st.markdown("## 📊 Yield Prediction Results")
        
        # Create three columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Predicted Yield", 
                value=f"{predicted_yield:.2f} tons/acre", 
                delta=None
            )
        
        with col2:
            # Display confidence with color coding
            if confidence >= 80:
                confidence_color = "green"
            elif confidence >= 60:
                confidence_color = "orange"
            else:
                confidence_color = "red"
                
            st.markdown(
                f"""
                <div style="border-radius:10px; padding:10px; text-align:center; margin-bottom:10px">
                    <h4 style="margin:0; font-size:1rem;">Confidence</h4>
                    <p style="font-size:1.8rem; font-weight:bold; color:{confidence_color}; margin:0">
                        {confidence:.1f}%
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col3:
            st.write(f"**Crop Type:** {input_data['crop_type']}")
            st.write(f"**Season:** {input_data['season']}")
            
        # Display prediction info box
        st.info(
            f"""
            This prediction is based on the environmental conditions and farming practices you provided.
            With a confidence score of {confidence:.1f}%, the model predicts a yield of {predicted_yield:.2f} tons per acre
            for {input_data['crop_type']} under the specified conditions.
            """
        )
    
    def _display_factor_importance(self, factor_importance: Dict[str, float]):
        """Display factor importance chart."""
        st.markdown("### 🔍 Factor Importance")
        st.write("The chart below shows which factors had the biggest impact on the yield prediction:")
        
        # Convert factor importance to DataFrame for plotting
        factor_df = pd.DataFrame({
            'Factor': list(factor_importance.keys()),
            'Importance': list(factor_importance.values())
        })
        
        # Clean up factor names for display
        factor_df['Factor'] = factor_df['Factor'].apply(
            lambda x: x.replace('_', ' ').title()
        )
        
        # Sort by importance
        factor_df = factor_df.sort_values('Importance', ascending=False)
        
        # Create the horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.barh(factor_df['Factor'], factor_df['Importance'], color=sns.color_palette("viridis", len(factor_df)))
        
        # Add values at the end of each bar
        for i, bar in enumerate(bars):
            ax.text(
                bar.get_width() + 0.01, 
                bar.get_y() + bar.get_height()/2, 
                f'{factor_df["Importance"].iloc[i]:.2f}', 
                va='center'
            )
        
        # Set labels and title
        ax.set_xlabel('Importance Score')
        ax.set_title('Factors Affecting Yield Prediction')
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Display the chart
        st.pyplot(fig)
    
    def _display_historical_comparison(self, predicted_yield: float, historical_data: pd.DataFrame, crop_type: str):
        """Display comparison with historical yields."""
        st.markdown("### 📈 Historical Comparison")
        st.write(f"How the predicted yield compares to historical yields for {crop_type}:")
        
        # Create a copy of the historical data
        hist_data = historical_data.copy()
        
        # Add the predicted yield as a "Predicted" row
        current_year = max(hist_data['Year']) + 1
        predicted_row = pd.DataFrame({
            'Year': [current_year], 
            'Yield (tons/acre)': [predicted_yield],
            'Type': ['Predicted']
        })
        
        # Add 'Type' column to historical data
        hist_data['Type'] = 'Historical'
        
        # Combine datasets
        combined_data = pd.concat([hist_data, predicted_row], ignore_index=True)
        
        # Calculate average historical yield
        avg_yield = hist_data['Yield (tons/acre)'].mean()
        
        # Create the line chart
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot historical yield data
        sns.lineplot(
            x='Year', 
            y='Yield (tons/acre)', 
            data=hist_data,
            marker='o',
            color='blue',
            label='Historical Yield',
            ax=ax
        )
        
        # Add predicted yield point with different style
        ax.scatter(
            current_year, 
            predicted_yield, 
            color='green' if predicted_yield > avg_yield else 'red', 
            s=100, 
            label=f'Predicted ({current_year})'
        )
        
        # Add average line
        ax.axhline(
            y=avg_yield, 
            color='gray', 
            linestyle='--', 
            alpha=0.7,
            label=f'Historical Average ({avg_yield:.2f})'
        )
        
        # Set labels and title
        ax.set_xlabel('Year')
        ax.set_ylabel('Yield (tons/acre)')
        ax.set_title(f'Yield Comparison for {crop_type} Over Time')
        
        # Customize x-axis to show all years
        ax.set_xticks(combined_data['Year'].unique())
        
        # Add legend
        ax.legend()
        
        # Display the chart
        st.pyplot(fig)
        
        # Display comparison metrics
        percent_diff = ((predicted_yield - avg_yield) / avg_yield) * 100
        
        if percent_diff > 0:
            st.success(
                f"The predicted yield is {abs(percent_diff):.1f}% higher than the historical average."
            )
        elif percent_diff < 0:
            st.warning(
                f"The predicted yield is {abs(percent_diff):.1f}% lower than the historical average."
            )
        else:
            st.info(
                "The predicted yield is equal to the historical average."
            )
    
    def _display_optimization_suggestions(self, factor_importance: Dict[str, float], input_data: Dict[str, Any]):
        """Display suggestions for yield optimization."""
        st.markdown("### 🚜 Optimization Suggestions")
        
        # Get the top 3 factors affecting yield
        top_factors = list(factor_importance.keys())[:3]
        
        # Define suggestion templates for different factors
        suggestions = {
            "temperature": "Consider adjusting planting dates to better align with optimal temperature conditions.",
            "rainfall": "Implement proper irrigation scheduling based on crop water requirements.",
            "soil_ph": "Consider soil amendments to adjust pH to optimal levels for your crop.",
            "nitrogen_level": "Optimize nitrogen fertilization based on soil tests and crop requirements.",
            "phosphorus_level": "Consider adjusting phosphorus application based on soil test results.",
            "potassium_level": "Optimize potassium fertilization based on soil tests and crop needs.",
            "organic_matter": "Incorporate cover crops or apply organic amendments to improve soil organic matter.",
            "humidity": "In high humidity conditions, ensure proper spacing for air circulation. In low humidity, consider humidity management techniques.",
            "irrigation_method": "Consider upgrading to more efficient irrigation methods like drip irrigation.",
            "soil_type": "Select crop varieties that are well-suited to your soil type or consider soil amendments.",
            "sunlight": "Ensure proper plant spacing to maximize light interception."
        }
        
        # Display suggestions for top factors
        for i, factor in enumerate(top_factors):
            if factor in suggestions:
                st.markdown(f"**{i+1}. {factor.replace('_', ' ').title()}:** {suggestions[factor]}")
        
        # General suggestions
        st.markdown("---")
        st.markdown("**General recommendations:**")
        st.markdown("• Implement proper pest and disease management strategies")
        st.markdown("• Consider crop rotation to improve soil health and break pest cycles")
        st.markdown("• Regular soil testing is recommended to monitor nutrient levels")
        
        # Create expander for detailed recommendations
        with st.expander("View Detailed Recommendations"):
            # Create tabs for different categories
            tabs = st.tabs(["Soil Health", "Water Management", "Nutrient Management"])
            
            with tabs[0]:  # Soil Health
                st.markdown("### Soil Health Recommendations")
                st.markdown("• Implement minimum tillage practices to preserve soil structure")
                st.markdown("• Use cover crops during off-seasons to prevent erosion and add organic matter")
                st.markdown("• Consider soil amendments specific to your soil type")
                st.markdown("• Monitor soil pH regularly and adjust as needed")
            
            with tabs[1]:  # Water Management
                st.markdown("### Water Management Recommendations")
                st.markdown("• Implement water conservation practices")
                st.markdown("• Use soil moisture sensors to optimize irrigation timing")
                st.markdown("• Consider water-efficient irrigation methods")
                st.markdown("• Implement proper drainage in areas with excess water")
            
            with tabs[2]:  # Nutrient Management
                st.markdown("### Nutrient Management Recommendations")
                st.markdown("• Develop a balanced fertilization plan based on crop needs")
                st.markdown("• Consider split applications of nitrogen to reduce leaching")
                st.markdown("• Implement precision agriculture techniques for targeted nutrient application")
                st.markdown("• Use soil tests as the basis for fertilizer decisions")
    
    def display_error(self, error_message: str):
        """Display an error message."""
        st.error(f"Error: {error_message}")
        st.markdown("Please check your inputs and try again.") 