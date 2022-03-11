from datetime import date

def age(date_of_birth):
    today =  date.today()
    if date_of_birth.month <= today.month and date_of_birth.day <= today.day:
       return today.year - date_of_birth.year
    return today.year - date_of_birth.year - 1