import streamlit as st

def show_onetime_page():
    st.markdown("<h2>One-Time Investment</h2>", unsafe_allow_html=True)
    st.write("Here you can make a one-time crypto investment.")

    amount = st.number_input("Enter Amount in ₹", min_value=500)
    crypto = st.selectbox("Select Cryptocurrency", ["Bitcoin", "Ethereum", "Solana"])

    if st.button("Invest"):
        st.success(f"Invested ₹{amount} in {crypto} (One-Time).")
