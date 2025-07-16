import streamlit as st
import streamlit.components.v1 as components
from utils.razorpay_handler import create_payment_order, verify_payment
from utils.web3_handler import connect_wallet
import pandas as pd
import time 




st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# --- Page Config ---
st.set_page_config(page_title="eCapital Trading App", layout="wide")

# --- Load Styles ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Home Page ---
def show_home_page():
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<div class="big-title">Smart Crypto Investing Made Simple</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Start with as little as ₹500. Build your wealth with our automated investment platform.</div>', unsafe_allow_html=True)

        if st.button("Invest Now", key="invest_btn", type="primary"):
            st.session_state.page = 'converter'
            st.rerun()

        colA, colB, colC = st.columns([1, 1, 1])
        with colA:
            if st.button("One-Time Investment"):
                st.session_state.page = "onetime"
                st.rerun()
        with colB:
            if st.button("SIP Plans"):
                st.session_state.page = "sip"
                st.rerun()
        with colC:
            if st.button("My Portfolio"):
                st.session_state.page = "dashboard"
                st.rerun()

    with col2:
        st.image("assets/wallet_mockup.png", use_container_width=True)

# --- INR to Crypto Converter ---
def show_converter_page():
    st.markdown("<h2 style='text-align:center;'>INR to Crypto Converter</h2>", unsafe_allow_html=True)

    inr_amount = st.number_input("Amount in INR (₹)", min_value=500.0, step=100.0, format="%.2f")
    currency = st.selectbox("Select Cryptocurrency", ["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)"])

    crypto_data = {
        "Bitcoin (BTC)": {"id": "bitcoin", "symbol": "BTC", "rate": 3000000},
        "Ethereum (ETH)": {"id": "ethereum", "symbol": "ETH", "rate": 200000},
        "Solana (SOL)": {"id": "solana", "symbol": "SOL", "rate": 6000}
    }

    rate = crypto_data[currency]["rate"]
    converted = round(inr_amount / rate, 8)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='pay-box'><small>You pay</small><br><strong>₹{inr_amount:,.2f}</strong></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='pay-box'><small>You get</small><br><strong>{converted} {crypto_data[currency]['symbol']}</strong></div>", unsafe_allow_html=True)

    if st.button("Proceed to Payment", type="primary"):
        handle_payment(inr_amount, currency, converted, crypto_data[currency]['symbol'])

# --- Razorpay Handler ---
def handle_payment(amount, currency, converted_amount, symbol):
    order = create_payment_order(amount)
    if order:
        st.session_state.payment_data = {
            "order_id": order['id'],
            "amount": amount,
            "currency": currency,
            "crypto_amount": converted_amount,
            "symbol": symbol
        }

        razorpay_script = f"""
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <button id="rzp-button" class="rzp-button">Pay ₹{amount}</button>
        <script>
            var options = {{
                "key": "{order['public_key']}",
                "amount": "{order['amount']}",
                "currency": "INR",
                "name": "eCapital Investments",
                "description": "Purchase {converted_amount} {symbol}",
                "order_id": "{order['id']}",
                "handler": function(response) {{
                    window.parent.postMessage({{
                        event: "payment-success",
                        payment_id: response.razorpay_payment_id,
                        order_id: response.razorpay_order_id,
                        signature: response.razorpay_signature
                    }}, "*");
                }},
                "theme": {{ "color": "#F37254" }}
            }};
            var rzp1 = new Razorpay(options);
            document.getElementById('rzp-button').onclick = function(e) {{
                rzp1.open();
                e.preventDefault();
            }};
        </script>
        """
        components.html(razorpay_script, height=300)

        payment_status = st.empty()

        if st.button("Verify Payment"):
            verified = verify_payment(
                st.session_state.payment_data["order_id"],
                st.session_state.payment_data.get("payment_id"),
                st.session_state.payment_data.get("signature")
            )
            if verified:
                st.session_state.payment_verified = True
                payment_status.success("Payment successful! Your crypto will be credited shortly.")
                time.sleep(2)
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                payment_status.error("Payment verification failed. Please try again.")

# --- My Portfolio ---
def show_dashboard_page():
    st.title("💰 My Investment Portfolio")

    cols = st.columns(3)
    with cols[0]: st.metric("Total Invested", "₹24,500", "+12.5%")
    with cols[1]: st.metric("Current Value", "₹27,560", "23.4%")
    with cols[2]: st.metric("Active SIPs", "3", "2 ongoing")

    st.subheader("Asset Allocation")
    chart_url = "https://quickchart.io/chart?c=%7B%22type%22%3A%22doughnut%22%2C%22data%22%3A%7B%22labels%22%3A%5B%22BTC%22%2C%22ETH%22%2C%22SOL%22%5D%2C%22datasets%22%3A%5B%7B%22data%22%3A%5B65%2C25%2C10%5D%2C%22backgroundColor%22%3A%5B%22%23FF6384%22%2C%22%2336A2EB%22%2C%22%23FFCE56%22%5D%7D%5D%7D%7D"
    st.image(chart_url)

    #st.image("https://quickchart.io/chart?c={type:'doughnut',data:{labels:['BTC','ETH','SOL'], datasets:[{data:[65,25,10],backgroundColor:['#FF6384','#36A2EB','#FFCE56']}]}}")

    st.subheader("Recent Transactions")
    st.table(pd.DataFrame([
        {"Date": "2023-11-20", "Type": "Buy", "Asset": "BTC", "Amount": "0.002", "Value": "₹6,000", "Status": "Completed"},
        {"Date": "2023-11-15", "Type": "SIP", "Asset": "ETH", "Amount": "0.05", "Value": "₹10,000", "Status": "Processing"},
        {"Date": "2023-11-10", "Type": "Buy", "Asset": "SOL", "Amount": "10", "Value": "₹8,500", "Status": "Completed"}
    ]))

    if st.button("Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

# --- SIP Page ---
def show_sip_page():
    st.title("🔄 Systematic Investment Plans")

    st.write("""
    Invest fixed amounts regularly to benefit from rupee-cost averaging 
    and build your crypto portfolio automatically.
    """)

    with st.form("sip_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Monthly Amount (₹)", min_value=500, step=500, value=5000)
            currency = st.selectbox("Cryptocurrency", ["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)"])
        with col2:
            start_date = st.date_input("Start Date")
            duration = st.selectbox("Duration", ["3 Months", "6 Months", "1 Year", "Indefinite"])

        submitted = st.form_submit_button("Start SIP")
        if submitted:
            st.success(f"SIP created successfully! ₹{amount} will be invested in {currency} every month starting {start_date}.")
            time.sleep(2)
            st.session_state.page = 'dashboard'
            st.rerun()

# --- One-Time Investment ---
def show_onetime_page():
    st.title("🪙 One-Time Crypto Investment")

    with st.form("onetime_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Investment Amount (₹)", min_value=500, step=100, value=1000)
            crypto = st.selectbox("Select Cryptocurrency", ["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)"])
        with col2:
            comment = st.text_area("Note (optional)")

        submitted = st.form_submit_button("Confirm Investment")
        if submitted:
            st.success(f"✅ One-time investment of ₹{amount} in {crypto} placed successfully!")
            time.sleep(2)
            st.session_state.page = 'dashboard'
            st.rerun()

# --- Session State + Navigation ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'converter':
    show_converter_page()
elif st.session_state.page == 'dashboard':
    show_dashboard_page()
elif st.session_state.page == 'sip':
    show_sip_page()
elif st.session_state.page == 'onetime':
    show_onetime_page()
