import streamlit as st
import smtplib
from email.mime.text import MIMEText
from auth.auth_service import login_user, register_user

def send_registration_email(user_email):
    """Sends a welcome email upon successful registration."""
    try:
        sender_email = st.secrets["EMAIL_USER"]
        password = st.secrets["EMAIL_PASSWORD"]
        
        msg = MIMEText(f"Welcome to CryptoPort AI! Your account ({user_email}) has been successfully created.")
        msg['Subject'] = "🚀 Welcome to CryptoPort AI"
        msg['From'] = f"CryptoPort Team <{sender_email}>"
        msg['To'] = user_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, user_email, msg.as_string())
        return True
    except Exception as e:
        st.warning(f"Note: Could not send welcome email. ({str(e)})")
        return False

def login_ui():
    # Modern Glass-morphism CSS
    st.markdown("""
        <style>
        .auth-container { background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); }
        .stButton>button { width: 100%; border-radius: 8px; height: 3em; transition: 0.3s; }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Toggle between Login and Register
        mode = st.radio("Select Action", ["Login", "Create Account"], horizontal=True, label_visibility="collapsed")
        
        st.title("🚀 CryptoPort AI" if mode == "Login" else "📝 Join CryptoPort")
        
        email = st.text_input("Email Address", placeholder="name@example.com")
        password = st.text_input("Password", type="password")

        if mode == "Login":
            if st.button("🚀 Login Now", type="primary"):
                result = login_user(email, password)
                if result["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.rerun()
                else:
                    st.error(result["msg"])
        
        else: # Register Mode
            confirm_pw = st.text_input("Confirm Password", type="password")
            if st.button("✨ Create My Account", type="primary"):
                if password != confirm_pw:
                    st.error("Passwords do not match!")
                else:
                    result = register_user(email, password)
                    if result["success"]:
                        st.success("Account created successfully!")
                        send_registration_email(email) # Trigger the email
                        st.info("A welcome email has been sent to your inbox.")
                        time.sleep(2)
                        st.session_state.mode = "login"
                        st.rerun()
                    else:
                        st.error(result["msg"])
        
        st.markdown('</div>', unsafe_allow_html=True)
