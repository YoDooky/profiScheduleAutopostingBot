from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram import markups, aux_funcs
from database.controllers import post_controller


class PostState(StatesGroup):
    wait_schedule_period = State()
    wait_schedule_time = State()
    wait_schedule_approve_finish = State()
    wait_schedule_set_finish = State()


class SetPost:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def check_auth(decorated_func):
        """Auth decorator"""

        def inner(*args, **kwargs):
            decorated_func(*args, **kwargs)

        return inner

    @staticmethod
    async def add_post_content(message: types.Message, state: FSMContext):
        """Add post content"""
        await state.finish()
        await message.answer("👉 Напиши текст поста. Если пост с изображением, текст должен быть в подписи")
        await state.set_state(PostState.wait_schedule_period.state)

    @staticmethod
    async def edit_post_content(call: types.CallbackQuery, state: FSMContext):
        """Edit post content (same as add_post_content but made on callbacks)"""
        await state.finish()
        await call.message.edit_text("👉 Напиши текст поста. Если пост с изображением, текст должен быть в подписи")
        await state.set_state(PostState.wait_schedule_period.state)

    @staticmethod
    async def set_post_schedule_period(message: types.Message, state: FSMContext):
        """Set period of autoreposting"""
        try:
            photo_id = message.photo[-1].file_id
        except Exception as ex:
            photo_id = None
            pass
        post_text = message.text if not message.caption else message.caption
        if not post_text:
            await message.answer("⚠ Текст поста не должен быть пустым. Если во вложении изображение, "
                                 "пожалуйста укажи в подписи к нему текст поста")
            return
        await state.update_data(post_photo_id=photo_id, post_text=post_text)
        keyboard = markups.get_shedule_period_buttons()
        await message.answer(text='👉 Выбери периодичность авторепостинга',
                             reply_markup=keyboard)
        await state.set_state(PostState.wait_schedule_time.state)

    @staticmethod
    async def set_post_shedule_time(call: types.CallbackQuery, state: FSMContext):
        """Set post schedule time"""
        schedule_period = call.data.split('schedule_period_')[1]
        await state.update_data(schedule_period=schedule_period)
        await call.message.edit_text("👉 Введи время поста в формате hh:mm (например: 9:00")
        await state.set_state(PostState.wait_schedule_approve_finish.state)

    @staticmethod
    async def confirm_post_schedule(message: types.Message, state: FSMContext):
        """Finish set schedule time"""
        if not aux_funcs.check_time_format(message.text):
            await message.answer(
                "⚠ Неверный формат времени для автопостинга. Введи время формате hh:mm (например: 9:00")
            return
        await state.update_data(schedule_time=message.text)
        user_data = await state.get_data()
        keyboard = markups.get_shedule_confirmation_menu()
        if user_data.get('post_photo_id'):
            await message.answer_photo(
                photo=user_data.get('post_photo_id'),
                caption=f"🏞 изображение 👆\n"
                        f"📝 текст: {user_data.get('post_text')}\n"
                        f"⏳ периодичность: {user_data.get('schedule_period')}\n"
                        f"🕔 время: {user_data.get('schedule_time')}",
                reply_markup=keyboard
            )
        else:
            await message.answer(
                text=f"📝 текст: {user_data.get('post_text')}\n"
                     f"⏳ периодичность: {user_data.get('schedule_period')}\n"
                     f"🕔 время: {user_data.get('schedule_time')}",
                reply_markup=keyboard
            )
        await state.set_state(PostState.wait_schedule_set_finish.state)

    @staticmethod
    async def set_post_schedule(call: types.CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        post_controller.db_write_post_data(user_data)
        await call.message.answer('👌 Пост успешно добавлен в расписание')
        await state.finish()

    def register_handlers(self, dp: Dispatcher):
        """Register handlers"""
        dp.register_message_handler(self.add_post_content, commands='setpost',
                                    state='*')
        dp.register_callback_query_handler(self.edit_post_content, text='schedule_cancel', state='*')
        dp.register_message_handler(self.set_post_schedule_period, content_types=['photo', 'text'],
                                    state=PostState.wait_schedule_period)
        dp.register_callback_query_handler(self.set_post_shedule_time, Text(contains='schedule_period_'),
                                           state=PostState.wait_schedule_time)
        dp.register_message_handler(self.confirm_post_schedule, content_types='text',
                                    state=PostState.wait_schedule_approve_finish)
        dp.register_callback_query_handler(self.set_post_schedule, text='schedule_approve',
                                           state=PostState.wait_schedule_set_finish)
