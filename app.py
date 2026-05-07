import streamlit as st
import pandas as pd
import requests
import urllib.parse
from io import BytesIO
from datetime import datetime
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Courier Management System",
    page_icon="📦",
    layout="wide"
)

# =====================================================
# SHOP DETAILS
# =====================================================

SHOP_NAME = "राजहंस पुस्तक पेठ , पुणे ०३८"
SHOP_MOBILE = "9322630703"

# =====================================================
# YOUR CALLMEBOT API KEY
# =====================================================

API_KEY = "YOUR_API_KEY"

# =====================================================
# CREATE FOLDER
# =====================================================

os.makedirs("monthly_reports", exist_ok=True)

# =====================================================
# HEADER
# =====================================================

st.title("📦 Courier Management System")
st.subheader(f"{SHOP_NAME} | 📞 {SHOP_MOBILE}")

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

# =====================================================
# SAVE DATA
# =====================================================

if submitted:

    # =================================================
    # TRACKING LINK
    # =================================================

    tracking_link = (
        f"https://trackcourier.in/track-shreetirupati.php?cno={tracking_no}"
    )

    # =================================================
    # MESSAGE
    # =================================================

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

    # =================================================
    # SEND WHATSAPP
    # =================================================

    encoded_message = urllib.parse.quote(whatsapp_message)

    whatsapp_url = (
        f"https://api.callmebot.com/whatsapp.php?"
        f"phone=91{mobile}"
        f"&text={encoded_message}"
        f"&apikey={API_KEY}"
    )

    try:

        response = requests.get(whatsapp_url)

        if response.status_code == 200:

            whatsapp_status = "Sent"

            st.success("✅ WhatsApp Message Sent Successfully!")

        else:

            whatsapp_status = "Failed"

            st.error("❌ WhatsApp Sending Failed")

    except Exception as e:

        whatsapp_status = "Error"

        st.error(f"❌ Error : {e}")

    # =================================================
    # SAVE ROW
    # =================================================

    row = {
        "Date": str(courier_date),
        "Customer Name": customer_name,
        "Mobile": mobile,
        "From City": from_city,
        "To City": to_city,
        "Amount": amount,
        "Courier Company": courier_company,
        "Tracking Number": tracking_no,
        "Tracking Link": tracking_link,
        "WhatsApp Status": whatsapp_status
    }

    st.session_state.courier_data.append(row)

    # =================================================
    # DATAFRAME
    # =================================================

    df = pd.DataFrame(st.session_state.courier_data)

    # =================================================
    # MONTHLY SAVE
    # =================================================

    current_month = datetime.now().strftime("%B_%Y")

    monthly_file = (
        f"monthly_reports/Courier_{current_month}.xlsx"
    )

    with pd.ExcelWriter(
        monthly_file,
        engine="xlsxwriter"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Courier Report"
        )

    # =================================================
    # SHOW MESSAGE
    # =================================================

    st.subheader("WhatsApp Message")

    st.text_area(
        "Message",
        whatsapp_message,
        height=250
    )

# =====================================================
# SHOW TABLE
# =====================================================

if len(st.session_state.courier_data) > 0:

    st.divider()

    st.subheader("Courier Records")

    df = pd.DataFrame(st.session_state.courier_data)

    st.dataframe(
        df,
        use_container_width=True
    )

    # =================================================
    # FULL EXCEL DOWNLOAD
    # =================================================

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="All Courier Data"
        )

    excel_data = output.getvalue()

    st.download_button(
        label="Download Full Excel",
        data=excel_data,
        file_name="All_Courier_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # =================================================
    # MONTHLY FILE DOWNLOAD
    # =================================================

    st.divider()

    st.subheader("Monthly Reports")

    monthly_files = os.listdir("monthly_reports")

    excel_files = [
        file for file in monthly_files
        if file.endswith(".xlsx")
    ]

    if excel_files:

        selected_file = st.selectbox(
            "Select Monthly File",
            excel_files
        )

        file_path = f"monthly_reports/{selected_file}"

        with open(file_path, "rb") as file:

            st.download_button(
                label="Download Monthly Excel",
                data=file,
                file_name=selected_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
