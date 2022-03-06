from datetime import datetime

from .Settlement import Settlement
from .Gender import Gender
from pathlib import Path


class Person:
    def __init__(self,
                 user_id: int,
                 name: str,
                 date_of_birth: datetime,
                 gender: Gender,
                 settlement: Settlement,
                 bio: str | None,
                 height: str | None,
                 enabled: bool,
                 registration_date: datetime,
                 path_to_photo: str,
                 instagram: str | None,
                 tiktok: str | None
                 ):
        self.user_id = user_id
        self.tiktok = tiktok
        self.instagram = instagram
        self.path_to_photo = Path(path_to_photo)
        self.registration_date = registration_date
        self.height = height
        self.enabled = enabled
        self.bio = bio
        self.settlement = settlement
        self.gender = gender
        self.name = name
        self.date_of_birth = date_of_birth
