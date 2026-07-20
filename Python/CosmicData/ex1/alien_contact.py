from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum
from typing import Self


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_contact_rules(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if self.contact_type == ContactType.TELEPATHIC \
           and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")

        return self


def main() -> None:
    messages = {
        "contact_id": "Contact ID must be between 5 and 15 characters.",
        "timestamp": "Timestamp is missing or invalid.",
        "location": "Location must be between 3 and 100 characters.",
        "contact_type": "Invalid contact type selected.",
        "signal_strength": "Signal strength must be between 0.0 and 10.0.",
        "duration_minutes": "Duration must be between 1 and 1440 minutes.",
        "witness_count": "Witness count must be between 1 and 100.",
        "message_received": "Message exceeds maximum length."
    }

    print("Alien Contact Log Validation")
    print("======================================")

    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.fromisoformat("2024-07-10T12:00:00+00:00"),
            location="visual at Atacama Desert, Chile",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )
        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'")
        print("======================================")
    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0]) if error["loc"] else "unknown"
            print(messages.get(field, f"Error in {field}: {error['msg']}"))
    except UnboundLocalError:
        print("Not all the variables are initialized")

    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="Ad_2024_002",
            timestamp=datetime.fromisoformat("2024-07-10T12:00:00+00:00"),
            location="Roswell, New Mexico",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=4.5,
            duration_minutes=15,
            witness_count=4,
            message_received=None,
            is_verified=False
        )
    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0]) if error["loc"] else "model"
            if field in messages:
                print(messages[field])
            else:
                clean_msg = error['msg'].replace('Value error, ', '')
                print(f"Validation Error: {clean_msg}")


if __name__ == "__main__":
    main()
