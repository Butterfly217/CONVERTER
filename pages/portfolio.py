import streamlit as st

def show_portfolio_page():
    st.markdown("<h2>My Portfolio</h2>", unsafe_allow_html=True)

    # Dummy data
    portfolio = {
        "Bitcoin": {"amount": "₹5,000", "tokens": 0.0015},
        "Ethereum": {"amount": "₹3,000", "tokens": 0.02}
    }

    for crypto, data in portfolio.items():
        st.subheader(crypto)
        st.write(f"Invested: {data['amount']}")
        st.write(f"Tokens Owned: {data['tokens']}")
