ALLOWED_CLINIC_TOPICS = (
    "appointment", "schedule", "scheduling", "business hours", "hours", "address", "location",
    "clinic", "dentist", "dental", "treatment", "service", "preparation", "insurance",
    "payment", "care", "administrative", "cleaning", "whitening", "root canal", "implant",
    "extraction", "braces",
)

OUT_OF_SCOPE_RESPONSE = (
    "I can only help with dental clinic-related topics, such as appointments, scheduling, "
    "business hours, address, services, and administrative questions."
)


def is_within_scope(text: str) -> bool:
    text = text.lower()
    return any(topic in text for topic in ALLOWED_CLINIC_TOPICS)
