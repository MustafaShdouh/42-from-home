from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum
from typing import List, Self


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> Self:
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        has_lead = any(member.rank in (Rank.CAPTAIN, Rank.COMMANDER)
                       for member in self.crew)
        if not has_lead:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        if self.duration_days > 365:
            experienced_count = sum(
                1 for member in self.crew if member.years_experience >= 5)
            if (experienced_count / len(self.crew)) < 0.5:
                raise ValueError(
                    "Long missions (> 365 days) need "
                    "50% experienced crew (5+ years)")

        all_active = all(member.is_active for member in self.crew)
        if not all_active:
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    messages = {
        "mission_id": "Mission ID must be between 5 and 15 characters.",
        "mission_name": "Mission name must be between 3 and 100 characters.",
        "destination": "Destination must be between 3 and 50 characters.",
        "launch_date": "Launch date is missing or invalid.",
        "duration_days": "Duration must be between 1 and 3650 days.",
        "crew": "Crew requirements not met. Check nested member data.",
        "mission_status": "Invalid mission status.",
        "budget_millions": "Budget must be between 1.0 and 10000.0 million."
    }

    print("Space Mission Crew Validation\n"
          "=========================================")

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.fromisoformat("2024-09-01T08:00:00+00:00"),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(member_id="C01", name="Sarah Connor",
                           rank=Rank.COMMANDER, age=45,
                           specialization="Mission Command",
                           years_experience=15, is_active=True),
                CrewMember(member_id="C02", name="John Smith",
                           rank=Rank.LIEUTENANT, age=35,
                           specialization="Navigation",
                           years_experience=8, is_active=True),
                CrewMember(member_id="C03", name="Alice Johnson",
                           rank=Rank.OFFICER, age=28,
                           specialization="Engineering", years_experience=3,
                           is_active=True)
            ]
        )
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(
                f" - {member.name} ({member.rank.value})"
                f" - {member.specialization}")
        print("=========================================")
    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0]) if error["loc"] else "model"
            if field in messages:
                print(messages[field])
            else:
                clean_msg = error['msg'].replace('Value error, ', '')
                print(f"Validation Error: {clean_msg}")

    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Lunar Base Alpha",
            destination="Moon",
            launch_date=datetime.fromisoformat("2024-10-01T08:00:00+00:00"),
            duration_days=400,
            budget_millions=500.0,
            crew=[
                CrewMember(member_id="C04", name="Bob Bobson",
                           rank=Rank.LIEUTENANT,
                           specialization="Geology", years_experience=4,
                           is_active=True, age=20),
                CrewMember(member_id="C05", name="Eve Evans",
                           rank=Rank.OFFICER, age=25,
                           specialization="Life Support", years_experience=6,
                           is_active=True),
                CrewMember(member_id="C06", name="Mustafa Shdouh",
                           rank=Rank.OFFICER, age=20,
                           specialization="Software Engineer",
                           years_experience=6, is_active=True)
            ]
        )
    except ValidationError as e:
        for error in e.errors():
            field = str(error["loc"][0]) if error["loc"] else "model"
            if field in messages:
                print(messages[field])
            else:
                clean_msg = error['msg'].replace('Value error, ', '')
                print(f"{clean_msg}")


if __name__ == "__main__":
    main()
