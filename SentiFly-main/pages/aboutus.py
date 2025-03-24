import streamlit as st
import base64
import os

st.set_page_config(page_title="about Us", layout="wide")
# Set page title and layout (Must be first command)
def show():
    st.title("About Us")
    st.write("This page displays the details about us.")

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


# Set background with corrected image path
set_background(r"SentiFly-main/Images/bg8.jpeg")

# Apply custom styles (CSS)
custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
            background-image: url('Images/bg8.jpeg');
            background-size: cover;
            background-position: center;
        }

        .container {
            max-width: 900px;
            margin: 100px auto 50px auto;
            background: rgb(255, 235, 235);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
            text-align: center;
            animation: fadeIn 1.5s ease-in-out;
        }

        h1, h2 {
            color: #a70c0c;
        }

        p {
            font-size: 30px;
            line-height: 1.6;
        }

        .footer {
            margin-top: 30px;
            font-size: 14px;
            color: #ccc;
            text-align: center;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        ul.custom-list li {
        font-size: 25px;
        transition: all 0.3s ease-in-out;
    }

    ul.custom-list li:hover {
        color: #a70c0c;
        font-weight: bold;
        transform: translateX(10px);
    }
    </style>
"""

# Inject the CSS styles
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1>Welcome to SentiFly</h1>", unsafe_allow_html=True)
st.markdown(
    '<p style="font-size: 25px;">SentiFly is an innovative platform designed to revolutionize the airline customer experience by analyzing passenger feedback. Our goal is to bridge the gap between airlines and passengers, ensuring better service quality, enhanced safety, and an overall smoother journey.</p>',
    unsafe_allow_html=True,
)

st.markdown("<h2>Our Mission</h2>", unsafe_allow_html=True)
st.markdown(
    '<p style="font-size: 25px;">At SentiFly, we are committed to helping airlines gain meaningful insights from passenger reviews. By identifying trends in customer feedback, we enable airlines to address concerns proactively, improve customer satisfaction, and ensure a seamless flying experience for all.</p>',
    unsafe_allow_html=True,
)

st.markdown("<h2>Our Vision</h2>", unsafe_allow_html=True)
st.markdown(
    '<p style="font-size: 25px;">We envision a world where every airline values customer feedback as a key driver of growth and excellence. Our platform aspires to create a more transparent and responsive aviation industry, where passenger experiences shape the future of air travel.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <ul class="custom-list" style="text-align: left; font-size: 25px; display: inline-block; list-style: none;">
        <li>✔ Gain real-time insights into passenger sentiment</li>
        <li>✔ Enhance customer service and improve operational efficiency</li>
        <li>✔ Identify and respond to emergency situations swiftly</li>
        <li>✔ Improve airline reputation and customer loyalty</li>
        <li>✔ Detect and filter out fake reviews to ensure credibility</li>
        <li>✔ Enable data-driven decision-making for airlines</li>
        <li>✔ Offer AI-powered analytics for in-depth review categorization</li>
        <li>✔ Provide airlines with personalized recommendations for service improvements</li>
        <li>✔ Support passengers with a user-friendly interface to share their experiences easily</li>
        <li>✔ Allow bulk review uploads for comprehensive airline performance analysis</li>
    </ul>
    """,
    unsafe_allow_html=True,
)


st.markdown("<h2>How SentiFly Works</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <p style="font-size: 25px;">AI-Powered Sentiment Analysis: Our advanced algorithms classify passenger feedback into categories like Positive, Negative, and Emergency, helping airlines focus on areas that matter most.</p>
    
    <p style="font-size: 25px;">Interactive Dashboards & Reports: Get detailed statistics and graphical insights on passenger sentiment trends, service satisfaction levels, and operational bottlenecks.</p>

    <p style="font-size: 25px;">Emergency Alert System: Critical or urgent complaints (such as safety concerns) are immediately flagged to ensure swift airline response.</p>

    <p style="font-size: 25px;">Fake Review Detection: SentiFly identifies suspicious reviews and prevents fake feedback from influencing airline decisions.</p>

    <p style="font-size: 25px;">Risk Prediction Model: Utilizing historical accident data, maintenance records, operational insights, and sentiment analysis, SentiFly forecasts potential safety risks across major Indian airlines.</p>
    
    <p style="font-size: 25px;">Safety Ratings: Airlines are scored on a 0-100 scale based on incident history, maintenance practices, customer sentiment, operational excellence, and regulatory compliance.</p>
    
    <p style="font-size: 25px;">Customizable Metrics: Adjust weightings for each factor to personalize airline safety evaluations.</p>
    
    <p style="font-size: 25px;">Ready to take flight with SentiFly? Let’s make air travel safer and better, together!</p>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h2 style="text-align: right;">- Team SentiFly</h2>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Close the container
