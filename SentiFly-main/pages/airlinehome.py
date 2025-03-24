import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import random
from datetime import datetime, timedelta
st.set_page_config(page_title="Airline Insights Dashboard", layout="wide")
# Function to set background image
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

# Set background image
set_background(r"SentiFly-main/Images/bg8.jpeg")

# Set CSS
def set_css():
    custom_css = """
        <style>
            .container {background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 90%; max-width: 1100px; margin: auto;}
            .summary-box {background: #f9f9f9e3; padding: 15px; border-radius: 8px; box-shadow: 0px 2px 5px rgba(2, 2, 2, 0.2); text-align: left; margin-top: 20px;}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Set page title
st.markdown("<h2 style='text-align: center;'>Upload Airline Reviews File</h2>", unsafe_allow_html=True)
set_css()

# File Upload
st.markdown('<p style="font-size: 20px; font-weight: bold;">📂 Upload a CSV file</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Rename 'Review Text' to 'Review' if it exists
    if "Review Text" in df.columns:
        df.rename(columns={"Review Text": "Review"}, inplace=True)
    
    # Check required columns
    required_columns = {"Sentiment", "Is Fake", "Review"}
    missing_cols = required_columns - set(df.columns)
    if missing_cols:
        st.error(f"CSV must contain {required_columns} columns. Missing: {missing_cols}")
    else:
        # Summary
        total_reviews = len(df)
        fake_review_count = len(df[df["Is Fake"].str.lower() == "yes"])
        sentiment_counts = df["Sentiment"].value_counts().to_dict()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reviews", total_reviews)
        col2.metric("Fake Reviews", fake_review_count)
        col3.metric("Authentic Reviews", total_reviews - fake_review_count)
        
        # Option to download specific sentiment data
        selected_sentiment = st.selectbox("Select Sentiment to Download", list(sentiment_counts.keys()))
        filtered_df = df[df["Sentiment"] == selected_sentiment]
        sentiment_csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(label=f"📥 Download {selected_sentiment} Reviews", data=sentiment_csv, file_name=f"{selected_sentiment}_reviews.csv", mime="text/csv")
        
        # Visualizations
        st.markdown("<h2 style='text-align: center;'>Visual Insights</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Distribution")
            sentiment_fig = px.bar(x=list(sentiment_counts.keys()), y=list(sentiment_counts.values()), 
                                   labels={"x": "Sentiment", "y": "Count"},
                                   title="Sentiment Breakdown",
                                   color_discrete_sequence=["#FF5E4D", "#FF8C00", "#FFD700"])
            st.plotly_chart(sentiment_fig, use_container_width=True)
        
        with col2:
            st.subheader("Fake Review Analysis")
            fake_fig = px.pie(df, names="Is Fake", title="Fake vs Real Reviews", color_discrete_sequence=["#FF5E4D", "#FFD700"])
            st.plotly_chart(fake_fig, use_container_width=True)
        
        # Additional Graphs
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Review Sentiment Over Time")
            if "Review Date" in df.columns:
                df["Review Date"] = pd.to_datetime(df["Review Date"])
            else:
                df["Review Date"] = [datetime.today() - timedelta(days=random.randint(0, 365)) for _ in range(len(df))]
            time_fig = px.line(df.groupby("Review Date")["Sentiment"].value_counts().unstack().fillna(0), title="Sentiment Trends Over Time")
            st.plotly_chart(time_fig, use_container_width=True)
        
        with col4:
            st.subheader("Review Length Distribution")
            df["Review Length"] = df["Review"].astype(str).apply(len)
            length_fig = px.histogram(df, x="Review Length", nbins=30, title="Review Length Distribution", color_discrete_sequence=["#FF8C00"])
            st.plotly_chart(length_fig, use_container_width=True)
        
        # Summary Insights
        st.subheader("Key Insights")
        st.write(f"✅ **Most Frequent Sentiment:** {max(sentiment_counts, key=sentiment_counts.get)}")
        st.write(f"✅ **Fake Review Percentage:** {round((fake_review_count / total_reviews) * 100, 2)}%")
        
        # Report Download Option
        st.subheader("Download Full Report")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download CSV Report", data=csv_data, file_name="airline_reviews_report.csv", mime="text/csv")
