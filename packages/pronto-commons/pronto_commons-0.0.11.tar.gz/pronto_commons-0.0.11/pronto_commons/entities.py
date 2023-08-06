from dataclasses import dataclass, field


@dataclass
class Point:
    latitude: float
    longitude: float


@dataclass
class PhoneNumber:
    country_code: int
    national_number: int
    international_format: str = field(init=False)

    def __post_init__(self):
        # Creates the international format of the phone number
        self.international_format = f"+{self.country_code}{self.national_number}"
