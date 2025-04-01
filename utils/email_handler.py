import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OWNER_EMAIL = "chsieh3@scu.edu"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EXCEL_FILE = "bookings.xlsx"

def send_email_notification(customer_info, pets):
    # Create Excel in memory
    data = {
        **customer_info,
        **{f"pet{i+1}_{k}": v for i, pet in enumerate(pets) for k, v in pet.items()},
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    df = pd.DataFrame([data])

    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    # Email content
    msg = EmailMessage()
    msg["Subject"] = "New J.Sit & Stay Booking 🐾"
    msg["From"] = OWNER_EMAIL
    msg["To"] = OWNER_EMAIL

    pet_details = "\n".join(
        [f"- {p['Name']} ({p['Type']}, Drop-off: {p['Drop-off Date']} at {p['Drop-off Time']})" for p in pets]
    )
    body = f"""Hi Jerry,

You've got a new booking inquiry! 📅

Customer: {customer_info['first_name']} {customer_info['last_name']}
Phone: {customer_info['phone']}
Pets: {len(pets)}

Pet Details:
{pet_details}

Please check attached intake sheet.

– J.Sit & Stay Assistant
"""
    msg.set_content(body)

    # Attach Excel file
    filename = f"booking_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    msg.add_attachment(excel_buffer.read(), maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(OWNER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
