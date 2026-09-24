import streamlit as st
import pywhatkit
from datetime import datetime
import time
import os
import tempfile


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="WhatsApp Message Scheduler",
    page_icon="📱",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("📱 WhatsApp Message Scheduler")

st.write(
    "Schedule a message and image for multiple WhatsApp numbers."
)

st.divider()


# =========================================================
# 1. WHATSAPP NUMBERS
# =========================================================

st.subheader("📞 WhatsApp Recipients")

numbers_input = st.text_area(
    "Enter WhatsApp numbers separated by comma",
    placeholder="+919588792043, +919729276531",
    height=100,
    help="Example: +919588792043, +919729276531"
)


# =========================================================
# 2. MESSAGE
# =========================================================

st.subheader("💬 Message")

message = st.text_area(
    "Enter your message",
    placeholder="Hello! This is a scheduled message.",
    height=120
)


# =========================================================
# 3. IMAGE
# =========================================================

st.subheader("🖼️ Image")

uploaded_file = st.file_uploader(
    "Choose JPG, JPEG or PNG",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Selected Image",
        width=350
    )


# =========================================================
# 4. SELECT DATE
# =========================================================

st.subheader("📅 Select Date")

selected_date = st.date_input(
    "Choose the day on which you want to send the message"
)


# =========================================================
# 5. SELECT TIME
# =========================================================

st.subheader("⏰ Select Time")

selected_time = st.time_input(
    "Choose the time at which you want to send the message"
)


# =========================================================
# 6. SCHEDULE BUTTON
# =========================================================

st.divider()

schedule_button = st.button(
    "🚀 Schedule Message",
    type="primary",
    use_container_width=True
)


# =========================================================
# 7. WHEN BUTTON IS CLICKED
# =========================================================

