import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from utils.risk_predictor import predict_airline_risk, get_risk_factors, predict_flight_risk
from models.risk_model import RiskModel
import base64
import os

st.set_page_config(page_title="Welcome To SentiFly", layout="wide")


def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        bg_image = f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(245, 245, 245, 0.7), rgba(245, 245, 245, 0.7)), 
                        url("data:image/jpg;base64,{encoded_string}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """
        st.markdown(bg_image, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Background image not found at: {image_path}")


set_background(r"SentiFly-main/Images/bg8.jpeg")

# Header
st.title("Risk Prediction")
st.markdown("Simple AI risk predictions for Indian airlines")

# Initialize risk model
@st.cache_resource
def load_risk_model():
    return RiskModel()

risk_model = load_risk_model()

# Simplified sidebar
st.sidebar.header("Quick Options")

# Set defaults for simplicity
selected_analysis = "Airline Risk Analysis"

# Main content based on selected analysis type
if selected_analysis == "Airline Risk Analysis":
    st.header("Indian Airline Risk Analysis")
    
    # Indian airlines only for simplicity
    airlines = ["Air India", "IndiGo", "SpiceJet", "GoAir", "Air Asia India", "Vistara"]
    selected_airline = st.selectbox("Select Airline", airlines)
    
    # Time period for prediction (simplified)
    prediction_periods = ["Next 6 Months", "Next 1 Year"]
    selected_prediction_period = st.selectbox("Prediction Period", prediction_periods)
    
    # Run prediction
    if st.button("Generate Risk Prediction"):
        with st.spinner(f"Analyzing risk factors and generating predictions for {selected_airline}..."):
            try:
                # Get prediction from risk predictor function
                risk_prediction = predict_airline_risk(
                    airline=selected_airline,
                    prediction_period=selected_prediction_period,
                    model=risk_model
                )
                
                if risk_prediction:
                    # Display overall risk score
                    st.subheader("Predicted Risk Assessment")
                    
                    # Create a gauge chart for risk score
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = risk_prediction['overall_risk_score'],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Risk Score (Higher = More Risk)"},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 25], 'color': "green"},
                                {'range': [25, 50], 'color': "yellow"},
                                {'range': [50, 75], 'color': "orange"},
                                {'range': [75, 100], 'color': "red"}
                            ],
                            'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.75,
                                'value': risk_prediction['overall_risk_score']
                            }
                        }
                    ))
                    
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interpret the risk score
                    risk_level = ""
                    if risk_prediction['overall_risk_score'] < 25:
                        risk_level = "Low Risk"
                        st.success(f"📊 {risk_level}: {selected_airline} has a favorable risk profile for the {selected_prediction_period.lower()}.")
                    elif risk_prediction['overall_risk_score'] < 50:
                        risk_level = "Moderate Risk"
                        st.info(f"📊 {risk_level}: {selected_airline} shows some risk factors that should be monitored for the {selected_prediction_period.lower()}.")
                    elif risk_prediction['overall_risk_score'] < 75:
                        risk_level = "Elevated Risk"
                        st.warning(f"📊 {risk_level}: {selected_airline} exhibits concerning risk factors for the {selected_prediction_period.lower()}.")
                    else:
                        risk_level = "High Risk"
                        st.error(f"📊 {risk_level}: {selected_airline} shows significant risk factors that require attention for the {selected_prediction_period.lower()}.")
                    
                    # Display risk factors
                    st.subheader("Risk Factor Analysis")
                    
                    # Create a DataFrame for risk factors
                    risk_factors_df = pd.DataFrame({
                        'Risk Factor': list(risk_prediction['risk_factors'].keys()),
                        'Risk Score': list(risk_prediction['risk_factors'].values())
                    })
                    
                    # Sort by risk score descending
                    risk_factors_df = risk_factors_df.sort_values(by='Risk Score', ascending=False)
                    
                    # Create horizontal bar chart
                    fig = px.bar(
                        risk_factors_df,
                        y='Risk Factor',
                        x='Risk Score',
                        orientation='h',
                        color='Risk Score',
                        color_continuous_scale=["green", "yellow", "orange", "red"],
                        range_color=[0, 100],
                        title=f"Risk Factors for {selected_airline}"
                    )
                    
                    fig.update_layout(
                        xaxis_title="Risk Score",
                        xaxis_range=[0, 100],
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Get detailed risk factors from utility function
                    detailed_factors = get_risk_factors(selected_airline)
                    
                    # Display detailed breakdown of each risk factor
                    for factor in risk_factors_df['Risk Factor']:
                        score = risk_prediction['risk_factors'][factor]
                        
                        with st.expander(f"{factor}: {score:.1f}/100"):
                            # Find detailed info for this factor if available
                            if detailed_factors and factor in detailed_factors:
                                factor_details = detailed_factors[factor]
                                st.markdown(f"**Description:** {factor_details['description']}")
                                st.markdown(f"**Analysis:** {factor_details['analysis']}")
                                st.markdown(f"**Trend:** {factor_details['trend']}")
                                st.markdown(f"**Mitigation Suggestions:** {factor_details['mitigation']}")
                            else:
                                # Generic descriptions if detailed info not available
                                if factor == "Fleet Age":
                                    st.markdown("**Description:** Analysis of the airline's fleet age and replacement schedule.")
                                    st.markdown("**Analysis:** Older aircraft may have higher maintenance requirements and be more prone to technical issues.")
                                    if score > 50:
                                        st.markdown("**Recommendation:** Consider accelerating fleet modernization plans.")
                                elif factor == "Maintenance Patterns":
                                    st.markdown("**Description:** Evaluation of maintenance procedures, compliance, and technical incidents.")
                                    st.markdown("**Analysis:** Proactive maintenance reduces the risk of in-flight technical problems.")
                                    if score > 50:
                                        st.markdown("**Recommendation:** Review maintenance processes and consider increasing inspection frequency.")
                                elif factor == "Operational Stress":
                                    st.markdown("**Description:** Assessment of operational factors including route complexity, flight frequency, and scheduling.")
                                    st.markdown("**Analysis:** High operational stress can lead to increased error rates and safety concerns.")
                                    if score > 50:
                                        st.markdown("**Recommendation:** Consider reducing schedule density and improving crew rest policies.")
                                elif factor == "Weather Exposure":
                                    st.markdown("**Description:** Analysis of exposure to severe weather conditions based on routes and seasonal patterns.")
                                    st.markdown("**Analysis:** Frequent exposure to severe weather increases risk of disruptions and incidents.")
                                    if score > 50:
                                        st.markdown("**Recommendation:** Enhance weather training and consider seasonal route adjustments.")
                                elif factor == "Regulatory Compliance":
                                    st.markdown("**Description:** Evaluation of compliance history with aviation regulations and safety directives.")
                                    st.markdown("**Analysis:** Strong regulatory compliance is associated with better safety outcomes.")
                                    if score > 50:
                                        st.markdown("**Recommendation:** Strengthen compliance monitoring and safety culture.")
                                else:
                                    st.markdown(f"**Description:** Analysis of {factor.lower()} as a risk factor.")
                                    st.markdown("**Analysis:** Based on historical patterns and industry benchmarks.")
                                    if score > 50:
                                        st.markdown("**Recommendation:** Consider this an area requiring attention and mitigation.")
                    
                    # Risk prediction over time
                    st.subheader("Risk Projection Over Time")
                    
                    # Create time points based on prediction period
                    if selected_prediction_period == "Next 6 Months":
                        months = 6
                        interval = "month"
                    elif selected_prediction_period == "Next 1 Year":
                        months = 12
                        interval = "month"
                    elif selected_prediction_period == "Next 3 Years":
                        months = 36
                        interval = "quarter"
                    else:  # Next 5 Years
                        months = 60
                        interval = "quarter"
                    
                    # Generate time points
                    start_date = datetime.now()
                    if interval == "month":
                        time_points = [start_date + timedelta(days=30*i) for i in range(months + 1)]
                        labels = [date.strftime("%b %Y") for date in time_points]
                    else:  # quarter
                        time_points = [start_date + timedelta(days=90*i) for i in range(months//3 + 1)]
                        labels = [date.strftime("%b %Y") for date in time_points]
                    
                    # Generate risk projection
                    base_risk = risk_prediction['overall_risk_score']
                    
                    # Use risk trend from prediction if available
                    if 'risk_trend' in risk_prediction:
                        risk_trend = risk_prediction['risk_trend']
                    else:
                        # Generate a plausible trend for demonstration
                        # Slightly increasing or decreasing based on current score
                        if base_risk < 30:
                            trend_direction = random.choice([0.5, 1, 1.5])  # Likely to increase
                        elif base_risk > 70:
                            trend_direction = random.choice([-1.5, -1, -0.5])  # Likely to decrease
                        else:
                            trend_direction = random.choice([-1, -0.5, 0, 0.5, 1])  # Could go either way
                        
                        risk_scores = [base_risk]
                        current_risk = base_risk
                        
                        for i in range(1, len(time_points)):
                            # Add some randomness to the trend
                            variation = random.uniform(-2, 2)
                            current_risk += trend_direction + variation
                            # Ensure within bounds
                            current_risk = max(0, min(100, current_risk))
                            risk_scores.append(current_risk)
                        
                        risk_trend = dict(zip(labels, risk_scores))
                    
                    # Create projection DataFrame
                    projection_df = pd.DataFrame({
                        'Time': list(risk_trend.keys()),
                        'Risk Score': list(risk_trend.values())
                    })
                    
                    # Create line chart
                    fig = px.line(
                        projection_df,
                        x='Time',
                        y='Risk Score',
                        title=f"Risk Score Projection for {selected_airline}",
                        markers=True
                    )
                    
                    fig.update_layout(
                        xaxis_title="Time Period",
                        yaxis_title="Projected Risk Score",
                        yaxis_range=[0, 100]
                    )
                    
                    # Add reference zones for risk levels
                    fig.add_hrect(y0=0, y1=25, line_width=0, fillcolor="green", opacity=0.1)
                    fig.add_hrect(y0=25, y1=50, line_width=0, fillcolor="yellow", opacity=0.1)
                    fig.add_hrect(y0=50, y1=75, line_width=0, fillcolor="orange", opacity=0.1)
                    fig.add_hrect(y0=75, y1=100, line_width=0, fillcolor="red", opacity=0.1)
                    
                    # Add annotations for risk levels
                    fig.add_annotation(x=projection_df['Time'].iloc[0], y=12.5, text="Low Risk", showarrow=False, font=dict(color="green"))
                    fig.add_annotation(x=projection_df['Time'].iloc[0], y=37.5, text="Moderate Risk", showarrow=False, font=dict(color="orange"))
                    fig.add_annotation(x=projection_df['Time'].iloc[0], y=62.5, text="Elevated Risk", showarrow=False, font=dict(color="orangered"))
                    fig.add_annotation(x=projection_df['Time'].iloc[0], y=87.5, text="High Risk", showarrow=False, font=dict(color="red"))
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Key insights
                    st.subheader("Key Insights")
                    
                    insights = risk_prediction.get('insights', [
                        f"{risk_level} profile detected for {selected_airline}.",
                        f"Most significant risk factors: {', '.join(risk_factors_df['Risk Factor'].head(3).tolist())}.",
                        f"Risk is projected to {risk_prediction.get('risk_direction', 'remain stable')} over the {selected_prediction_period.lower()}."
                    ])
                    
                    for insight in insights:
                        st.markdown(f"- {insight}")
                    
                    # Recommendations
                    st.subheader("Risk Mitigation Recommendations")
                    
                    recommendations = risk_prediction.get('recommendations', [
                        "Continue monitoring key risk factors, especially those with elevated scores.",
                        "Implement enhanced safety reviews for high-risk areas.",
                        "Benchmark safety practices against industry leaders.",
                        "Ensure maintenance schedules are optimized for fleet age and condition."
                    ])
                    
                    for recommendation in recommendations:
                        st.markdown(f"- {recommendation}")
                
                else:
                    st.error("Unable to generate risk prediction. Please try again later.")
            
            except Exception as e:
                st.error(f"Error generating risk prediction: {str(e)}")
                st.info("Unable to complete risk analysis. Please try again later.")

elif selected_analysis == "Flight-Specific Risk Prediction":
    st.header("Flight-Specific Risk Prediction")
    st.markdown("Analyze individual flight risk based on route, aircraft, weather, and historical data.")
    
    # Create a form for flight information
    with st.form("flight_risk_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Airline selection with focus on Indian airlines
            airlines = ["Air India", "IndiGo", "SpiceJet", "GoAir", "Air Asia India", "Vistara",
                      "American Airlines", "Delta Air Lines", "United Airlines", 
                      "British Airways", "Emirates", "Singapore Airlines"]
            flight_airline = st.selectbox("Airline", airlines)
            
            # Flight number
            flight_number = st.text_input("Flight Number", "")
            
            # Aircraft type
            aircraft_types = ["Boeing 737", "Boeing 787", "Boeing 777", "Airbus A320", "Airbus A321", "Airbus A330", "Airbus A350", "Embraer E190"]
            aircraft_type = st.selectbox("Aircraft Type", aircraft_types)
            
            # Aircraft age
            aircraft_age = st.slider("Aircraft Age (years)", 0, 30, 5)
        
        with col2:
            # Departure and arrival airports with focus on Indian airports
            airports = ["DEL - Delhi", "BOM - Mumbai", "MAA - Chennai", "BLR - Bengaluru", "HYD - Hyderabad", 
                        "CCU - Kolkata", "COK - Kochi", "AMD - Ahmedabad", "GOI - Goa", "PNQ - Pune",
                        "JFK - New York", "DXB - Dubai", "SIN - Singapore", "LHR - London", "BKK - Bangkok"]
            departure_airport = st.selectbox("Departure Airport", airports)
            arrival_airport = st.selectbox("Arrival Airport", airports, index=1)
            
            # Flight date
            flight_date = st.date_input("Flight Date", datetime.now())
            
            # Time of day
            times_of_day = ["Morning (6AM-10AM)", "Midday (10AM-2PM)", "Afternoon (2PM-6PM)", "Evening (6PM-10PM)", "Night (10PM-6AM)"]
            time_of_day = st.selectbox("Time of Day", times_of_day)
            
            # Season
            current_month = datetime.now().month
            seasons = ["Winter", "Spring", "Summer", "Fall"]
            default_season = 0  # Winter
            if 3 <= current_month <= 5:
                default_season = 1  # Spring
            elif 6 <= current_month <= 8:
                default_season = 2  # Summer
            elif 9 <= current_month <= 11:
                default_season = 3  # Fall
            season = st.selectbox("Season", seasons, index=default_season)
        
        # Additional risk factors
        st.subheader("Additional Risk Factors")
        
        col3, col4 = st.columns(2)
        
        with col3:
            weather_conditions = st.selectbox("Expected Weather Conditions", 
                                             ["Clear", "Light Rain", "Heavy Rain", "Thunderstorms", 
                                              "Snow", "Fog", "High Winds", "Unknown"])
            
            route_complexity = st.slider("Route Complexity", 1, 10, 5, 
                                        help="Higher values indicate more complex routes (e.g., mountain terrain, oceanic crossing)")
        
        with col4:
            maintenance_status = st.selectbox("Recent Maintenance", 
                                             ["Routine check completed", "Major overhaul completed", 
                                              "Pending scheduled maintenance", "Unknown"])
            
            previous_incidents = st.selectbox("Previous Route Incidents", 
                                             ["None in past 5 years", "Minor incidents only", 
                                              "One major incident", "Multiple incidents"])
        
        submitted = st.form_submit_button("Predict Flight Risk")
    
    if submitted:
        with st.spinner("Analyzing flight risk factors..."):
            try:
                # Prepare flight data
                flight_data = {
                    "airline": flight_airline,
                    "flight_number": flight_number,
                    "aircraft_type": aircraft_type,
                    "aircraft_age": aircraft_age,
                    "departure_airport": departure_airport.split(" - ")[0],
                    "arrival_airport": arrival_airport.split(" - ")[0],
                    "flight_date": flight_date.strftime("%Y-%m-%d"),
                    "time_of_day": time_of_day,
                    "season": season,
                    "weather_conditions": weather_conditions,
                    "route_complexity": route_complexity,
                    "maintenance_status": maintenance_status,
                    "previous_incidents": previous_incidents
                }
                
                # Get prediction from risk predictor function
                risk_prediction = predict_flight_risk(
                    flight_data=flight_data,
                    model=risk_model
                )
                
                if risk_prediction:
                    # Create columns for results
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("Flight Risk Assessment")
                        
                        # Create risk score display
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = risk_prediction['risk_score'],
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Flight Risk Score"},
                            gauge = {
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 25], 'color': "green"},
                                    {'range': [25, 50], 'color': "yellow"},
                                    {'range': [50, 75], 'color': "orange"},
                                    {'range': [75, 100], 'color': "red"}
                                ],
                                'threshold': {
                                    'line': {'color': "black", 'width': 4},
                                    'thickness': 0.75,
                                    'value': risk_prediction['risk_score']
                                }
                            }
                        ))
                        
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Risk level interpretation
                        risk_level = ""
                        if risk_prediction['risk_score'] < 25:
                            risk_level = "Low Risk"
                            st.success(f"✅ {risk_level}: This flight has a favorable risk profile.")
                        elif risk_prediction['risk_score'] < 50:
                            risk_level = "Moderate Risk"
                            st.info(f"ℹ️ {risk_level}: This flight shows some risk factors that should be monitored.")
                        elif risk_prediction['risk_score'] < 75:
                            risk_level = "Elevated Risk"
                            st.warning(f"⚠️ {risk_level}: This flight exhibits concerning risk factors.")
                        else:
                            risk_level = "High Risk"
                            st.error(f"🚨 {risk_level}: This flight shows significant risk factors that require attention.")
                        
                        # Risk comparison
                        st.subheader("Risk Comparison")
                        
                        # Create comparison data
                        comparison_data = {
                            "Category": ["This Flight", "Airline Average", "Route Average", "Industry Average"],
                            "Risk Score": [
                                risk_prediction['risk_score'],
                                risk_prediction.get('airline_average', random.uniform(30, 50)),
                                risk_prediction.get('route_average', random.uniform(30, 50)),
                                risk_prediction.get('industry_average', 40)
                            ]
                        }
                        
                        comparison_df = pd.DataFrame(comparison_data)
                        
                        # Create comparison chart
                        fig = px.bar(
                            comparison_df,
                            x="Category",
                            y="Risk Score",
                            color="Risk Score",
                            color_continuous_scale=["green", "yellow", "orange", "red"],
                            range_color=[0, 100],
                            title="Risk Score Comparison"
                        )
                        
                        fig.update_layout(
                            xaxis_title="",
                            yaxis_title="Risk Score",
                            yaxis_range=[0, 100]
                        )
                        
                        # Add reference lines for risk levels
                        fig.add_shape(
                            type="line",
                            x0=-0.5,
                            y0=25,
                            x1=3.5,
                            y1=25,
                            line=dict(color="green", width=2, dash="dash")
                        )
                        fig.add_shape(
                            type="line",
                            x0=-0.5,
                            y0=50,
                            x1=3.5,
                            y1=50,
                            line=dict(color="orange", width=2, dash="dash")
                        )
                        fig.add_shape(
                            type="line",
                            x0=-0.5,
                            y0=75,
                            x1=3.5,
                            y1=75,
                            line=dict(color="red", width=2, dash="dash")
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.subheader("Key Risk Factors")
                        
                        # Display contributing risk factors
                        risk_factors = risk_prediction.get('risk_factors', {})
                        
                        if risk_factors:
                            # Convert to DataFrame for display
                            risk_factors_df = pd.DataFrame({
                                'Factor': list(risk_factors.keys()),
                                'Impact': list(risk_factors.values())
                            })
                            
                            # Sort by impact
                            risk_factors_df = risk_factors_df.sort_values(by='Impact', ascending=False)
                            
                            # Create horizontal bar chart
                            fig = px.bar(
                                risk_factors_df,
                                y='Factor',
                                x='Impact',
                                orientation='h',
                                color='Impact',
                                color_continuous_scale=["green", "yellow", "orange", "red"],
                                range_color=[0, 100],
                                title="Contributing Risk Factors"
                            )
                            
                            fig.update_layout(
                                xaxis_title="Impact Level",
                                xaxis_range=[0, 100],
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Display specific risk factors as bullet points
                            for idx, row in risk_factors_df.iterrows():
                                if row['Impact'] >= 75:
                                    st.error(f"🚨 {row['Factor']}: Very High Impact")
                                elif row['Impact'] >= 50:
                                    st.warning(f"⚠️ {row['Factor']}: High Impact")
                                elif row['Impact'] >= 25:
                                    st.info(f"ℹ️ {row['Factor']}: Moderate Impact")
                                else:
                                    st.success(f"✅ {row['Factor']}: Low Impact")
                        else:
                            st.info("No specific risk factors identified.")
                    
                    # Risk mitigation recommendations
                    st.subheader("Risk Mitigation Recommendations")
                    
                    recommendations = risk_prediction.get('recommendations', [])
                    
                    if not recommendations:
                        # Generate generic recommendations based on risk level
                        if risk_prediction['risk_score'] < 25:
                            recommendations = [
                                "Standard pre-flight checks are sufficient.",
                                "Follow normal operational procedures.",
                                "No additional measures required."
                            ]
                        elif risk_prediction['risk_score'] < 50:
                            recommendations = [
                                "Conduct thorough pre-flight checks with special attention to key systems.",
                                "Monitor weather conditions closely before departure.",
                                "Ensure all crew members are briefed on potential risk areas."
                            ]
                        elif risk_prediction['risk_score'] < 75:
                            recommendations = [
                                "Consider additional technical inspections before departure.",
                                "Implement enhanced monitoring during flight.",
                                "Review contingency plans for this route.",
                                "Consider additional fuel reserves if weather is a factor."
                            ]
                        else:
                            recommendations = [
                                "Comprehensive technical inspection strongly recommended.",
                                "Consider postponing if severe weather is expected.",
                                "Assign most experienced crew members.",
                                "Implement maximum safety protocols.",
                                "Consider alternative routing if applicable."
                            ]
                    
                    for recommendation in recommendations:
                        st.markdown(f"- {recommendation}")
                    
                    # Similar flights
                    st.subheader("Similar Flights Analysis")
                    
                    # This would typically show real data about similar flights
                    # For demo, create sample data
                    similar_flights = risk_prediction.get('similar_flights', [])
                    
                    if not similar_flights:
                        # Generate sample similar flights
                        for i in range(5):
                            variation = random.uniform(-15, 15)
                            similar_flight = {
                                "flight_number": f"{flight_airline[:2]}{random.randint(100, 9999)}",
                                "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
                                "risk_score": max(0, min(100, risk_prediction['risk_score'] + variation)),
                                "status": "Completed Safely" if random.random() < 0.9 else random.choice(["Delayed", "Diverted", "Minor Incident"])
                            }
                            similar_flights.append(similar_flight)
                    
                    # Create DataFrame for similar flights
                    similar_df = pd.DataFrame(similar_flights)
                    
                    st.dataframe(similar_df, use_container_width=True)
                    
                    # Weather impact visualization if applicable
                    if weather_conditions != "Clear" and weather_conditions != "Unknown":
                        st.subheader("Weather Impact Analysis")
                        
                        st.markdown(f"Selected weather condition: **{weather_conditions}**")
                        
                        # Create weather impact visualization
                        weather_impact = {
                            "Clear": 0,
                            "Light Rain": 15,
                            "Heavy Rain": 40,
                            "Thunderstorms": 70,
                            "Snow": 60,
                            "Fog": 50,
                            "High Winds": 55,
                            "Unknown": 25
                        }
                        
                        weather_df = pd.DataFrame({
                            "Condition": list(weather_impact.keys()),
                            "Risk Impact": list(weather_impact.values())
                        })
                        
                        fig = px.bar(
                            weather_df,
                            x="Condition",
                            y="Risk Impact",
                            color="Risk Impact",
                            color_continuous_scale=["green", "yellow", "orange", "red"],
                            range_color=[0, 100],
                            title="Weather Condition Risk Impact"
                        )
                        
                        fig.update_layout(
                            xaxis_title="Weather Condition",
                            yaxis_title="Risk Impact",
                            yaxis_range=[0, 100]
                        )
                        
                        # Highlight selected weather condition
                        selected_idx = list(weather_impact.keys()).index(weather_conditions)
                        fig.add_annotation(
                            x=selected_idx,
                            y=weather_impact[weather_conditions] + 5,
                            text="Selected",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#000000"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.error("Unable to generate flight risk prediction. Please try again with different parameters.")
            
            except Exception as e:
                st.error(f"Error predicting flight risk: {str(e)}")
                st.info("Unable to complete flight risk analysis. Please try again later.")

else:  # Industry Risk Trends
    st.header("Industry-Wide Risk Trends")
    st.markdown("Analysis of broad aviation risk trends and patterns across the industry.")
    
    # Time period selection
    time_periods = ["Last 12 Months", "Last 3 Years", "Last 5 Years", "Last 10 Years"]
    selected_time = st.selectbox("Time Period", time_periods)
    
    # Create tabs for different trend views
    trend_tab1, trend_tab2, trend_tab3 = st.tabs(["Risk by Airline", "Risk by Region", "Risk by Aircraft Type"])
    
    # Tab 1: Risk by Airline
    with trend_tab1:
        st.subheader("Risk Score Trends by Airline")
        
        with st.spinner("Analyzing industry risk trends..."):
            try:
                # This would typically come from a database or API
                # Generate sample data for demonstration
                airlines = ["Air India", "IndiGo", "SpiceJet", "GoAir", "Air Asia India", "Vistara",
                            "American Airlines", "Delta Air Lines", "United Airlines", 
                            "British Airways", "Emirates", "Singapore Airlines"]
                
                # Generate timeline based on selected period
                if selected_time == "Last 12 Months":
                    months = 12
                    start_date = datetime.now() - timedelta(days=365)
                    time_points = [(start_date + timedelta(days=30*i)).strftime("%b %Y") for i in range(months + 1)]
                elif selected_time == "Last 3 Years":
                    quarters = 12
                    start_date = datetime.now() - timedelta(days=365*3)
                    time_points = [(start_date + timedelta(days=90*i)).strftime("%b %Y") for i in range(quarters + 1)]
                elif selected_time == "Last 5 Years":
                    quarters = 20
                    start_date = datetime.now() - timedelta(days=365*5)
                    time_points = [(start_date + timedelta(days=90*i)).strftime("%b %Y") for i in range(quarters + 1)]
                else:  # Last 10 Years
                    years = 10
                    start_date = datetime.now() - timedelta(days=365*10)
                    time_points = [(start_date + timedelta(days=365*i)).strftime("%Y") for i in range(years + 1)]
                
                # Generate risk scores for each airline over time
                trend_data = []
                
                for airline in airlines:
                    # Start with a base risk based on airline
                    base_risk = random.uniform(30, 60)
                    
                    # Generate a trend direction
                    trend = random.uniform(-0.5, 0.5)
                    
                    for time_point in time_points:
                        # Add some random variation
                        variation = random.uniform(-5, 5)
                        risk_score = max(0, min(100, base_risk + variation))
                        
                        trend_data.append({
                            "Airline": airline,
                            "Time": time_point,
                            "Risk Score": risk_score
                        })
                        
                        # Update base risk with trend for next time point
                        base_risk += trend
                
                # Convert to DataFrame
                trend_df = pd.DataFrame(trend_data)
                
                # Create line chart
                fig = px.line(
                    trend_df,
                    x="Time",
                    y="Risk Score",
                    color="Airline",
                    title="Risk Score Trends by Airline",
                    markers=True
                )
                
                fig.update_layout(
                    xaxis_title="Time Period",
                    yaxis_title="Risk Score",
                    yaxis_range=[0, 100],
                    legend_title="Airline"
                )
                
                # Add reference zones for risk levels
                fig.add_hrect(y0=0, y1=25, line_width=0, fillcolor="green", opacity=0.1)
                fig.add_hrect(y0=25, y1=50, line_width=0, fillcolor="yellow", opacity=0.1)
                fig.add_hrect(y0=50, y1=75, line_width=0, fillcolor="orange", opacity=0.1)
                fig.add_hrect(y0=75, y1=100, line_width=0, fillcolor="red", opacity=0.1)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate current risk for each airline
                current_risks = trend_df[trend_df["Time"] == time_points[-1]].sort_values(by="Risk Score")
                
                # Create bar chart of current risks
                fig = px.bar(
                    current_risks,
                    x="Airline",
                    y="Risk Score",
                    color="Risk Score",
                    color_continuous_scale=["green", "yellow", "orange", "red"],
                    range_color=[0, 100],
                    title="Current Risk Scores by Airline"
                )
                
                fig.update_layout(
                    xaxis_title="Airline",
                    yaxis_title="Risk Score",
                    yaxis_range=[0, 100]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate trend direction for each airline
                if len(time_points) >= 3:
                    trend_analysis = []
                    
                    for airline in airlines:
                        airline_data = trend_df[trend_df["Airline"] == airline].sort_values(by="Time")
                        first_third = airline_data["Risk Score"].iloc[:len(airline_data)//3].mean()
                        last_third = airline_data["Risk Score"].iloc[-len(airline_data)//3:].mean()
                        trend_diff = last_third - first_third
                        
                        trend_direction = "Improving" if trend_diff < -5 else "Worsening" if trend_diff > 5 else "Stable"
                        
                        trend_analysis.append({
                            "Airline": airline,
                            "Current Risk": airline_data["Risk Score"].iloc[-1],
                            "Trend Direction": trend_direction,
                            "Change": trend_diff
                        })
                    
                    # Convert to DataFrame
                    trend_analysis_df = pd.DataFrame(trend_analysis)
                    
                    # Display trend analysis
                    st.subheader("Airline Risk Trend Analysis")
                    
                    # Format the DataFrame for display
                    display_df = trend_analysis_df.copy()
                    display_df["Current Risk"] = display_df["Current Risk"].map(lambda x: f"{x:.1f}")
                    display_df["Change"] = display_df["Change"].map(lambda x: f"{x:+.1f}")
                    
                    # Add color coding to trend direction
                    def color_trend(val):
                        if val == "Improving":
                            return "background-color: #c6efce; color: #006100"
                        elif val == "Worsening":
                            return "background-color: #ffc7ce; color: #9c0006"
                        return ""
                    
                    # Display with styling
                    st.dataframe(display_df.style.applymap(color_trend, subset=["Trend Direction"]), use_container_width=True)
            
            except Exception as e:
                st.error(f"Error analyzing risk trends: {str(e)}")
                st.info("Unable to retrieve trend data. Please try again later.")
    
    # Tab 2: Risk by Region
    with trend_tab2:
        st.subheader("Risk Score Trends by Region")
        
        with st.spinner("Analyzing regional risk trends..."):
            try:
                # Generate sample data for regions with focus on Indian regions
                regions = ["North India", "South India", "East India", "West India", "Northeast India", "Central India", 
                          "Asia Pacific", "Europe", "Middle East", "North America"]
                
                # Generate regional risk scores
                region_data = []
                
                for region in regions:
                    # Assign a base risk for each region
                    if region == "North India":
                        base_risk = random.uniform(30, 45)
                    elif region == "South India":
                        base_risk = random.uniform(32, 42)
                    elif region == "East India":
                        base_risk = random.uniform(35, 45)
                    elif region == "West India":
                        base_risk = random.uniform(30, 40)
                    elif region == "Northeast India":
                        base_risk = random.uniform(38, 48)
                    elif region == "Central India":
                        base_risk = random.uniform(35, 45)
                    elif region == "North America":
                        base_risk = random.uniform(25, 35)
                    elif region == "Europe":
                        base_risk = random.uniform(28, 38)
                    elif region == "Asia Pacific":
                        base_risk = random.uniform(32, 42)
                    else:  # Middle East
                        base_risk = random.uniform(35, 45)
                    
                    # Generate a trend direction
                    trend = random.uniform(-0.3, 0.3)
                    
                    for time_point in time_points:
                        # Add some random variation
                        variation = random.uniform(-3, 3)
                        risk_score = max(0, min(100, base_risk + variation))
                        
                        region_data.append({
                            "Region": region,
                            "Time": time_point,
                            "Risk Score": risk_score
                        })
                        
                        # Update base risk with trend for next time point
                        base_risk += trend
                
                # Convert to DataFrame
                region_df = pd.DataFrame(region_data)
                
                # Create line chart
                fig = px.line(
                    region_df,
                    x="Time",
                    y="Risk Score",
                    color="Region",
                    title="Risk Score Trends by Region",
                    markers=True
                )
                
                fig.update_layout(
                    xaxis_title="Time Period",
                    yaxis_title="Risk Score",
                    yaxis_range=[0, 100],
                    legend_title="Region"
                )
                
                # Add reference zones for risk levels
                fig.add_hrect(y0=0, y1=25, line_width=0, fillcolor="green", opacity=0.1)
                fig.add_hrect(y0=25, y1=50, line_width=0, fillcolor="yellow", opacity=0.1)
                fig.add_hrect(y0=50, y1=75, line_width=0, fillcolor="orange", opacity=0.1)
                fig.add_hrect(y0=75, y1=100, line_width=0, fillcolor="red", opacity=0.1)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Current regional risk map
                st.subheader("Current Risk Score by Region")
                
                # Get current risk for each region
                current_region_risks = region_df[region_df["Time"] == time_points[-1]]
                
                # Create choropleth map
                fig = px.choropleth(
                    current_region_risks,
                    locations="Region",
                    locationmode="country names",
                    color="Risk Score",
                    color_continuous_scale=["green", "yellow", "orange", "red"],
                    range_color=[0, 100],
                    title="Global Risk Score Distribution",
                    labels={"Risk Score": "Risk Level"}
                )
                
                fig.update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=True,
                        projection_type='equirectangular'
                    )
                )
                
                # Note: This is a simplified map and may not work perfectly with the region names as given
                # A real implementation would use ISO country codes or more specific location data
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display current region risks as a bar chart as fallback
                fig = px.bar(
                    current_region_risks,
                    x="Region",
                    y="Risk Score",
                    color="Risk Score",
                    color_continuous_scale=["green", "yellow", "orange", "red"],
                    range_color=[0, 100],
                    title="Current Risk Scores by Region"
                )
                
                fig.update_layout(
                    xaxis_title="Region",
                    yaxis_title="Risk Score",
                    yaxis_range=[0, 100]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Regional risk factors
                st.subheader("Key Regional Risk Factors")
                
                # Create a table of regional risk factors
                regional_factors = []
                
                for region in regions:
                    if region == "North India":
                        factors = ["Fog during winter", "High traffic density", "Variable weather conditions"]
                        mitigation = "Advanced navigation systems and enhanced pilot training for low visibility"
                    elif region == "South India":
                        factors = ["Monsoon impacts", "Coastal weather patterns", "Airport modernization"]
                        mitigation = "Weather monitoring systems and improved drainage infrastructure"
                    elif region == "East India":
                        factors = ["Cyclone exposure", "Infrastructure development", "Seasonal flooding"]
                        mitigation = "Advanced weather tracking and emergency response protocols"
                    elif region == "West India":
                        factors = ["Dense air traffic", "Urban airport challenges", "Monsoon disruptions"]
                        mitigation = "Traffic management systems and improved scheduling"
                    elif region == "Northeast India":
                        factors = ["Mountainous terrain", "Limited infrastructure", "Weather extremes"]
                        mitigation = "Special approach procedures and pilot terrain training"
                    elif region == "Central India":
                        factors = ["Summer heat impacts", "Developing infrastructure", "Dust storms"]
                        mitigation = "Heat management protocols and surface maintenance"
                    elif region == "North America":
                        factors = ["Weather disruptions", "Air traffic congestion", "Aging infrastructure"]
                        mitigation = "Strong regulatory oversight and technological investments"
                    elif region == "Europe":
                        factors = ["Airspace congestion", "Weather variability", "Mixed fleet age"]
                        mitigation = "Strong regulatory framework and standardized procedures"
                    elif region == "Asia Pacific":
                        factors = ["Rapid growth", "Variable regulatory standards", "Weather extremes"]
                        mitigation = "Improving regulatory harmonization and infrastructure investment"
                    else:  # Middle East
                        factors = ["Geopolitical tensions", "Extreme heat", "Rapid aviation sector growth"]
                        mitigation = "Modern fleets and stringent operational standards"
                    
                    regional_factors.append({
                        "Region": region,
                        "Key Risk Factors": ", ".join(factors),
                        "Mitigation Strategies": mitigation
                    })
                
                # Convert to DataFrame
                factors_df = pd.DataFrame(regional_factors)
                
                st.dataframe(factors_df, use_container_width=True)
            
            except Exception as e:
                st.error(f"Error analyzing regional trends: {str(e)}")
                st.info("Unable to retrieve regional data. Please try again later.")
    
    # Tab 3: Risk by Aircraft Type
    with trend_tab3:
        st.subheader("Risk Analysis by Aircraft Type")
        
        with st.spinner("Analyzing aircraft type risk data..."):
            try:
                # Generate sample data for aircraft types
                aircraft_types = ["Boeing 737", "Boeing 787", "Boeing 777", "Airbus A320", "Airbus A321", "Airbus A330", "Airbus A350", "Embraer E190"]
                
                # Generate risk scores by aircraft type
                aircraft_data = []
                
                for aircraft in aircraft_types:
                    # Assign a base risk for each aircraft type
                    # Newer aircraft generally have lower risk scores
                    if aircraft in ["Boeing 787", "Airbus A350"]:
                        base_risk = random.uniform(20, 35)
                    elif aircraft in ["Boeing 777", "Airbus A330", "Airbus A321"]:
                        base_risk = random.uniform(30, 45)
                    else:
                        base_risk = random.uniform(35, 50)
                    
                    # Generate a trend direction
                    trend = random.uniform(-0.2, 0.2)
                    
                    for time_point in time_points:
                        # Add some random variation
                        variation = random.uniform(-4, 4)
                        risk_score = max(0, min(100, base_risk + variation))
                        
                        aircraft_data.append({
                            "Aircraft Type": aircraft,
                            "Time": time_point,
                            "Risk Score": risk_score
                        })
                        
                        # Update base risk with trend for next time point
                        base_risk += trend
                
                # Convert to DataFrame
                aircraft_df = pd.DataFrame(aircraft_data)
                
                # Create line chart
                fig = px.line(
                    aircraft_df,
                    x="Time",
                    y="Risk Score",
                    color="Aircraft Type",
                    title="Risk Score Trends by Aircraft Type",
                    markers=True
                )
                
                fig.update_layout(
                    xaxis_title="Time Period",
                    yaxis_title="Risk Score",
                    yaxis_range=[0, 100],
                    legend_title="Aircraft Type"
                )
                
                # Add reference zones for risk levels
                fig.add_hrect(y0=0, y1=25, line_width=0, fillcolor="green", opacity=0.1)
                fig.add_hrect(y0=25, y1=50, line_width=0, fillcolor="yellow", opacity=0.1)
                fig.add_hrect(y0=50, y1=75, line_width=0, fillcolor="orange", opacity=0.1)
                fig.add_hrect(y0=75, y1=100, line_width=0, fillcolor="red", opacity=0.1)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Current aircraft type risks
                current_aircraft_risks = aircraft_df[aircraft_df["Time"] == time_points[-1]].sort_values(by="Risk Score")
                
                # Create bar chart
                fig = px.bar(
                    current_aircraft_risks,
                    x="Aircraft Type",
                    y="Risk Score",
                    color="Risk Score",
                    color_continuous_scale=["green", "yellow", "orange", "red"],
                    range_color=[0, 100],
                    title="Current Risk Scores by Aircraft Type"
                )
                
                fig.update_layout(
                    xaxis_title="Aircraft Type",
                    yaxis_title="Risk Score",
                    yaxis_range=[0, 100]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Aircraft type risk factors
                st.subheader("Aircraft Type Risk Analysis")
                
                # Create a table of aircraft risk factors
                aircraft_factors = []
                
                for aircraft in aircraft_types:
                    # Set age and incidents based on type
                    if aircraft in ["Boeing 787", "Airbus A350"]:
                        age_category = "New Generation"
                        fleet_age = random.randint(1, 8)
                        incidents = random.randint(0, 5)
                    elif aircraft in ["Boeing 777", "Airbus A330", "Airbus A321"]:
                        age_category = "Mid-Generation"
                        fleet_age = random.randint(5, 15)
                        incidents = random.randint(3, 15)
                    else:
                        age_category = "Mature Design"
                        fleet_age = random.randint(10, 25)
                        incidents = random.randint(8, 25)
                    
                    # Calculate a reliability score inversely related to age and incidents
                    reliability = 100 - (fleet_age * 1.5) - (incidents * 2)
                    reliability = max(30, min(95, reliability))
                    
                    # Set risk factors based on aircraft type
                    if aircraft.startswith("Boeing"):
                        if aircraft == "Boeing 737":
                            specific_factors = "Varied configurations and generations"
                        elif aircraft == "Boeing 787":
                            specific_factors = "New technology systems"
                        else:
                            specific_factors = "Complex systems integration"
                    elif aircraft.startswith("Airbus"):
                        if aircraft in ["Airbus A320", "Airbus A321"]:
                            specific_factors = "High cycle operations"
                        else:
                            specific_factors = "Advanced automation systems"
                    else:
                        specific_factors = "Regional operations profile"
                    
                    aircraft_factors.append({
                        "Aircraft Type": aircraft,
                        "Age Category": age_category,
                        "Average Fleet Age": fleet_age,
                        "Incidents (5yr)": incidents,
                        "Reliability Score": round(reliability, 1),
                        "Key Risk Factors": specific_factors
                    })
                
                # Convert to DataFrame
                factors_df = pd.DataFrame(aircraft_factors)
                
                # Sort by reliability score
                factors_df = factors_df.sort_values(by="Reliability Score", ascending=False)
                
                st.dataframe(factors_df, use_container_width=True)
                
                # Relationship between age and risk
                st.subheader("Relationship: Aircraft Age vs. Risk Score")
                
                # Create a scatter plot of age vs. risk
                fig = px.scatter(
                    factors_df,
                    x="Average Fleet Age",
                    y="Reliability Score",
                    color="Age Category",
                    size="Incidents (5yr)",
                    hover_name="Aircraft Type",
                    title="Aircraft Age, Reliability, and Incident Correlation"
                )
                
                fig.update_layout(
                    xaxis_title="Average Fleet Age (Years)",
                    yaxis_title="Reliability Score"
                )
                
                # Add a trend line
                fig.add_shape(
                    type="line",
                    x0=0,
                    y0=95,
                    x1=25,
                    y1=30,
                    line=dict(color="gray", width=2, dash="dash")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"Error analyzing aircraft data: {str(e)}")
                st.info("Unable to retrieve aircraft type data. Please try again later.")

# Add information about the AI risk prediction model
with st.expander("About the Risk Prediction Model"):
    st.markdown("""
    ### SentiFly Risk Prediction Methodology for Indian Airlines

    Our AI-powered risk prediction system uses machine learning to analyze patterns in historical aviation data and predict potential safety risks for Indian airlines including Air India, IndiGo, SpiceJet, GoAir, Air Asia India, and Vistara. The model incorporates:

    **Data Sources**:
    - Historical accident and incident databases
    - Aircraft maintenance records and reliability data
    - Weather patterns and seasonal factors
    - Airline operational data and safety practices
    - Regulatory compliance records
    - SentiFly sentiment analysis results from customer reviews

    **Model Architecture**:
    - Multi-factor risk assessment framework
    - Time-series analysis for trend prediction
    - Comparative benchmarking against industry standards
    - Pattern recognition for anomaly detection
    - Sentiment analysis correlation with safety outcomes

    **Limitations**:
    - Predictions are based on historical patterns and may not capture unprecedented events
    - Risk assessment is probabilistic in nature, not deterministic
    - Model accuracy depends on data quality and completeness
    - Regular updates are needed to incorporate new safety information

    **How to Use Results**:
    - Risk scores should be used as indicators, not absolute measurements
    - Higher risk scores indicate areas that may need additional attention
    - Compare scores across airlines, routes, and time periods for context
    - Use recommendations as a starting point for further investigation
    """)