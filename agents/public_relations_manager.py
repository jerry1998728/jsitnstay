def public_relations(message: str) -> str:
    msg = message.lower()

    if "discount" in msg or "cheaper" in msg:
        return (
            "🧾 Thanks so much for asking! We totally understand wanting the best value when it comes to your pet's care.\n\n"
            "Our pricing reflects not only all-day companionship and personalized care, but also:\n"
            "- Flat, transparent nightly rates — no surprise fees\n"
            "- Flexible drop-off and pick-up times\n"
            "- A clean, calm home environment (not a kennel!)\n"
            "- A dedicated sitter who prioritizes your pet's comfort and safety\n\n"
            "That said, Jerry is always happy to speak personally if there are special circumstances — feel free to text him directly at **707-660-0325**.\n\n"
            "🐾 We truly appreciate your trust in J.Sit & Stay!"
        )

    elif "payment" in msg or "pay" in msg or "venmo" in msg or "zelle" in msg:
        return "💳 We currently accept **Zelle** or **Venmo only**. You'll receive payment instructions once your booking is confirmed by Jerry."

    else:
        return "I'd be happy to help clarify our pricing or policies. Could you let me know what you're curious about?"
