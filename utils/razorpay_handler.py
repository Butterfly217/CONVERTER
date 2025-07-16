import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

if not RAZORPAY_KEY or not RAZORPAY_SECRET:
    raise EnvironmentError("Missing Razorpay credentials")

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

def create_payment_order(amount_inr):
    try:
        if amount_inr > 500000:
            raise ValueError("Amount exceeds Razorpay test limit (₹5,00,000)")
            
        order = client.order.create({
            "amount": int(amount_inr * 100),
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "platform": "eCapital Investments"
            }
        })
        order["public_key"] = RAZORPAY_KEY
        return order
    except Exception as e:
        st.error(f"Payment error: {str(e)}")
        return None

def verify_payment(payment_id, order_id, signature):
    try:
        return client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
    except Exception as e:
        print(f"Verification failed: {str(e)}")
        return False