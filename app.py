import streamlit as st
        "Amount": amount,
        "Courier": courier_company,
        "Tracking No": tracking_no,
        "Tracking Link": tracking_link
    }

    st.session_state.data.append(row)

    st.markdown(
        '<div class="success-box">✅ Courier Saved Successfully!</div>',
        unsafe_allow_html=True
    )

    st.write("### WhatsApp Auto Reply")

    st.text_area("Message", whatsapp_message, height=250)

    st.markdown(
        f"""
        <a href='{whatsapp_link}' target='_blank'>
            <button style='background-color:#16A34A;color:white;padding:12px 25px;border:none;border-radius:10px;font-size:18px;'>
                📲 Send WhatsApp Message
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# =====================================
# DATA TABLE
# =====================================
if st.session_state.data:

    st.divider()
    st.subheader("📋 Courier Records")

    df = pd.DataFrame(st.session_state.data)

    st.dataframe(df, use_container_width=True)

    # =====================================
    # DOWNLOAD CSV
    # =====================================
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name=f"courier_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