if schedule_button:

    # =====================================================
    # VALIDATE PHONE NUMBERS
    # =====================================================

    if not numbers_input.strip():

        st.error(
            "❌ Please enter at least one WhatsApp number."
        )

        st.stop()


    # =====================================================
    # CLEAN PHONE NUMBERS
    # =====================================================

    raw_numbers = numbers_input.split(",")

    phone_numbers = []


    for number in raw_numbers:

        phone = number.strip()

        # Remove spaces
        phone = phone.replace(" ", "")

        # Remove hyphens
        phone = phone.replace("-", "")

        # Remove brackets
        phone = phone.replace("(", "")
        phone = phone.replace(")", "")

        if phone:

            phone_numbers.append(phone)


    # =====================================================
    # VALIDATE PHONE NUMBERS
    # =====================================================

    invalid_numbers = []
    valid_numbers = []


    for phone in phone_numbers:

        if not phone.startswith("+"):

            invalid_numbers.append(phone)

        elif not phone[1:].isdigit():

            invalid_numbers.append(phone)

        else:

            valid_numbers.append(phone)


    if invalid_numbers:

        st.error("❌ Invalid WhatsApp number(s):")

        for number in invalid_numbers:

            st.write(f"• {number}")

        st.info(
            "Use international format such as "
            "+919588792043"
        )

        st.stop()


    if not valid_numbers:

        st.error(
            "❌ No valid WhatsApp numbers found."
        )

        st.stop()


    # =====================================================
    # VALIDATE MESSAGE
    # =====================================================

    if not message.strip():

        st.error(
            "❌ Please enter a message."
        )

        st.stop()


    # =====================================================
    # VALIDATE IMAGE
    # =====================================================

    if uploaded_file is None:

        st.error(
            "❌ Please select an image."
        )

        st.stop()


    # =====================================================
    # CHECK IMAGE FORMAT
    # =====================================================

    extension = os.path.splitext(
        uploaded_file.name
    )[1].lower()


    if extension not in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:

        st.error(
            "❌ Only JPG, JPEG and PNG files are supported."
        )

        st.stop()


    # =====================================================
    # SAVE IMAGE TEMPORARILY
    # =====================================================

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            image_path = temp_file.name

    except Exception as error:

        st.error(
            f"❌ Could not save image: {error}"
        )

        st.stop()


    # =====================================================
    # CREATE SELECTED DATE + TIME
    # =====================================================

    scheduled_datetime = datetime.combine(
        selected_date,
        selected_time
    )


    # =====================================================
    # CHECK WHETHER DATE/TIME IS IN THE PAST
    # =====================================================

    now = datetime.now()


    if scheduled_datetime <= now:

        st.error(
            "❌ The selected date and time have already passed."
        )

        st.info(
            "Please select a future date and time."
        )

        os.remove(image_path)

        st.stop()


    # =====================================================
    # SHOW SCHEDULE INFORMATION
    # =====================================================

    st.success(
        "✅ Message scheduled!"
    )


    st.write("### 📋 Schedule Details")


    st.write(
        "**📅 Date:** "
        + scheduled_datetime.strftime(
            "%d-%m-%Y"
        )
    )


    st.write(
        "**⏰ Time:** "
        + scheduled_datetime.strftime(
            "%I:%M %p"
        )
    )


    st.write(
        "**🖼️ Image:** "
        + uploaded_file.name
    )


    st.write(
        "**💬 Message:** "
        + message
    )


    st.write(
        "**📞 Recipients:**"
    )


    for phone in valid_numbers:

        st.write(
            f"• {phone}"
        )


    # =====================================================
    # IMPORTANT WARNING
    # =====================================================

    st.warning(
        "⚠️ Keep this computer ON and connected to "
        "the internet until the scheduled message is sent."
    )


    st.warning(
        "⚠️ Keep WhatsApp Web logged in and do not "
        "manually interact with the browser while sending."
    )


    # =====================================================
    # WAIT FOR SELECTED DATE + TIME
    # =====================================================

    st.write(
        "## ⏳ Waiting for Scheduled Time"
    )


    countdown_box = st.empty()


    while datetime.now() < scheduled_datetime:

        remaining = (
            scheduled_datetime -
            datetime.now()
        )


        remaining_text = str(
            remaining
        ).split(".")[0]


        countdown_box.info(
            f"⏳ Time remaining: {remaining_text}"
        )


        time.sleep(1)


    # =====================================================
    # SELECTED TIME REACHED
    # =====================================================

    countdown_box.success(
        "🟢 Scheduled time reached!"
    )


    st.write(
        "## 📤 Sending Messages"
    )


    total_numbers = len(valid_numbers)

    progress_bar = st.progress(0)


    successful = []
    failed = []


    # =====================================================
    # SEND TO EACH NUMBER
    # =====================================================

    for index, phone in enumerate(valid_numbers):

        st.write(
            f"### 📤 Sending to {phone}"
        )


        try:

            pywhatkit.sendwhats_image(
                receiver=phone,
                img_path=image_path,
                caption=message,
                wait_time=30,
                tab_close=True,
                close_time=5
            )


            successful.append(phone)


            st.success(
                f"✅ Message sent successfully to {phone}"
            )


        except Exception as error:

            failed.append(
                (
                    phone,
                    str(error)
                )
            )


            st.error(
                f"❌ Message could not be processed for {phone}"
            )


            st.code(
                str(error)
            )


        # =================================================
        # UPDATE PROGRESS
        # =================================================

        progress_bar.progress(
            int(
                ((index + 1) / total_numbers) * 100
            )
        )


        # =================================================
        # WAIT BEFORE NEXT NUMBER
        # =================================================

        if index < total_numbers - 1:

            st.info(
                "⏳ Preparing the next recipient..."
            )

            time.sleep(10)


    # =====================================================
    # FINAL REPORT
    # =====================================================

    st.divider()

    st.write(
        "## 📊 Final Report"
    )


    if successful:

        st.success(
            f"✅ Message sent to "
            f"{len(successful)} recipient(s)."
        )


        for phone in successful:

            st.write(
                f"✅ {phone}"
            )


    if failed:

        st.error(
            f"❌ Failed for "
            f"{len(failed)} recipient(s)."
        )


        for phone, error in failed:

            st.write(
                f"❌ {phone}"
            )


    # =====================================================
    # NO RECURRING SCHEDULE
    # =====================================================

    st.info(
        "ℹ️ This message was scheduled only for the "
        "date and time you selected. It will NOT be "
        "automatically scheduled for the next day."
    )


    # =====================================================
    # CLEAN TEMPORARY IMAGE
    # =====================================================

    try:

        if os.path.exists(image_path):

            os.remove(image_path)

    except Exception:

        pass


    # =====================================================
    # FINAL MESSAGE
    # =====================================================

    st.success(
        "🎉 Message sending process completed!"
    )
