from datetime import datetime

from pathlib import Path


class Person:
    def __init__(self,
                 user_id: int,
                 name: str,
                 date_of_birth: datetime,
                 gender: str,
                 looking_for: str,
                 settlement: id,
                 path_to_photo: str,
                 bio: str | None = None,
                 height: str | None = None,
                 enabled: bool = True,
                 registration_date: datetime = datetime.now(),
                 instagram: str | None = None,
                 tiktok: str | None = None
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
        self.looking_for = looking_for
