import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO
from datetime import datetime

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Courier System",
    page_icon="📦",
    layout="wide"
)

# =========================================
# SHOP DETAILS
# =========================================

SHOP_NAME = "राजहंस पुस्तक पेठ , पुणे ०३८"
SHOP_MOBILE = "9322630703"

# =========================================
# SESSION STATE
# =========================================

if "courier_data" not in st.session_state:
    st.session_state.courier_data = []

# =========================================
# TITLE
# =========================================

st.title("📦 Courier Management System")
st.subheader(f"{SHOP_NAME} | 📞 {SHOP_MOBILE}")

# =========================================
# FORM
# =========================================

with st.form("courier_form"):

    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name")
        mobile = st.text_input("Mobile Number")
        from_city = st.text_input("From City")
        to_city = st.text_input("To City")

    with col2:
        amount = st.text_input("Amount")
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

        courier_date = st.date_input("Courier Date")

    submitted = st.form_submit_button("Save Courier")

# =========================================
# SAVE DATA
# =========================================

if submitted:

    tracking_link = (
        "https://trackcourier.in/track-shreetirupati.php?cno="
        + tracking_no
    )

    whatsapp_message = (
        f"नमस्कार {customer_name},\n\n"
        f"आपले कुरियर पाठवण्यात आले आहे 📦\n\n"
        f"📍 From : {from_city}\n"
        f"🏙 To : {to_city}\n\n"
        f"🚚 Courier : {courier_company}\n"
        f"🔢 Tracking No : {tracking_no}\n\n"
        f"धन्यवाद 🙏\n\n"
        f"{SHOP_NAME}\n"
        f"📞 {SHOP_MOBILE}"
    )

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

    st.success("Courier Saved Successfully!")

    # =====================================
    # WHATSAPP MESSAGE
    # =====================================

    st.subheader("WhatsApp Message")

    st.text_area(
        "Message",
        whatsapp_message,
        height=250
    )

    st.markdown(
        f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="
                background-color:green;
                color:white;
                padding:12px;
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

# =========================================
# SHOW TABLE
# =========================================

if len(st.session_state.courier_data) > 0:

    st.divider()

    st.subheader("Courier Records")

    df = pd.DataFrame(st.session_state.courier_data)

    st.dataframe(df, use_container_width=True)

    # =====================================
    # EXCEL DOWNLOAD
    # =====================================

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
