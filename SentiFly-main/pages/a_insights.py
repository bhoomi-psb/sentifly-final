import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import base64
import os
st.set_page_config(page_title="Airline Insights Dashboard", layout="wide")
#  Set page title and layout
def show():
    st.title("Airlines Insights")
    st.write("This page displays insights for Airlines.")

#  Function to set background image
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

#  Set background
set_background(r"SentiFly-main/Images/bg8.jpeg")  # Adjust path if needed

#  Load dataset
df = pd.read_csv("airline_reviews_with_fake.csv")
df["Date of Travel"] = pd.to_datetime(df["Date of Travel"])
df["Month"] = df["Date of Travel"].dt.strftime("%B")  # Month names with year
df["Year"] = df["Date of Travel"].dt.year  # Extract year column

# 🎨 **Graph Styling - Light Theme Adjustments**
graph_layout = dict(
    plot_bgcolor="#f8f9fa",  # Light gray background
    paper_bgcolor="#f8f9fa",  # Light gray background for paper
    font=dict(color="black"),  # Darker text for better contrast
)

# 🔹 **Custom CSS for Dropdown Styling**
custom_css = """
    <style>
        div[data-baseweb="select"] > div {
            background-color: #f5f5f5 !important;  /* White background */
            color: #000000 !important;             /* Dark text */
            border-radius: 10px !important;        /* Rounded corners */
            border: 1px solid #ced4da !important;  /* Light border */
            padding: 8px !important;
        }

        ul[role="listbox"] {
            background-color: #ffffff !important; /* White options background */
            color: black !important;             /* Option text color */
        }

        li[role="option"]:hover {
            background-color: #f1f3f5 !important; /* Soft gray on hover */
            color: black !important;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

#  Page Title
st.markdown("# Airline Insights Dashboard")
st.markdown("i")

# ✅ Filters in one row
col_filter1, col_filter2, col_filter3 = st.columns([1, 1, 1])

# 📌 Airline Selection Dropdown
with col_filter1:
    selected_airline = st.selectbox(
        "Choose an airline", df["Airline Name"].unique(), key="airline_select"
    )

# 📌 Month Filter
# 📌 Extract Month Names in Correct Order
df["Month Name"] = df["Date of Travel"].dt.month_name()  # Extract only the month name

# ✅ Ensure Months are Ordered (January → December)
month_order = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]
month_list = sorted(df["Month Name"].unique(), key=lambda x: month_order.index(x))  # Sort in correct order

# 📌 Month Filter (Ordered List)
with col_filter2:
    selected_month = st.selectbox("Select Month", ["All"] + list(month_list), key="month_filter")

# 📌 Year Filter
with col_filter3:
    year_list = df["Year"].unique()
    selected_year = st.selectbox("Select Year", ["All"] + list(map(str, year_list)), key="year_filter")

# ✅ Filter Data
airline_df = df[df["Airline Name"] == selected_airline]
if selected_month != "All":
    airline_df = airline_df[airline_df["Month"] == selected_month]
if selected_year != "All":
    airline_df = airline_df[airline_df["Year"] == int(selected_year)]

# ✅ Detailed Airline Insights
st.markdown(f"###  Insights for {selected_airline}")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# 📊 Sentiment Breakdown
with col1:
    st.subheader(" Sentiment Breakdown")
    airline_sentiment = airline_df["Sentiment"].value_counts()
    fig_airline_sentiment = px.bar(
        airline_sentiment, x=airline_sentiment.index, y=airline_sentiment.values,
        title="Sentiment Distribution", color=airline_sentiment.index,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig_airline_sentiment.update_layout(**graph_layout)
    st.plotly_chart(fig_airline_sentiment, use_container_width=True)

# 🛑 Fake Review Analysis
with col2:
    st.subheader(" Fake Reviews Analysis")
    fake_review_counts = airline_df["Fake Review"].value_counts().reset_index()
    fake_review_counts.columns = ["Fake Review", "count"]
    fig_fake_reviews = px.pie(
        fake_review_counts, names="Fake Review", values="count", hole=0.5,
        title="Proportion of Fake Reviews", color_discrete_sequence=px.colors.sequential.Sunsetdark_r
    )
    fig_fake_reviews.update_layout(**graph_layout)
    st.plotly_chart(fig_fake_reviews, use_container_width=True)

# ⭐ Service Ratings Breakdown
with col3:
    st.subheader(" Service Ratings Breakdown")
    service_ratings = airline_df.pivot_table(index="Review Category", values="Rating", aggfunc="mean").reset_index()
    fig_service_ratings = px.bar(
        service_ratings, x="Review Category", y="Rating", title="Service Ratings Overview",
        color="Rating", color_continuous_scale="Sunset"
    )
    fig_service_ratings.update_layout(**graph_layout)
    st.plotly_chart(fig_service_ratings, use_container_width=True)

# 📈 Review Trends Over Time
with col4:
    st.subheader(" Review Trends Over Time")
    review_trends = airline_df.groupby("Month")["Rating"].mean().reset_index()
    fig_trends = px.line(
        review_trends, x="Month", y="Rating", title="Review Trends Over Time (Monthly)",
        markers=True, color_discrete_sequence=["#FF6A88"]
    )
    fig_trends.update_layout(**graph_layout)
    st.plotly_chart(fig_trends, use_container_width=True)

# 📝 Dropdown for Top Reviews per Sentiment
st.markdown("## Recent Reviews per Sentiment")
col5, col6 = st.columns([1, 3])

with col5:
    selected_sentiment = st.selectbox(
        "Select Sentiment", ["Positive", "Negative", "Emergency"], key="sentiment_select"
    )

with col6:
    top_reviews = airline_df[airline_df["Sentiment"] == selected_sentiment].head(5)[["Review Text"]]
    st.dataframe(
        top_reviews.style.set_properties(**{"text-align": "left"}),
        width=800
    )
