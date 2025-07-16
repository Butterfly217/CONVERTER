import streamlit as st

def authenticate_user():
    st.title("🔒 Login to Your Account")
    
    with st.form("auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            # Simple demo authentication
            if email and password:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Please enter credentials")