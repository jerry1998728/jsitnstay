import streamlit as st
from utils.email_handler import send_email_notification
from utils.excel_writer import save_booking_to_excel

def booking_manager(message):
    if "booking_state" not in st.session_state:
        st.session_state.booking_state = {
            "step": 0,
            "customer_info": {},
            "pets": [],
            "current_pet": {},
            "num_pets": 0,
            "completed": False  # ✅ Added flag
        }

    state = st.session_state.booking_state
    response = ""

    if state["step"] == 0:
        response = "Thanks for your inquiry! Let’s get started with your first name?"
        state["step"] = 1

    elif state["step"] == 1:
        state["customer_info"]["first_name"] = message
        response = "Thanks! And your last name?"
        state["step"] = 2

    elif state["step"] == 2:
        state["customer_info"]["last_name"] = message
        response = "Got it. What’s the best phone number to reach you?"
        state["step"] = 3

    elif state["step"] == 3:
        state["customer_info"]["phone"] = message
        response = "Perfect. How many pets are you booking for today?"
        state["step"] = 4

    elif state["step"] == 4:
        try:
            state["num_pets"] = int(message)
            state["step"] = 5
            state["current_pet"] = {}
            response = "Let’s start with your first pet. What’s their name?"
        except ValueError:
            response = "Please enter a number for how many pets you’re booking for."

    elif state["step"] == 5:
        state["current_pet"]["Name"] = message
        response = "Are they a dog or a cat?"
        state["step"] = 6

    elif state["step"] == 6:
        state["current_pet"]["Type"] = message
        response = "What’s their sex? (Male or Female)"
        state["step"] = 7

    elif state["step"] == 7:
        state["current_pet"]["Sex"] = message
        response = "What breed are they?"
        state["step"] = 8

    elif state["step"] == 8:
        state["current_pet"]["Breed"] = message
        response = "How old are they in months?"
        state["step"] = 9

    elif state["step"] == 9:
        try:
            state["current_pet"]["Age_months"] = int(message)
            response = "On a scale from 0 to 1, how friendly is your pet with others?"
            state["step"] = 10
        except ValueError:
            response = "Please enter their age as a number in months."

    elif state["step"] == 10:
        try:
            state["current_pet"]["Friendliness"] = float(message)
            response = "What type of food do they eat? (Wet, Dry, Mixed)"
            state["step"] = 11
        except ValueError:
            response = "Please enter a number between 0.0 and 1.0 for friendliness."

    elif state["step"] == 11:
        state["current_pet"]["Food_type"] = message
        response = "How much do they eat per meal? (Ex. half bowl, 1 can, or 1 scoop)"
        state["step"] = 12

    elif state["step"] == 12:
        state["current_pet"]["Portion"] = message
        response = "How many times per day do they eat? (Ex. 1, 2, 3)"
        state["step"] = 13

    elif state["step"] == 13:
        state["current_pet"]["Frequency"] = message
        response = "Any medications or special needs? (Enter None if not needed)"
        state["step"] = 14

    elif state["step"] == 14:
        state["current_pet"]["Medication"] = message
        response = "What is the drop off date that you have in mind? (Ex. MM-DD-YYYY)"
        state["step"] = 15

    elif state["step"] == 15:
        state["current_pet"]["Drop-off Date"] = message
        response = "What drop off time works best for you? (Ex. 10AM/10PM)"
        state["step"] = 16

    elif state["step"] == 16:
        state["current_pet"]["Drop-off Time"] = message
        response = "You are almost there! When do you plan to pick up your fur baby? (Ex. MM-DD-YYYY)"
        state["step"] = 17

    elif state["step"] == 17:
        state["current_pet"]["Pick-up Date"] = message
        response = "And at what time to pick up?"
        state["step"] = 18

    elif state["step"] == 18:
        state["current_pet"]["Pick-up Time"] = message

        # ✅ Verify all required fields
        required_keys = ["Name", "Type", "Sex", "Breed", "Age_months", "Friendliness", "Food_type", "Portion", "Frequency", "Medication", "Drop-off Date", "Drop-off Time", "Pick-up Date", "Pick-up Time"]
        if all(k in state["current_pet"] for k in required_keys):
            state["pets"].append(state["current_pet"])
        else:
            return "⚠️ Something went wrong. Missing pet information. Please restart booking."

        if len(state["pets"]) < state["num_pets"]:
            response = f"Awesome! Now let’s continue with Pet {len(state['pets']) + 1}. What’s their name?"
            state["step"] = 5
            state["current_pet"] = {}
        else:
            send_email_notification(state["customer_info"], state["pets"])
            response = (
                "🎉 All Set! Jerry appreciates your effort in sharing all the details, and he will reach out as soon as possible to confirm your stay!<br>"
                "<br>"
                "To ensure a great experience for both you and your pets, please bring their food, bowls, and pee pads (if necessary)!<br>"
                "<br>"
                "In the future, you can simply message Jerry for direct and easy booking!<br>"
                "<br>"
                "✅ Booking completed. Feel free to ask me anything else now!"
            )
            state["completed"] = True  # ✅ mark as completed

    return response
