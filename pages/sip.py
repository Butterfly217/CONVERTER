import streamlit as st

def show_sip_page():
    st.markdown("<h2>SIP Plans</h2>", unsafe_allow_html=True)
    st.write("Set up a Systematic Investment Plan (SIP) for crypto.")

    sip_amount = st.number_input("Monthly SIP Amount in ₹", min_value=500)
    crypto = st.selectbox("Select Cryptocurrency", ["Bitcoin", "Ethereum", "Solana"])
    months = st.slider("Select duration (months)", 1, 36)

    if st.button("Start SIP"):
        st.success(f"SIP of ₹{sip_amount}/month in {crypto} started for {months} months.")
