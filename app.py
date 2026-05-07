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
# CSS
# =====================================================

st.markdown("""
<style>

.main {
    padding-top: 10px;
}

.stButton > button {
    background-color: #0E7490;
    color: white;
    border-radius: 10px;
    padding: 12px;
    border: none;
    width: 100%;
}

.title-box {
    background: #0F172A;
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.success-box {
    background: #DCFCE7;
    padding: 15px;
    border-radius: 10px;
    color: #166534;
    font-size: 18px;
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
    <h4>📞 {SHOP_MOBILE}</h4>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
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

        mobile = st.text_input("📱 Mobile Number")

        from_city = st.text_input("📍 From City")

        to_city = st.text_input("🏙 To City")

    with col2:

        amount = st.text_input("💰 Amount")

        tracking_no = st.text_input("🔢 Tracking Number")

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
# SAVE DATA
# =====================================================

if submitted:

   tracking_link = (
    f"https://trackcourier.in/track-shreetirupati.php?cno={tracking_no}"
)

    whatsapp_message = f"""
नमस्कार {customer_name},

आपले कुरियर पाठवण्यात आले आहे 📦

📍 From : {from_city}
🏙 To : {to_city}

🚚 Courier : {courier_company}
🔢 Tracking No : {tracking_no}

Tracking Link 👇
{tracking_link}

💰 Amount : {amount}

धन्यवाद 🙏

{SHOP_NAME}
📞 {SHOP_MOBILE}
"""

    encoded_message = urllib.parse.quote(whatsapp_message)

    whatsapp_link = (
        f"https://wa.me/91{mobile}?text={encoded_message}"
    )

    row = {
        "Date": str(courier_date),
        "Customer Name": customer_name,
        "Mobile": mobile,
        "From City": from_city,
        "To City": to_city,
        "Amount": amount,
        "Courier Company": courier_company,
        "Tracking Number": tracking_no,
        "Tracking Link": tracking_link
    }

    st.session_state.courier_data.append(row)

    st.markdown(
        """
        <div class="success-box">
            ✅ Courier Saved Successfully!
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # WHATSAPP MESSAGE
    # =====================================================

    st.subheader("📲 WhatsApp Message")

    st.text_area(
        "Message",
        whatsapp_message,
        height=250
    )

    st.markdown(
        f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="
                background:#16A34A;
                color:white;
                padding:15px;
                border:none;
                border-radius:10px;
                width:100%;
                font-size:18px;
                cursor:pointer;
            ">
                📲 Send WhatsApp Message
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# SHOW DATA
# =====================================================

if len(st.session_state.courier_data) > 0:

    st.divider()

    st.subheader("📋 Courier Records")

    df = pd.DataFrame(st.session_state.courier_data)

    st.dataframe(df, use_container_width=True)

    # =====================================================
    # EXCEL DOWNLOAD
    # =====================================================

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

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
