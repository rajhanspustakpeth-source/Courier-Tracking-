import streamlit as st
import pandas as pd
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
# CREATE MONTHLY REPORT FOLDER
# =====================================================

os.makedirs("monthly_reports", exist_ok=True)

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
    border-radius: 10px;
    padding: 12px;
    border: none;
    width: 100%;
    font-size: 16px;
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

        mobile = st.text_input("📱 Customer Mobile Number")

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

    # =================================================
    # TRACKING LINK
    # =================================================

   tracking_link = (
    f"https://trackcourier.in/track-shreetirupati.php?cno={tracking_no}"
)
    # =================================================
    # WHATSAPP MESSAGE
    # =================================================

    whatsapp_message = (
        f"नमस्कार {customer_name},\n\n"
        f"आपले कुरियर पाठवण्यात आले आहे 📦\n\n"
        f"📍 From : {from_city}\n"
        f"🏙 To : {to_city}\n\n"
        f"🚚 Courier : {courier_company}\n"
        f"🔢 Tracking No : {tracking_no}\n\n"
        f"Tracking Link 👇\n"
        f"{tracking_link}\n\n"
       
        f"धन्यवाद 🙏\n\n"
        f"{SHOP_NAME}\n"
        f"📞 {SHOP_MOBILE}"
    )

    # =================================================
    # WHATSAPP LINK
    # =================================================

    encoded_message = urllib.parse.quote(whatsapp_message)

    whatsapp_link = (
        f"https://wa.me/91{SHOP_MOBILE}?text={encoded_message}"
    )

    # =================================================
    # SAVE ROW
    # =================================================

    row = {
        "Date": str(courier_date),
        "Customer Name": customer_name,
        "Customer Mobile": mobile,
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

    # =================================================
    # SHOW MESSAGE
    # =================================================

    st.subheader("📲 WhatsApp Message")

    st.text_area(
        "Message",
        whatsapp_message,
        height=250
    )

    # =================================================
    # SEND WHATSAPP BUTTON
    # =================================================

    st.markdown(
        f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="
                background-color:#16A34A;
                color:white;
                padding:15px;
                border:none;
                border-radius:10px;
                width:100%;
                font-size:18px;
                cursor:pointer;
            ">
                📲 Send WhatsApp SMS
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    # =================================================
    # SAVE MONTHLY EXCEL
    # =================================================

    save_df = pd.DataFrame(st.session_state.courier_data)

    current_month = datetime.now().strftime("%B_%Y")

    monthly_file_name = (
        f"monthly_reports/Courier_{current_month}.xlsx"
    )

    with pd.ExcelWriter(
        monthly_file_name,
        engine="xlsxwriter"
    ) as writer:

        save_df.to_excel(
            writer,
            index=False,
            sheet_name="Courier Report"
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
        label="⬇ Download Full Excel",
        data=excel_data,
        file_name="All_Courier_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # =================================================
    # MONTHLY REPORT DOWNLOAD
    # =================================================

    st.divider()

    st.subheader("📅 Monthly Reports")

    monthly_files = os.listdir("monthly_reports")

    excel_files = [
        file for file in monthly_files
        if file.endswith(".xlsx")
    ]

    if len(excel_files) > 0:

        selected_file = st.selectbox(
            "Select Monthly File",
            excel_files
        )

        file_path = f"monthly_reports/{selected_file}"

        with open(file_path, "rb") as file:

            st.download_button(
                label="⬇ Download Monthly Excel",
                data=file,
                file_name=selected_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
