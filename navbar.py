import streamlit as st
import base64
import os

def show():
    """Render the navigation bar for users."""

    # ✅ Load and encode the logo image
    logo_path = "Images/logo.png"  # Ensure logo is in the correct folder
    try:
        with open(logo_path, "rb") as img_file:
            encoded_logo = base64.b64encode(img_file.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{encoded_logo}" alt="Logo" style="height: 40px;">'
    except FileNotFoundError:
        st.warning("⚠ Logo image not found at: Images/logo.png")
        logo_html = '<p style="font-size:16px; color:red;">[Logo Not Found]</p>'

    # ✅ Apply custom CSS styles for navbar
    custom_css = """
        <style>
            .navbar {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background: #f8d7da;  /* Improved color */
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 20px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            }
            .navbar-buttons {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            .nav-btn {
                background: none;
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: black;
                cursor: pointer;
                transition: color 0.3s ease-in-out;
            }
            .nav-btn:hover {
                color: #ea5353;
            }
        </style>
    """

    # ✅ Inject CSS styles
    st.markdown(custom_css, unsafe_allow_html=True)

    # ✅ Render Navbar
    st.markdown(f"""
        <div class="navbar">
            <div>{logo_html}</div>
            <div class="navbar-buttons">
    """, unsafe_allow_html=True)

    # ✅ Page Navigation Buttons
    pages = {
        "Home": "pages/userhome.py",
        "Insights": "pages/userinsights.py",
        "Flight Risk & Safety": "pages/flight_risk_safety.py",
        "About Us": "pages/aboutus.py",
        "Contact Us": "pages/contactus.py",
        "Sign In": "pages/signin.py",
    }

    # ✅ Button layout
    cols = st.columns(len(pages))  # Auto-align buttons in a row

    for i, (label, page) in enumerate(pages.items()):
        cols[i].page_link(page, label=label)  # ✅ Uses page_link() instead of switch_page()

    st.markdown("</div></div>", unsafe_allow_html=True)

# ✅ Call show() only if this file is run directly
if __name__ == "__main__":
    show()
