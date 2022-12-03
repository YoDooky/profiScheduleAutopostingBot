from datetime import datetime
from typing import List, Dict
from database.models.utils import dbcontrol
from typing import Dict

from config.db_config import POSTS_TABLE
from telegram import vars_global


def db_write_post_data(user_data: Dict):
    """Write post schedule and text to DB"""
    dbcontrol.insert_db(POSTS_TABLE, user_data)
    vars_global.update_schedule[0] = True


def db_read_post_data() -> List[Dict]:
    """Read data from post table"""
    data_columns = ['id', 'post_photo_id', 'post_text', 'schedule_period', 'schedule_time']
    table_data = dbcontrol.fetchall(POSTS_TABLE, data_columns)
    return table_data


def db_del_post_data(post_id: int):
    data = {'id': post_id}
    dbcontrol.delete(POSTS_TABLE, data)
    vars_global.update_schedule[0] = True
