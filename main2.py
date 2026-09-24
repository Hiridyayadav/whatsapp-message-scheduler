import pywhatkit
from datetime import datetime, timedelta
import time
import os

# ==========================================
# 1. ENTER MULTIPLE WHATSAPP NUMBERS
# ==========================================

numbers_input = input(
    "Enter WhatsApp numbers separated by comma (+91...): "
).strip()

phone_numbers = [
    number.strip()
    for number in numbers_input.split(",")
    if number.strip()
]

# ==========================================
# 2. ENTER MESSAGE
# ==========================================

message = input("Enter your message: ").strip()

# ==========================================
# 3. ENTER IMAGE PATH
# ==========================================

image_path = input(
    "Enter image path (.jpg, .jpeg or .png): "
).strip()

# Check whether file exists
if not os.path.isfile(image_path):
    print("\nERROR: Image file not found!")
    exit()

# Check image extension
extension = os.path.splitext(image_path)[1].lower()

if extension not in [".jpg", ".jpeg", ".png"]:
    print("\nERROR: Only JPG, JPEG and PNG files are supported!")
    exit()

# ==========================================
# 4. ENTER TIME
# ==========================================

time_input = input(
    "Enter time (HH:MM, 24-hour format): "
).strip()

# Validate time
try:
    hour, minute = map(int, time_input.split(":"))

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError

except ValueError:
    print("\nERROR: Invalid time!")
    print("Example: 18:30")
    exit()

# ==========================================
# 5. CALCULATE NEXT SCHEDULED TIME
# ==========================================

now = datetime.now()

scheduled = now.replace(
    hour=hour,
    minute=minute,
    second=0,
    microsecond=0
)

# If today's time has already passed,
# schedule for tomorrow
if scheduled <= now:
    scheduled += timedelta(days=1)

# ==========================================
# 6. SHOW SCHEDULE INFORMATION
# ==========================================

print("\n========================================")
print("       WHATSAPP MESSAGE SCHEDULER")
print("========================================")

print("\nNumbers:")
for number in phone_numbers:
    print("  ", number)

print("\nMessage:", message)
print("Image  :", image_path)
print("Type   :", extension.upper())

print(
    "\nScheduled Time:",
    scheduled.strftime("%d-%m-%Y %H:%M")
)

print("\nThe message will NOT be sent now.")
print("Waiting for scheduled time...")
print("Keep your computer and internet ON.")
print("Keep WhatsApp Web logged in.")

# ==========================================
# 7. WAIT UNTIL SCHEDULED TIME
# ==========================================

while datetime.now() < scheduled:
    remaining = scheduled - datetime.now()

    print(
        f"\rTime remaining: {str(remaining).split('.')[0]}",
        end=""
    )

    time.sleep(1)

print("\n\nScheduled time reached!")
print("Starting message delivery...\n")

# ==========================================
# 8. SEND TO MULTIPLE NUMBERS
# ==========================================

for phone in phone_numbers:

    print("--------------------------------")
    print("Sending to:", phone)

    try:

        pywhatkit.sendwhats_image(
            receiver=phone,
            img_path=image_path,
            caption=message,
            wait_time=15,
            tab_close=True,
            close_time=3
        )

        print("Message sent to:", phone)

    except Exception as e:

        print("Failed to send to:", phone)
        print("Error:", e)

    # Small delay before next number
    time.sleep(5)

# ==========================================
# 9. COMPLETION
# ==========================================

print("\n========================================")
print("All messages processed successfully!")
print("========================================")