import streamlit as st
import datetime
import sqlite3
import base64
import os
from pages.models import SentimentAnalyzer  # Import the sentiment model

# Database connection
conn = sqlite3.connect("airline_reviews.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists (Removed 'ticket' column)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        airline TEXT,
        flight_type TEXT,
        seat_class TEXT,
        date_of_travel TEXT,
        purpose_of_travel TEXT,
        source TEXT,
        destination TEXT,
        booking_method TEXT,
        frequent_flyer TEXT,
        check_in_rating TEXT,
        seat_comfort TEXT,
        crew_service TEXT,
        food_quality TEXT,
        punctuality TEXT,
        review_comment TEXT,
        improvement_needed TEXT,
        recommend TEXT,
        sentiment TEXT,
        fake_review TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Set page title
st.set_page_config(page_title="Airline Review Submission", layout="wide")

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

set_background("SentiFly-main/Images/bg8.jpeg")

# Custom form styling
st.markdown("""
    <style>
        div[data-testid="stForm"] {
            background-color: #f7f9fc;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            width: 700px;
            margin: auto;
        }
        div[data-testid="stFormSubmitButton"] button {
            background-color: #b22222 !important;
            color: white !important;
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown("<h2 style='text-align: center;'>✈ Airline Review</h2>", unsafe_allow_html=True)

# Review Form
with st.form("review_form"):
    with st.expander("📝 Basic Information"):
        name = st.text_input("Name", "")
        email = st.text_input("Email", "")
        airline = st.selectbox("Select Airline", ["Vistara", "IndiGo", "Air India", "AirAsia India", "SpiceJet", "GoAir"])
        
    with st.expander("✈ Flight Details"):
        flight_type = st.selectbox("Type of Flight", ["Domestic", "International"])
        seat_class = st.selectbox("Seat Class", ["Economy", "Premium Economy", "Business", "First Class"])
        date_of_travel = st.date_input("Date of Travel", max_value=datetime.date.today())
        purpose_of_travel = st.selectbox("Purpose of Travel", ["Business", "Leisure", "Family Visit", "Other"])
        source = st.text_input("Source (City/Airport)", "")
        destination = st.text_input("Destination (City/Airport)", "")

    with st.expander("🎟 Booking & Ticket Upload"):
        booking_method = st.selectbox("How did you book your ticket?", ["Website", "Mobile App", "Travel Agent", "Airport Counter"])
        frequent_flyer = st.radio("Are you a frequent flyer?", ["Yes", "No", "Occasionally"])
        uploaded_ticket = st.file_uploader("Upload Ticket (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])
        if uploaded_ticket:
            st.info("✅ Ticket uploaded successfully. (Not stored in database)")

    with st.expander("🌟 Rate Your Experience"):
        check_in_rating = st.radio("Check-in & Boarding", ["Poor", "Fair", "Good", "Very Good", "Excellent"], index=2)
        seat_comfort = st.radio("Seat Comfort", ["Poor", "Fair", "Good", "Very Good", "Excellent"], index=2)
        crew_service = st.radio("Cabin Crew Service", ["Poor", "Fair", "Good", "Very Good", "Excellent"], index=2)
        food_quality = st.radio("Food & Beverage", ["Poor", "Fair", "Good", "Very Good", "Excellent"], index=2)
        punctuality = st.radio("Punctuality", ["Poor", "Fair", "Good", "Very Good", "Excellent"], index=2)

    with st.expander("💬 Share Your Feedback"):
        review_comment = st.text_area("Review Comment", "", max_chars=5000)
        improvement_needed = st.text_area("What could have been better?", "")

    with st.expander("👍 Would You Recommend?"):
        recommend = st.radio("Would you recommend this airline?", ["Yes", "No", "Maybe"])

    submitted = st.form_submit_button("Submit Review")

if submitted:
    analyzer = SentimentAnalyzer()
    sentiment_result = analyzer.analyze(review_comment)
    sentiment = sentiment_result["sentiment"]
    fake_review = analyzer.detect_fake_review(review_comment)

    # Insert data into database (Removed ticket_data)
    cursor.execute('''
        INSERT INTO reviews (
            name, email, airline, flight_type, seat_class, date_of_travel, 
            purpose_of_travel, source, destination, booking_method, frequent_flyer, 
            check_in_rating, seat_comfort, crew_service, food_quality, punctuality, 
            review_comment, improvement_needed, recommend, sentiment, fake_review
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name, email, airline, flight_type, seat_class, str(date_of_travel), 
        purpose_of_travel, source, destination, booking_method, frequent_flyer, 
        check_in_rating, seat_comfort, crew_service, food_quality, punctuality, 
        review_comment, improvement_needed, recommend, sentiment, fake_review
    ))

    conn.commit()

    # Emergency Alert
    if sentiment == "Emergency":
        st.warning("🚨 *Emergency Alert:* This review contains urgent matters!")

    st.success(f"✅ Sentiment: *{sentiment}* | Fake Review: *{fake_review}*")

conn.close()
