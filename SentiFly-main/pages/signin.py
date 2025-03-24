import streamlit as st
import base64
import os

st.set_page_config(page_title="about Us",)
# ✅ Set page configuration (Centered layout)
def show():
    st.title("sign in page")
    st.write("This page displays sigin in options.")

# ✅ Function to set background image
def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        bg_image = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(bg_image, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Background image not found at: {image_path}")

# ✅ Set background
set_background(r"SentiFly-main/Images/singn.jpg")

# ✅ Session State for User/Airline toggle and Login/Sign-Up toggle
if "user_type" not in st.session_state:
    st.session_state["user_type"] = "User"
if "login_mode" not in st.session_state:
    st.session_state["login_mode"] = "Login"

# ✅ Toggle functions
def toggle_user_type():
    st.session_state["user_type"] = "User" if st.session_state["user_type"] == "Airline" else "Airline"

def toggle_login_mode():
    st.session_state["login_mode"] = "Login" if st.session_state["login_mode"] == "Sign Up" else "Sign Up"

# ✅ Updated Custom CSS - **Removes Extra Box**
st.markdown(
    """
    <style>
    /* Main container styling */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        width: 400px;
        margin: auto;
        padding: 20px;
        background: rgba(255, 231, 231, 0.9);  /* Light Pink */
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Remove unwanted padding from Streamlit */
    section.main div.block-container {
        padding-top: 0px;
        padding-bottom: 0px;
    }

    /* Login Form Styling */
    div[data-testid="stForm"] {
        background: rgba(255, 231, 231, 0.95);  /* Light Pink */
        padding: 25px;
        border-radius: 10px;
        border: none;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Input Fields */
    input {
        width: 100%;
        padding: 12px;
        border-radius: 6px;
        border: 1px solid rgba(255, 0, 0, 0.2);
        background: rgba(255, 230, 230, 0.4);
    }

    /* Buttons */
    div[data-testid="stFormSubmitButton"] button {
        background: #ff2f2f !important;
        color: white !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        padding: 10px;
        width: 100%;
        transition: 0.3s;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: #d90000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 🔹 User Type Toggle Button
if st.button(f"Switch to { 'Airline' if st.session_state['user_type'] == 'User' else 'User' } Login"):
    toggle_user_type()

# 🔹 Title
st.markdown(f"### {st.session_state['user_type']} {st.session_state['login_mode']}")

# 🔹 Login or Sign-Up Form
with st.form("auth_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.session_state["login_mode"] == "Sign Up":
        full_name = st.text_input("Full Name")

    submitted = st.form_submit_button(st.session_state["login_mode"])

    if submitted:
        if st.session_state["user_type"] == "User":
            st.success("✅ User Login Successful! Redirecting...")
            st.switch_page("pages/userhome.py")
        else:
            st.success("✅ Airline Login Successful! Redirecting...")
            st.switch_page("pages/airlinehome.py")

# 🔹 Toggle between Login and Sign-Up
st.markdown(
    f"Don't have an account? **[Click here to { 'Sign Up' if st.session_state['login_mode'] == 'Login' else 'Login' }]**",
    unsafe_allow_html=True,
)

if st.button(f"Switch to { 'Sign Up' if st.session_state['login_mode'] == 'Login' else 'Login' }"):
    toggle_login_mode()

st.markdown('</div>', unsafe_allow_html=True)
