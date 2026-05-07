import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Courier Management System",
    page_icon="📦",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>
.main {
    padding-top: 10px;
}

.stButton > button {
    background-color: #0E7490;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-size: 16px;
}

.success-box {
    padding: 15px;
    background-color: #DCFCE7;
    border-radius: 10px;
    color: #166534;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.title("📦 Courier Management System")
st.subheader("राजहंस पुस्तक पेठ - Courier Entry")

# =====================================
# SESSION STATE
# =====================================
if "data" not in st.session_state:
    st.session_state.data = []

# =====================================
# FORM
# =====================================
with st.form("courier_form"):

    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name")
        mobile = st.text_input("Mobile Number")
        tracking_no = st.text_input("Tracking Number")

        courier_company = st.selectbox(
            "Courier Company",
            [
                "Shree Tirupati Courier",
                "DTDC",
                "India Post",
                "Professional",
                "Other"
            ]
        )

    with col2:
        book_name = st.text_input("Book Name")
        city = st.text_input("City")
        amount = st.text_input("Amount")
        courier_date = st.date_input("Courier Date")

    submitted = st.form_submit_button("Save Courier")

# =====================================
# SAVE DATA
# =====================================
if submitted:

    # Tracking Link
    tracking_link = (
        f"http://www.shreetirupaticourier.net/"
        f"frmDocketTrack.aspx?DocketNo={tracking_no}"
    )

    # WhatsApp Message
    whatsapp_message = f"""
नमस्कार {customer_name},

आपले पुस्तक कुरियरने पाठवण्यात आले आहे 📦

📘 पुस्तक : {book_name}
📍 शहर : {city}
📦 Courier : {courier_company}
🔢 Tracking No : {tracking_no}

Tracking Link 👇
{tracking_link}

- राजहंस पुस्तक पेठ
"""

    # WhatsApp URL Encode
    encoded_message = urllib.parse.quote(whatsapp_message)

    whatsapp_link = (
        f"https://wa.me/91{mobile}?text={encoded_message}"
    )

    # Save Row
    row = {
        "Date": str(courier_date),
        "Customer": customer_name,
        "Mobile": mobile,
        "Book": book_name,
        "City": city,
        "Amount": amount,
        "Courier": courier_company,
        "Tracking No": tracking_no,
        "Tracking Link": tracking_link
    }

    st.session_state.data.append(row)

    # Success Message
    st.markdown(
        '<div class="success-box">✅ Courier Saved Successfully!</div>',
        unsafe_allow_html=True
    )

    # WhatsApp Message Display
    st.subheader("📲 WhatsApp Auto Reply")

    st.text_area(
        "Message",
        whatsapp_message,
        height=250
    )

    # WhatsApp Send Button
    st.markdown(
        f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="
                background-color:#16A34A;
                color:white;
                padding:12px 25px;
                border:none;
                border-radius:10px;
                font-size:18px;
                cursor:pointer;
            ">
                Send WhatsApp Message
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# =====================================
# DISPLAY DATA
# =====================================
if len(st.session_state.data) > 0:

    st.divider()

    st.subheader("📋 Courier Records")

    df = pd.DataFrame(st.session_state.data)

    st.dataframe(
        df,
        use_container_width=True
    )

    # CSV Download
    csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name=f"courier_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
