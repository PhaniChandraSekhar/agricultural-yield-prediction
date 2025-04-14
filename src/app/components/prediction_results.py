import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List

class PredictionResults:
    """Component for displaying yield prediction results and recommendations."""
    
    def show_results(self, predicted_yield: float, confidence: float, 
                     factor_importance: Dict[str, float], input_data: Dict[str, Any]):
        """
        Display the yield prediction results with visualizations.
        
        Args:
            predicted_yield: The predicted crop yield in tons/acre
            confidence: Confidence level of the prediction (0-100)
            factor_importance: Dictionary mapping factors to their importance
            input_data: Dictionary containing the input form data
        """
        # Display the prediction in a card
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f'<h2 class="sub-header">Prediction Results</h2>', unsafe_allow_html=True)
            
            # Create a colored box for the prediction
            predicted_yield_rounded = round(predicted_yield, 2)
            area = input_data.get("field_area", 1)
            total_yield = round(predicted_yield * area, 2)
            
            # Determine yield quality level based on confidence
            if confidence >= 85:
                quality_label = "High"
                color = "#4CAF50"  # Green
            elif confidence >= 70:
                quality_label = "Medium"
                color = "#FFA726"  # Orange
            else:
                quality_label = "Low"
                color = "#EF5350"  # Red
                
            # Display prediction card
            st.markdown(
                f"""
                <div style="background-color: #F1F8E9; padding: 20px; border-radius: 10px; 
                border-left: 5px solid {color};">
                    <h3 style="color: #2E7D32;">Predicted Yield</h3>
                    <p style="font-size: 2.2rem; font-weight: bold; color: {color};">{predicted_yield_rounded} tons/acre</p>
                    <p style="font-size: 1.5rem;">Total: {total_yield} tons</p>
                    <p>Crop: <b>{input_data.get("crop_type", "Unknown")}</b></p>
                    <p>Field Area: <b>{area} acres</b></p>
                    <p>Confidence: <b>{round(confidence, 1)}%</b> ({quality_label})</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col2:
            # Create a gauge chart for confidence
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=confidence,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Prediction Confidence", "font": {"size": 24}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkblue"},
                    "bar": {"color": self._get_confidence_color(confidence)},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "gray",
                    "steps": [
                        {"range": [0, 50], "color": "#FFCDD2"},
                        {"range": [50, 75], "color": "#FFE0B2"},
                        {"range": [75, 100], "color": "#C8E6C9"}
                    ],
                }
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=50, b=10),
                font={"color": "#1B5E20", "family": "Arial"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Display factor importance
        st.markdown("### Factors Affecting Yield")
        
        # Convert factor importance to DataFrame
        factor_df = pd.DataFrame({
            "Factor": list(factor_importance.keys()),
            "Importance": [round(v * 100, 1) for v in factor_importance.values()]
        })
        factor_df = factor_df.sort_values("Importance", ascending=False)
        
        # Display as horizontal bar chart
        fig = px.bar(
            factor_df, 
            y="Factor", 
            x="Importance",
            orientation="h",
            color="Importance",
            color_continuous_scale=px.colors.sequential.Greens,
            title="Factor Importance (%)"
        )
        
        fig.update_layout(
            xaxis_title="Importance (%)",
            yaxis_title="",
            height=400,
            margin=dict(l=10, r=10, t=50, b=10),
            font={"color": "#1B5E20", "family": "Arial"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Get and display recommendations
        recommendations = self._generate_recommendations(factor_importance, input_data)
        
        st.markdown("### Recommendations for Improvement")
        
        for idx, (category, rec_list) in enumerate(recommendations.items()):
            with st.expander(f"{category} Recommendations", expanded=(idx == 0)):
                for rec in rec_list:
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 10px; padding: 10px; background-color: #F1F8E9; 
                        border-left: 4px solid #4CAF50; border-radius: 4px;">
                            <p style="margin: 0;">{rec}</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
    
    def _get_confidence_color(self, confidence: float) -> str:
        """Return a color based on the confidence level."""
        if confidence >= 85:
            return "#4CAF50"  # Green
        elif confidence >= 70:
            return "#FFA726"  # Orange
        else:
            return "#EF5350"  # Red
    
    def _generate_recommendations(self, factor_importance: Dict[str, float], 
                                 input_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Generate recommendations based on factor importance and input data.
        
        Args:
            factor_importance: Dictionary mapping factors to their importance
            input_data: Dictionary containing the input form data
            
        Returns:
            Dictionary mapping recommendation categories to lists of recommendations
        """
        # Sort factors by importance
        sorted_factors = sorted(factor_importance.items(), key=lambda x: x[1], reverse=True)
        top_factors = [f[0] for f in sorted_factors[:3]]
        
        recommendations = {
            "Soil Management": [],
            "Water Management": [],
            "Fertilizer Application": [],
            "Climate Adaptation": []
        }
        
        # Climate recommendations
        if "Temperature" in top_factors:
            crop_type = input_data.get("crop_type", "")
            temp = input_data.get("temperature", 0)
            
            if temp > 30:
                recommendations["Climate Adaptation"].append(
                    "Consider using shade nets or increasing irrigation frequency to mitigate high temperatures."
                )
            elif temp < 15:
                recommendations["Climate Adaptation"].append(
                    "Consider using row covers or plastic mulch to increase soil temperature."
                )
        
        if "Rainfall" in top_factors:
            rainfall = input_data.get("rainfall", 0)
            
            if rainfall < 500:
                recommendations["Water Management"].append(
                    "Implement water conservation practices such as mulching and reduced tillage to preserve soil moisture."
                )
            elif rainfall > 1200:
                recommendations["Water Management"].append(
                    "Ensure proper drainage systems are in place to prevent waterlogging and root diseases."
                )
        
        if "Humidity" in top_factors:
            humidity = input_data.get("humidity", 0)
            
            if humidity > 80:
                recommendations["Climate Adaptation"].append(
                    "Increase plant spacing to improve air circulation and reduce fungal disease risk."
                )
            elif humidity < 40:
                recommendations["Water Management"].append(
                    "Consider using drip irrigation and mulching to maintain soil moisture in low humidity conditions."
                )
        
        # Soil recommendations
        if "Soil pH" in top_factors:
            ph = input_data.get("soil_ph", 0)
            
            if ph < 5.5:
                recommendations["Soil Management"].append(
                    "Apply agricultural lime to increase soil pH. Target a pH of 6.0-7.0 for most crops."
                )
            elif ph > 7.5:
                recommendations["Soil Management"].append(
                    "Apply sulfur or organic matter like compost to gradually lower soil pH."
                )
        
        if "Soil Type" in top_factors:
            soil_type = input_data.get("soil_type", "")
            
            if soil_type == "Sandy":
                recommendations["Soil Management"].append(
                    "Add organic matter to improve water retention capacity and nutrient holding capacity."
                )
            elif soil_type == "Clay":
                recommendations["Soil Management"].append(
                    "Add organic matter and consider deep tillage to improve drainage and aeration."
                )
        
        # Nutrient recommendations
        if "Nitrogen" in top_factors or "Phosphorus" in top_factors or "Potassium" in top_factors:
            n_level = input_data.get("nitrogen_level", 0)
            p_level = input_data.get("phosphorus_level", 0)
            k_level = input_data.get("potassium_level", 0)
            
            if n_level < 50:
                recommendations["Fertilizer Application"].append(
                    "Increase nitrogen application. Consider using legume cover crops or applying nitrogen-rich fertilizers."
                )
            
            if p_level < 30:
                recommendations["Fertilizer Application"].append(
                    "Increase phosphorus application, especially during early growth stages to promote root development."
                )
            
            if k_level < 40:
                recommendations["Fertilizer Application"].append(
                    "Increase potassium application to improve crop quality and disease resistance."
                )
        
        # Irrigation recommendations
        if "Irrigation" in top_factors:
            irrigation = input_data.get("irrigation_method", "")
            
            if irrigation == "Flood":
                recommendations["Water Management"].append(
                    "Consider switching to drip or sprinkler irrigation to improve water use efficiency."
                )
            elif irrigation == "Rainfed":
                recommendations["Water Management"].append(
                    "Implement rainwater harvesting techniques to supplement rainfall during dry periods."
                )
        
        # Ensure each category has at least one recommendation
        for category in recommendations:
            if not recommendations[category]:
                if category == "Soil Management":
                    recommendations[category].append(
                        "Conduct regular soil tests to monitor soil health and nutrient levels."
                    )
                elif category == "Water Management":
                    recommendations[category].append(
                        "Monitor soil moisture regularly and adjust irrigation schedules based on crop needs and weather conditions."
                    )
                elif category == "Fertilizer Application":
                    recommendations[category].append(
                        "Apply fertilizers based on soil test results and crop requirements to optimize nutrient use efficiency."
                    )
                elif category == "Climate Adaptation":
                    recommendations[category].append(
                        "Monitor weather forecasts regularly and adjust farming operations accordingly."
                    )
        
        return recommendations 