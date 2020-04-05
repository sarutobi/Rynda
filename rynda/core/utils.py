# -*- coding: utf-8 -*-
#  import dns.resolver

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


def validate_email_domain(email):
    if email != '':
        domain = email.split('@')[1]
        #  dns.resolver.query(domain, 'MX')


def get_client_ip(request):
    """ Get remote client IP.

    Getting from Froide project https://github.com/stefanw/froide
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
