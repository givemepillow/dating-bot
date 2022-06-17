from core import Feed
from core.markups.inline import QuestionnaireOptionsSelector, LikeAnswerSelector
from core.services import MessageBox
from core.tools import age_suffix
from db.model import Person
from loader import bot, repository


async def send_quest(user_id: int, person: Person, action=None, me=False):
    _age, _suffix = age_suffix(person.date_of_birth)
    _message = await bot.send_photo(
        photo=person.photo, chat_id=user_id,
        caption=f"{person.name}, {person.settlement.name} - {_age} {_suffix}\n"
                f"\n {person.bio}",
        reply_markup=QuestionnaireOptionsSelector.markup(action) if not me else None
    )
    if not me:
        MessageBox.put(_message, user_id)


async def send_like(from_user_id: int, message: str | None = None):
    to_user_id = Feed(from_user_id).current_id
    await bot.send_message(text='Тебя лайкнули!', chat_id=to_user_id)
    from_person = repository.get_person(from_user_id)
    _age, _suffix = age_suffix(from_person.date_of_birth)
    Feed(to_user_id).set_like(from_user_id)
    await bot.send_photo(photo=from_person.photo, chat_id=to_user_id,
                         caption=f"{from_person.name}, {from_person.settlement.name} - {_age} {_suffix}\n"
                                 f"\n {from_person.bio}",
                         reply_markup=LikeAnswerSelector.markup()
                         )
    if message:
        await bot.send_message(text=f"Сообщение от {from_person.name}:\n{message}", chat_id=to_user_id)


async def send_quest_if_person(user_id: int, person: Person):
    if person:
        await send_quest(user_id, person)
    else:
        await bot.send_message(text='Подходящих анкет больше нет...', chat_id=user_id)
