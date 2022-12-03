from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def start_command(message: types.Message, state: FSMContext):
    if message.chat.type != 'private':  # start only in private messages
        return
    await state.finish()
    await message.answer(
        "👋Добро пожаловать в бот для автопостинга в канал 🃏Fool House🃏 !\n"
        "Список комманд:\n"
        "/setpost - добавить в расписание пост\n"
        "/deletepost - убрать пост из расписания\n"
        "/sendpost - отправить пост сейчас"
    )


def register_handlers(dp: Dispatcher):
    """Register message handlers"""
    dp.register_message_handler(start_command, commands="start", state='*')
