from datetime import datetime

import pytz
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def check_user_last_login():
    users = User.objects.all()
    for user in users:
        if user.last_login:
            time_absence = datetime.now(
                pytz.timezone(settings.TIME_ZONE)) - user.last_login
        else:
            time_absence = datetime.now(
                pytz.timezone(settings.TIME_ZONE)) - user.date_joined
        if time_absence.days > 31:
            user.is_active = False
            user.save()
