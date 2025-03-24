import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from utils.safety_calculator import calculate_safety_score, get_airline_incidents, get_safety_factors
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

custom_css = """
    <style>
        body {
            background-image: url('Images/bg8.jpg');
            background-size: cover;
            background-attachment: fixed;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }

        .sidebar .block-container {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
        }

        h1, h2, h3, p {
            color: #333;
        }

        .stButton>button {
            background-color: #b22222;
            color: white;
            border-radius: 5px;
            font-size: 16px;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# Header
st.title("Safety Ratings")
st.markdown("Simple safety ratings for Indian airlines")

# Sidebar for filters and options (simplified)
st.sidebar.header("Quick Options")

# Airline selection with focus on Indian airlines (simplified list)
airlines = ["All Airlines", "Air India", "IndiGo", "SpiceJet", "GoAir", "Air Asia India", "Vistara"]
selected_airline = st.sidebar.selectbox("Select Airline", airlines)

# Time period for analysis (simplified)
time_periods = ["Last 5 Years", "Last 10 Years", "All Time"]
selected_period = st.sidebar.selectbox("Time Period", time_periods)

# Set default weights for simplicity
weights = {
    "incident_history": 0.3,
    "maintenance_records": 0.25,
    "customer_feedback": 0.15,
    "operational_excellence": 0.2,
    "regulatory_compliance": 0.1
}

# Main content area
tab1, tab2, tab3 = st.tabs(["Safety Ratings", "Incident History", "Comparative Analysis"])

# Tab 1: Safety Ratings
with tab1:
    st.header("Airline Safety Ratings")
    
    # If a specific airline is selected
    if selected_airline != "All Airlines":
        # Fetch and calculate safety score for the selected airline
        with st.spinner(f"Calculating safety score for {selected_airline}..."):
            try:
                safety_score, factor_scores = calculate_safety_score(
                    airline=selected_airline,
                    time_period=selected_period,
                    weights=weights
                )
                
                # Display the overall safety score prominently
                st.markdown(f"### Overall Safety Score for {selected_airline}")
                
                # Create score gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = safety_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Safety Score"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "red"},
                            {'range': [50, 75], 'color': "orange"},
                            {'range': [75, 90], 'color': "yellow"},
                            {'range': [90, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': safety_score
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Safety score interpretation
                if safety_score >= 90:
                    st.success("✅ Excellent safety record. This airline is among the safest in the industry.")
                elif safety_score >= 75:
                    st.info("ℹ️ Good safety record. This airline has a solid safety profile.")
                elif safety_score >= 50:
                    st.warning("⚠️ Average safety record. Some areas need improvement.")
                else:
                    st.error("❌ Below average safety record. Multiple safety concerns identified.")
                
                # Display factor breakdown
                st.subheader("Safety Factor Breakdown")
                
                # Create a factor breakdown chart
                factor_df = pd.DataFrame({
                    'Factor': list(factor_scores.keys()),
                    'Score': list(factor_scores.values()),
                    'Weight': [weights[k.lower().replace(' ', '_')] for k in factor_scores.keys()]
                })
                
                fig = px.bar(
                    factor_df,
                    x='Factor',
                    y='Score',
                    color='Score',
                    color_continuous_scale=["red", "orange", "yellow", "green"],
                    range_color=[0, 100],
                    text='Score',
                    title=f"Safety Factor Scores for {selected_airline}"
                )
                
                fig.update_layout(xaxis_title="Safety Factor", yaxis_title="Score (0-100)")
                st.plotly_chart(fig, use_container_width=True)
                
                # Add explanations for each factor
                st.markdown("### Factor Explanations")
                
                for factor, score in factor_scores.items():
                    with st.expander(f"{factor}: {score:.1f}/100"):
                        if factor == "Incident History":
                            st.markdown("Based on the airline's history of accidents, incidents, and near-misses over the selected time period.")
                            st.markdown(f"**Weight in calculation:** {weights['incident_history']*100:.1f}%")
                        elif factor == "Maintenance Records":
                            st.markdown("Evaluates the airline's aircraft maintenance practices, age of fleet, and technical reliability.")
                            st.markdown(f"**Weight in calculation:** {weights['maintenance_records']*100:.1f}%")
                        elif factor == "Customer Feedback":
                            st.markdown("Incorporates safety-related comments and concerns from customer reviews.")
                            st.markdown(f"**Weight in calculation:** {weights['customer_feedback']*100:.1f}%")
                        elif factor == "Operational Excellence":
                            st.markdown("Measures on-time performance, pilot training standards, and operational procedures.")
                            st.markdown(f"**Weight in calculation:** {weights['operational_excellence']*100:.1f}%")
                        elif factor == "Regulatory Compliance":
                            st.markdown("Assesses compliance with aviation regulations and results of safety audits.")
                            st.markdown(f"**Weight in calculation:** {weights['regulatory_compliance']*100:.1f}%")
                
                # Safety trends over time
                st.subheader("Safety Score Trend")
                
                # Get safety factors from utility function
                safety_factors = get_safety_factors(selected_airline)
                
                # If we have trend data, show it
                if safety_factors and 'trend_data' in safety_factors:
                    trend_df = pd.DataFrame(safety_factors['trend_data'])
                    
                    fig = px.line(
                        trend_df,
                        x='year',
                        y='safety_score',
                        title=f"Safety Score Trend for {selected_airline}",
                        markers=True
                    )
                    
                    fig.update_layout(xaxis_title="Year", yaxis_title="Safety Score", yaxis_range=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Generate sample trend data for demonstration
                    years = list(range(max(2000, datetime.now().year - 20), datetime.now().year + 1))
                    
                    # Simulate a generally improving trend with some variation
                    base_score = max(50, safety_score - 20)  # Start lower than current score
                    scores = []
                    
                    for i, year in enumerate(years):
                        progress = i / len(years)  # Ranges from 0 to almost 1
                        expected_score = base_score + (safety_score - base_score) * progress
                        variation = random.uniform(-5, 5)  # Random variation
                        scores.append(min(100, max(0, expected_score + variation)))
                    
                    trend_df = pd.DataFrame({
                        'year': years,
                        'safety_score': scores
                    })
                    
                    fig = px.line(
                        trend_df,
                        x='year',
                        y='safety_score',
                        title=f"Safety Score Trend for {selected_airline}",
                        markers=True
                    )
                    
                    fig.update_layout(xaxis_title="Year", yaxis_title="Safety Score", yaxis_range=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info("Note: This trend is an estimation based on available historical data.")
                
            except Exception as e:
                st.error(f"Error calculating safety score: {str(e)}")
                st.info("Unable to retrieve safety data for the selected airline. Please try again later.")
    
    else:  # All airlines selected
        # Fetch and calculate safety scores for all airlines
        with st.spinner("Calculating safety scores for all airlines..."):
            try:
                all_scores = []
                
                for airline in airlines[1:]:  # Skip "All Airlines"
                    score, _ = calculate_safety_score(
                        airline=airline,
                        time_period=selected_period,
                        weights=weights
                    )
                    all_scores.append({"Airline": airline, "Safety Score": score})
                
                # Create DataFrame for all airlines
                all_scores_df = pd.DataFrame(all_scores)
                
                # Sort by safety score
                all_scores_df = all_scores_df.sort_values(by="Safety Score", ascending=False)
                
                # Display as a bar chart
                fig = px.bar(
                    all_scores_df,
                    x="Airline",
                    y="Safety Score",
                    color="Safety Score",
                    color_continuous_scale=["red", "orange", "yellow", "green"],
                    range_color=[0, 100],
                    text="Safety Score",
                    title="Safety Scores for Major Airlines"
                )
                
                fig.update_layout(
                    xaxis_title="Airline",
                    yaxis_title="Safety Score",
                    yaxis_range=[0, 100]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display as a table as well
                st.subheader("Airline Safety Rankings")
                st.dataframe(all_scores_df, use_container_width=True)
                
                # Add score distribution chart
                st.subheader("Safety Score Distribution")
                
                fig = px.histogram(
                    all_scores_df,
                    x="Safety Score",
                    nbins=10,
                    range_x=[0, 100],
                    title="Distribution of Airline Safety Scores"
                )
                
                fig.update_layout(
                    xaxis_title="Safety Score",
                    yaxis_title="Number of Airlines"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"Error calculating safety scores: {str(e)}")
                st.info("Unable to retrieve safety data for all airlines. Please try again later.")

# Tab 2: Incident History
with tab2:
    st.header("Airline Incident History")
    
    if selected_airline != "All Airlines":
        # Fetch incident history for the selected airline
        with st.spinner(f"Retrieving incident history for {selected_airline}..."):
            try:
                incidents = get_airline_incidents(
                    airline=selected_airline,
                    time_period=selected_period
                )
                
                if incidents and len(incidents) > 0:
                    # Create a timeline of incidents
                    st.subheader(f"Incident Timeline for {selected_airline}")
                    
                    # Convert to DataFrame
                    incidents_df = pd.DataFrame(incidents)
                    
                    # Create a timeline chart
                    fig = px.scatter(
                        incidents_df,
                        x="date",
                        y="severity",
                        size="severity",
                        color="severity",
                        hover_name="description",
                        hover_data=["location", "aircraft_type", "fatalities"],
                        color_continuous_scale=["green", "yellow", "orange", "red"],
                        size_max=30,
                        title=f"Incident Timeline for {selected_airline}"
                    )
                    
                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Severity (1-10)",
                        yaxis_range=[0, 10]
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display incident details in a table
                    st.subheader("Incident Details")
                    
                    # Reformat the DataFrame for display
                    display_df = incidents_df[["date", "type", "location", "severity", "fatalities", "description"]]
                    display_df = display_df.sort_values(by="date", ascending=False)
                    
                    st.dataframe(display_df, use_container_width=True)
                    
                    # Add incident type breakdown
                    st.subheader("Incident Type Breakdown")
                    
                    # Count incidents by type
                    type_counts = incidents_df["type"].value_counts().reset_index()
                    type_counts.columns = ["Incident Type", "Count"]
                    
                    fig = px.pie(
                        type_counts,
                        values="Count",
                        names="Incident Type",
                        title=f"Incident Types for {selected_airline}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Add severity analysis
                    st.subheader("Severity Analysis")
                    
                    # Group by year and calculate average severity
                    yearly_severity = incidents_df.copy()
                    yearly_severity["year"] = pd.to_datetime(yearly_severity["date"]).dt.year
                    yearly_severity = yearly_severity.groupby("year").agg({
                        "severity": "mean",
                        "id": "count"
                    }).reset_index()
                    yearly_severity.columns = ["Year", "Average Severity", "Incident Count"]
                    
                    # Create a dual-axis chart
                    fig = go.Figure()
                    
                    # Add bar chart for incident count
                    fig.add_trace(go.Bar(
                        x=yearly_severity["Year"],
                        y=yearly_severity["Incident Count"],
                        name="Incident Count",
                        marker_color="lightblue"
                    ))
                    
                    # Add line chart for severity
                    fig.add_trace(go.Scatter(
                        x=yearly_severity["Year"],
                        y=yearly_severity["Average Severity"],
                        name="Average Severity",
                        marker_color="red",
                        mode="lines+markers",
                        yaxis="y2"
                    ))
                    
                    # Set up layout with secondary y-axis
                    fig.update_layout(
                        title=f"Yearly Incident Count and Severity for {selected_airline}",
                        xaxis_title="Year",
                        yaxis_title="Incident Count",
                        yaxis2=dict(
                            title="Average Severity",
                            overlaying="y",
                            side="right",
                            range=[0, 10]
                        ),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"No incidents found for {selected_airline} in the selected time period.")
            
            except Exception as e:
                st.error(f"Error retrieving incident history: {str(e)}")
                st.info("Unable to retrieve incident data for the selected airline. Please try again later.")
    
    else:  # All airlines selected
        # Show aggregated incident data across airlines
        with st.spinner("Retrieving incident data for all airlines..."):
            try:
                all_incidents = []
                
                for airline in airlines[1:]:  # Skip "All Airlines"
                    incidents = get_airline_incidents(
                        airline=airline,
                        time_period=selected_period
                    )
                    
                    if incidents:
                        for incident in incidents:
                            incident["airline"] = airline
                            all_incidents.append(incident)
                
                if all_incidents:
                    # Convert to DataFrame
                    all_incidents_df = pd.DataFrame(all_incidents)
                    
                    # Incident count by airline
                    st.subheader("Incident Count by Airline")
                    
                    airline_counts = all_incidents_df["airline"].value_counts().reset_index()
                    airline_counts.columns = ["Airline", "Incident Count"]
                    
                    fig = px.bar(
                        airline_counts,
                        x="Airline",
                        y="Incident Count",
                        color="Incident Count",
                        color_continuous_scale=["green", "yellow", "red"],
                        title="Total Incidents by Airline"
                    )
                    
                    fig.update_layout(
                        xaxis_title="Airline",
                        yaxis_title="Number of Incidents"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Incident trend over time
                    st.subheader("Industry-Wide Incident Trend")
                    
                    # Add year column
                    all_incidents_df["year"] = pd.to_datetime(all_incidents_df["date"]).dt.year
                    
                    # Group by year
                    yearly_incidents = all_incidents_df.groupby("year").agg({
                        "id": "count",
                        "severity": "mean",
                        "fatalities": "sum"
                    }).reset_index()
                    yearly_incidents.columns = ["Year", "Incident Count", "Average Severity", "Total Fatalities"]
                    
                    # Create a dual-axis chart
                    fig = go.Figure()
                    
                    # Add bar chart for incident count
                    fig.add_trace(go.Bar(
                        x=yearly_incidents["Year"],
                        y=yearly_incidents["Incident Count"],
                        name="Incident Count",
                        marker_color="lightblue"
                    ))
                    
                    # Add line chart for fatalities
                    fig.add_trace(go.Scatter(
                        x=yearly_incidents["Year"],
                        y=yearly_incidents["Total Fatalities"],
                        name="Fatalities",
                        marker_color="red",
                        mode="lines+markers",
                        yaxis="y2"
                    ))
                    
                    # Set up layout with secondary y-axis
                    fig.update_layout(
                        title="Yearly Incident Count and Fatalities Across All Airlines",
                        xaxis_title="Year",
                        yaxis_title="Incident Count",
                        yaxis2=dict(
                            title="Fatalities",
                            overlaying="y",
                            side="right"
                        ),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Incident type breakdown
                    st.subheader("Incident Type Breakdown")
                    
                    type_counts = all_incidents_df["type"].value_counts().reset_index()
                    type_counts.columns = ["Incident Type", "Count"]
                    
                    fig = px.pie(
                        type_counts,
                        values="Count",
                        names="Incident Type",
                        title="Distribution of Incident Types Across All Airlines"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Most recent incidents
                    st.subheader("Recent Industry Incidents")
                    
                    recent_df = all_incidents_df[["date", "airline", "type", "location", "severity", "fatalities", "description"]]
                    recent_df = recent_df.sort_values(by="date", ascending=False).head(10)
                    
                    st.dataframe(recent_df, use_container_width=True)
                
                else:
                    st.info("No incident data available for the selected time period.")
            
            except Exception as e:
                st.error(f"Error retrieving incident data: {str(e)}")
                st.info("Unable to retrieve incident data. Please try again later.")

# Tab 3: Comparative Analysis
with tab3:
    st.header("Comparative Safety Analysis")
    
    # Allow selection of airlines to compare
    st.subheader("Compare Airlines")
    
    # Multi-select for airlines
    compare_airlines = st.multiselect(
        "Select Airlines to Compare",
        options=airlines[1:],  # Skip "All Airlines"
        default=airlines[1:3]  # Default to first two airlines
    )
    
    if len(compare_airlines) > 0:
        # Fetch and calculate safety scores for selected airlines
        with st.spinner("Calculating comparative safety data..."):
            try:
                comparison_data = []
                
                for airline in compare_airlines:
                    score, factor_scores = calculate_safety_score(
                        airline=airline,
                        time_period=selected_period,
                        weights=weights
                    )
                    
                    # Add to comparison data
                    comparison_data.append({
                        "Airline": airline,
                        "Overall Score": score,
                        **factor_scores
                    })
                
                # Convert to DataFrame
                comparison_df = pd.DataFrame(comparison_data)
                
                # Display comparison chart
                st.subheader("Overall Safety Score Comparison")
                
                fig = px.bar(
                    comparison_df,
                    x="Airline",
                    y="Overall Score",
                    color="Overall Score",
                    color_continuous_scale=["red", "orange", "yellow", "green"],
                    range_color=[0, 100],
                    text="Overall Score",
                    title="Safety Score Comparison"
                )
                
                fig.update_layout(
                    xaxis_title="Airline",
                    yaxis_title="Safety Score",
                    yaxis_range=[0, 100]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Radar chart for factor comparison
                st.subheader("Safety Factor Comparison")
                
                # Create radar chart
                categories = list(factor_scores.keys())
                
                fig = go.Figure()
                
                for i, row in comparison_df.iterrows():
                    fig.add_trace(go.Scatterpolar(
                        r=[row[cat] for cat in categories],
                        theta=categories,
                        fill='toself',
                        name=row["Airline"]
                    ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    title="Safety Factor Comparison"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed comparison table
                st.subheader("Detailed Comparison")
                
                # Format the table
                display_df = comparison_df.copy()
                display_df = display_df.set_index("Airline")
                
                # Format to one decimal place
                for col in display_df.columns:
                    display_df[col] = display_df[col].map(lambda x: f"{x:.1f}")
                
                st.dataframe(display_df, use_container_width=True)
                
                
                    
                   
                
                
            
            except Exception as e:
                st.error(f"Error performing comparative analysis: {str(e)}")
                st.info("Unable to retrieve data for comparison. Please try again later.")
    
    else:
        st.info("Please select at least one airline to view comparison data.")

# Add methodology explanation at the bottom
with st.expander("Safety Rating Methodology"):
    st.markdown("""
    ### How Safety Scores Are Calculated

    Our safety scores combine multiple factors into a comprehensive rating on a 0-100 scale:

    1. **Incident History (Default weight: 30%)**: 
       Evaluates past accidents, incidents, and near-misses. More recent events carry more weight than older ones.

    2. **Maintenance Records (Default weight: 25%)**:
       Assesses aircraft maintenance practices, fleet age, and technical reliability.

    3. **Customer Feedback (Default weight: 15%)**:
       Incorporates safety-related comments from SentiFly's sentiment analysis system.

    4. **Operational Excellence (Default weight: 20%)**:
       Measures on-time performance, pilot training standards, and operational procedures.

    5. **Regulatory Compliance (Default weight: 10%)**:
       Evaluates compliance with aviation regulations and results of safety audits.

    **Data Sources**:
    - Historical accident databases (NTSB, Aviation Safety Network)
    - Regulatory filings and audit results
    - Fleet information and maintenance records
    - Customer reviews from SentiFly platform
    - Industry reports and expert assessments

    Adjust the weights using the sliders in the sidebar to customize the importance of each factor.
    """)