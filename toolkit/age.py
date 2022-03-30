from datetime import date


def age(start_date: date):
    today = date.today()
    if start_date.month <= today.month and start_date.day <= today.day:
        return today.year - start_date.year
    return today.year - start_date.year - 1


def suffix(_age: date):
    ending = _age % 10
    if ending == 1:
        return 'год'
    if ending > 4 or 4 < _age < 21 or ending == 0:
        return 'лет'
    return 'года'


def age_suffix(start_date: date):
    _age = age(start_date)
    return _age, suffix(_age)
