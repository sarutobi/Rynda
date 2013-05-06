# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from post_office import mail


def send_templated_email(template_name, user_list):
    for u in user_list:
        mail.send(
            recipients=[u.email],
            sender='iva@srdu.ru',
            template=template_name,
            context={'user': u},
            priority=3
        )
