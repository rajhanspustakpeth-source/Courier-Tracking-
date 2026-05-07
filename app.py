import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from io import BytesIO

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="राजहंस पुस्तक पेठ Courier System",
    page_icon="📦",
    layout="wide"
)

# =====================================================
# SHOP DETAILS
# =====================================================
SHOP_NAME = "राजहंस पुस्तक पेठ , पुणे ०३८"
SHOP_MOBILE = "9322630703"

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

.main {
    padding-top: 10px;
}

.stButton > button {
    background-color: #0E7490;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-size: 16px;
    width: 100%;
}

.success-box {
    padding: 15px;
    background-color: #DCFCE7;
    border-radius: 10px;
    color: #166534;
    font-size: 18px;
    margin-top: 10px;
}

.title-box {
    background-color: #0F172A;
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.markdown(f"""
<div class="title-box">
    <h1>📦 Courier Management System</h1>
    <h3>{SHOP_NAME}</h3>
    <p>📞 {SHOP_MOBILE}</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STORAGE
# =====================================================
if "courier_data" not in st.session_state:
    st.session_state.courier_data = []

# =====================================================
# FORM
# =====================================================
with st.form("courier_form"):

    col1, col2 = st.columns(2)

    with col1:

        customer_name = st.text_input("👤 Customer Name")

        mobile = st.text_input("📱 Customer Mobile Number")

        city = st.text_input("🏙 City")

        tracking_no = st.text_input("🔢 Tracking Number")

    with col2:

        book_name = st.text_input("📚 Book Name")

        amount = st.text_input("💰 Amount")

        courier_company = st.selectbox(
            "🚚 Courier Company",
            [
                "Shree Tirupati Courier",
                "DTDC",
                "India Post",
                "Professional",
                "Other"
            ]
        )

        courier_date = st.date_input("📅 Courier Date")

    submitted = st.form_submit_button("✅ Save Courier")

# =====================================================
# SAVE
# =====================================================
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

📚 पुस्तक : {book_name}
🏙 शहर : {city}
🚚 Courier : {courier_company}
🔢 Tracking No : {tracking_no}

Tracking Link 👇
{tracking_link}

धन्यवाद 🙏

{SHOP_NAME}
📞 {SHOP_MOBILE}
"""

    # Encode WhatsApp Message
    encoded_message = urllib.parse.quote(whatsapp_message)

    # WhatsApp Link
    whatsapp_link = (
        f"https://wa.me/91{mobile}?text={encoded_message}"
    )

    # Store Data
    row = {
        "Date": str(courier_date),
        "Customer Name": customer_name,
        "Mobile": mobile,
        "City": city,
        "Book Name": book_name,
        "Amount": amount,
        "Courier Company": courier_company,
        "Tracking Number": tracking_no,
        "Tracking Link": tracking_link
    }

    st.session_state.courier_data.append(row)

    # Success
    st.markdown(
        """
        <div class="success-box">
            ✅ Courier Saved Successfully!
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show Message
    st.subheader("📲 WhatsApp Auto Reply")

    st.text_area(
        "WhatsApp Message",
        whatsapp_message,
        height=250
    )

    # WhatsApp Button
    st.markdown(
        f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="
                background-color:#16A34A;
                color:white;
                padding:14px 20px;
                border:none;
                border-radius:10px;
                font-size:18px;
                width:100%;
                cursor:pointer;
            ">
                📲 Send WhatsApp Message
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# DISPLAY TABLE
# =====================================================
if len(st.session_state.courier_data) > 0:

    st.divider()

    st.subheader("📋 Courier Records")

    df = pd.DataFrame(st.session_state.courier_data)

    st.dataframe(
        df,
        use_container_width=True
    )

    # =================================================
    # EXCEL DOWNLOAD
    # =================================================
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Courier Data"
        )

    excel_data = output.getvalue()

    st.download_button(
        label="⬇ Download Excel File",
        data=excel_data,
        file_name=f"Courier_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
