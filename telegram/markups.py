from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.controllers import post_controller


def get_shedule_confirmation_menu() -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text='👍 Подтвердить', callback_data='schedule_approve'),
        InlineKeyboardButton(text='❌ Отмена', callback_data='schedule_cancel')
    ]
    for button in buttons:
        menu.insert(button)
    return menu


def get_post_buttons() -> InlineKeyboardMarkup:
    posts = post_controller.db_read_post_data()
    menu = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for post in posts:
        post_text = ' | '.join([post.get('post_text'), post.get('schedule_period'), post.get('schedule_time')])
        buttons.append(InlineKeyboardButton(text=post_text, callback_data=f'post_id_{post.get("id")}'))
    for button in buttons:
        menu.insert(button)
    return menu


get_post_buttons()


def get_shedule_period_buttons() -> InlineKeyboardMarkup:
    menu = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='каждый день', callback_data='schedule_period_everyday'),
        InlineKeyboardButton(text='каждый понедельник', callback_data='schedule_period_monday'),
        InlineKeyboardButton(text='каждый вторник', callback_data='schedule_period_tuesday'),
        InlineKeyboardButton(text='каждую среду', callback_data='schedule_period_wednesday'),
        InlineKeyboardButton(text='каждый четверг', callback_data='schedule_period_thursday'),
        InlineKeyboardButton(text='каждую пятницу', callback_data='schedule_period_friday'),
        InlineKeyboardButton(text='каждую субботу', callback_data='schedule_period_saturday'),
        InlineKeyboardButton(text='каждое воскресенье', callback_data='schedule_period_sunday'),
    ]
    for button in buttons:
        menu.insert(button)
    return menu
