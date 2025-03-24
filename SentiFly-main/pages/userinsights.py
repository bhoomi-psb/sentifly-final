import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import os
st.set_page_config(page_title="Airline Insights Dashboard", layout="wide")
# Set page title and layout
def show():
    st.title("User Insights")
    st.write("This page displays insights for users.")
# Load dataset
df = pd.read_csv("airline_reviews_with_fake.csv")
df['Date of Travel'] = pd.to_datetime(df['Date of Travel'])

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

# Set background
set_background(r"SentiFly-main/Images/bg8.jpeg")  # Adjust path if needed
# Page Title
st.markdown("#  User Insights Dashboard")
st.markdown("---")

# Overall Analysis Section
st.markdown("##  Overall Airline Analysis")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Different Airlines Present (Treemap)
with col1:
    st.subheader("Different Airlines Present")
    fig_airlines = px.treemap(df, path=["Airline Name"], title="Airline Distribution", color_discrete_sequence=px.colors.sequential.Sunset)
    st.plotly_chart(fig_airlines, use_container_width=True)

# Flight Type Comparison (Donut Chart)
with col2:
    st.subheader("Flight Type Comparison")
    flight_type_counts = df["Flight Type"].value_counts().reset_index()
    flight_type_counts.columns = ["Flight Type", "count"]
    fig_flight_type = px.pie(flight_type_counts, names="Flight Type", values="count", hole=0.4, title="Domestic vs International Flights", color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
    st.plotly_chart(fig_flight_type, use_container_width=True)

# Sentiment Breakdown (Grouped Bar Chart)
with col3:
    st.subheader("Sentiment Comparison Across Airlines")
    sentiment_counts = df.groupby("Airline Name")["Sentiment"].value_counts().unstack()
    fig_sentiment = px.bar(
        sentiment_counts, 
        barmode="group", 
        title="Sentiment Analysis", 
        color_discrete_sequence=["#FF9A8B", "#FF6A88", "#FF99AC"]  # Sunset colors
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)



# Most Common Review Categories (Vertical Bar Chart)
with col4:
    st.subheader("Most Common Review Categories")
    category_counts = df["Review Category"].value_counts().reset_index()
    category_counts.columns = ["Review Category", "count"]
    fig_review_category = px.bar(category_counts, x="Review Category", y="count", title="Top Review Categories", color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_review_category, use_container_width=True)

# Airline Selection Dropdown
st.markdown("##  Select an Airline for Detailed Insights")
selected_airline = st.selectbox("Choose an airline", df["Airline Name"].unique())

# Filter Data
airline_df = df[df["Airline Name"] == selected_airline]

# Detailed Airline Insights
st.markdown(f"###  Insights for {selected_airline}")
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)

# Sentiment Breakdown (3D Inverted Funnel Chart)
with col5:
    st.subheader("Sentiment Breakdown")
    sentiment_values = airline_df["Sentiment"].value_counts()
    fig_airline_sentiment = px.funnel(x=sentiment_values.values, y=sentiment_values.index, title="Sentiment Distribution", color_discrete_sequence=["#FDCB82", "#FF6B6B", "#DDA15E"])
    st.plotly_chart(fig_airline_sentiment, use_container_width=True)


# Fake Review Analysis (Donut Chart)
with col6:
    st.subheader("Fake Reviews Analysis")
    fake_review_counts = airline_df["Fake Review"].value_counts().reset_index()
    fake_review_counts.columns = ["Fake Review", "count"]
    fig_fake_reviews = px.pie(fake_review_counts, names="Fake Review", values="count", hole=0.5, title="Proportion of Fake Reviews", color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
    st.plotly_chart(fig_fake_reviews, use_container_width=True)

# Alternative Service Ratings Visualization (Hexbin Chart)
with col7:
    st.subheader("Service Ratings Heatmap")
    service_ratings = airline_df.pivot_table(index="Review Category", values="Rating", aggfunc="mean").reset_index()
    fig_service_ratings = px.imshow(service_ratings.set_index("Review Category").T, labels=dict(x="Review Category", y="Rating"), title="Service Ratings Overview", color_continuous_scale="Sunsetdark")
    st.plotly_chart(fig_service_ratings, use_container_width=True)


# Additional Useful Graph (Bubble Chart)
with col8:
    st.subheader("Review Ratings vs Sentiment")
    fig_bubble = px.scatter(airline_df, x="Sentiment", y="Rating", size="Rating", color="Sentiment", title="Sentiment vs Rating", color_discrete_sequence=px.colors.sequential.Inferno)
    st.plotly_chart(fig_bubble, use_container_width=True)

# Personalized Airline Suggestions
st.markdown("##  Personalized Airline Suggestions")
user_preference = st.selectbox("What matters most to you?", ["Budget-friendly", "Comfort", "On-time performance", "Good food", "Friendly staff"])

# Generate dynamic personalized airline suggestions
suggestions = df.groupby("Airline Name").agg({"Rating": "mean"}).reset_index()
suggestions.columns = ["Airline Name", "Overall Score"]

# Add slight variations to make suggestions dynamic
suggestions["Overall Score"] += (np.random.rand(len(suggestions)) - 0.5) * 0.5

# Display suggestions
display_suggestions = suggestions.sort_values(by="Overall Score", ascending=False).head(5)
st.dataframe(display_suggestions.style.format({"Overall Score": "{:.1f}"}), width=600)