from aiogram import Bot
import aioschedule
import asyncio

from database.controllers import post_controller
from config.bot_config import TARGET_CHANNEL_ID
from telegram import vars_global


class Schedule:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_post(self, text: str, photo_id: str):
        """Send post by shedule"""
        if photo_id != 'None':
            await self.bot.send_photo(chat_id=TARGET_CHANNEL_ID, photo=photo_id, caption=text)
            return
        await self.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=text)

    async def scheduler(self):
        """Shedule loop"""
        self.update_post_schedule()
        while True:
            if vars_global.update_schedule[0]:
                self.update_post_schedule()
                vars_global.update_schedule[0] = False
            await aioschedule.run_pending()
            await asyncio.sleep(1)

    def update_post_schedule(self):
        """Make new shedule"""
        print('[SHEDULE] Updating schedule...')
        aioschedule.clear()
        posts = post_controller.db_read_post_data()
        for post in posts:
            if post.get('schedule_period') == 'everyday':
                aioschedule.every().day.do(self.send_post, text=post.get('post_text'),
                                           photo_id=post.get('post_photo_id'))
            elif post.get('schedule_period') == 'monday':
                aioschedule.every().monday.do(self.send_post, text=post.get('post_text'),
                                              photo_id=post.get('post_photo_id'))
            elif post.get('schedule_period') == 'tuesday':
                aioschedule.every().tuesday.do(self.send_post, text=post.get('post_text'),
                                               photo_id=post.get('post_photo_id'))
            elif post.get('schedule_period') == 'wednesday':
                aioschedule.every().wednesday.do(self.send_post, text=post.get('post_text'),
                                                 photo_id=post.get('post_photo_id'))
            elif post.get('schedule_period') == 'thursday':
                aioschedule.every().thursday.do(self.send_post, text=post.get('post_text'),
                                                photo_id=post.get('post_photo_id'))
            elif post.get('schedule_period') == 'friday':
                aioschedule.every().friday.do(self.send_post, text=post.get('post_text'),
                                              photo_id=post.get('post_photo_id'))
            elif post.get('schedule_period') == 'saturday':
                aioschedule.every().saturday.do(self.send_post, text=post.get('post_text'),
                                                photo_id=post.get('post_photo_id'))
            elif post.get('schedule_period') == 'sunday':
                aioschedule.every().sunday.do(self.send_post, text=post.get('post_text'),
                                              photo_id=post.get('post_photo_id'))
