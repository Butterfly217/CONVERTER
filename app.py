import streamlit as st
import requests
from utils.web3_handler import connect_wallet

# --- Page Config ---
st.set_page_config(page_title="eCapital Trading App", layout="wide")

# --- Load Styles ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Page Navigation State ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- HOME PAGE ---
if st.session_state.page == 'home':
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<div class="big-title">The world\'s fastest Trading Platform App.</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">A faster, cleaner and smarter way to trade. Seize your opportunities with a cutting-edge platform built around your needs.</div>', unsafe_allow_html=True)
        
        if st.button("Get Started", key="start_btn"):
            st.session_state.page = 'converter'
            st.rerun()

    with col2:
        st.image("wallet_mockup.png", use_container_width=True)


# --- CONVERTER PAGE ---
elif st.session_state.page == 'converter':
    st.markdown("<h2 style='text-align:center;'>INR to Crypto Converter</h2>", unsafe_allow_html=True)

    inr_amount = st.number_input("Amount in INR (₹)", min_value=0.0, step=10.0, format="%.2f")
    currency = st.selectbox("Select Cryptocurrency", ["Bitcoin (BTC)", "Ethereum (ETH)"])

    crypto_ids = {"Bitcoin (BTC)": "bitcoin", "Ethereum (ETH)": "ethereum"}
    crypto_symbol = {"Bitcoin (BTC)": "BTC", "Ethereum (ETH)": "ETH"}

    # Get live rate
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_ids[currency]}&vs_currencies=inr")
        rate = response.json()[crypto_ids[currency]]['inr']
        converted = round(inr_amount / rate, 8)
    except:
        st.error("Failed to fetch conversion rate.")
        rate = 0
        converted = 0

    # Display conversion result
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='pay-box'><small>You pay</small><br><strong>₹{int(inr_amount)}</strong></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='pay-box'><small>You get</small><br><strong>{converted} {crypto_symbol[currency]}</strong></div>", unsafe_allow_html=True)

    if st.button("Proceed to Payment"):
        wallet_status = connect_wallet()
        if wallet_status:
            st.success("Wallet connected. Proceeding to payment...")
        else:
            st.error("Wallet connection failed. Ensure MetaMask is set up properly.")

    st.markdown("<p class='powered'>Payments powered by Razorpay</p>", unsafe_allow_html=True)


