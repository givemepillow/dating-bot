from datetime import date

from pathlib import Path


class Person:
    def __init__(self,
                 user_id: int,
                 name: str,
                 date_of_birth: date,
                 gender: str,
                 looking_for: str,
                 settlement_id: int,
                 path_to_photo: str,
                 bio: str | None = None,
                 height: str | None = None,
                 enabled: bool = True,
                 registration_date: date = date.today(),
                 instagram: str | None = None,
                 tiktok: str | None = None
                 ):
        self.user_id = user_id
        self.tiktok = tiktok
        self.instagram = instagram
        if Path(path_to_photo).exists():
            self.path_to_photo = path_to_photo
        else:
            raise FileNotFoundError("Path to photo don't exists.")
        self.registration_date = registration_date
        self.height = height
        self.enabled = enabled
        self.bio = bio
        self.settlement_id = settlement_id
        self.gender = gender
        self.name = name
        if isinstance(date_of_birth, date):
            self.date_of_birth = date_of_birth
        else:
            raise ValueError("Expected datetime type.")
        self.looking_for = looking_for
