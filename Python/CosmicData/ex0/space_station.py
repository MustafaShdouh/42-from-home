from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class User(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: str | None = Field(min_length=0, max_length=200)


def main() -> None:

    messages = {
        "crew_size": "Crew size should be less than or equal to 20.",
        "station_id": "Station ID is missing or invalid.",
        "name": "Station Name is missing or invalid.",
        "last_maintenance": "Last maintenance date is missing or invalid.",
        "power_level": "Power level must be between 0.0 and 100.0.",
        "oxygen_level": "Oxygen level must be between 0.0 and 100.0.",
        "notes": "Notes should be grater than 0 and less than 200",
    }

    try:
        user = User(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2005-09-06"),
            is_operational=True,
            notes=None,
        )
    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0]) if error["loc"] else "unknown"
            print(messages.get(field, f"Error in {field}: {error['msg']}"))

    print("Space Station Data Validation")
    print("========================================")
    try:
        print("Valid station created:")
        print(f"ID: {user.station_id}")
        print(f"Name: {user.name}")
        print(f"Crew: {user.crew_size} people")
        print(f"Power: {user.power_level}%")
        print(f"Oxygen: {user.oxygen_level}%")
        print(
            "Status: Operational" if user.is_operational else "Status: Not Operational"
        )
        print("\n========================================")
    except UnboundLocalError:
        print("Not all the variables are initialized")

    print("Expected validation error:")
    try:
        User(
            station_id="ISS001",
            name="International Space Station",
            crew_size=21,
            power_level=50.3,
            oxygen_level=78.5,
            last_maintenance=datetime.fromisoformat("2005-09-06"),
            is_operational=True,
            notes=None,
        )
    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0]) if error["loc"] else "unknown"
            print(messages.get(field, f"Error in {field}: {error['msg']}"))


if __name__ == "__main__":
    main()
