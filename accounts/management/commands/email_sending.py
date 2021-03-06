import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand

from accounts.models import *


def get_contact_admin_list():
    admin_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
    Contact.objects.filter(admin_time__gte=admin_time, status=0).update(status=1)
    contacts = Contact.objects.filter(admin_time__gte=admin_time, status=1)
    for contact in contacts:
        email_sending("User email to Admin", contact.description, "admin@gmail.com")
    return True


def get_contact_user_list():
    admin_time = datetime.datetime.now() + datetime.timedelta(minutes=20)
    Contact.objects.filter(user_time__gte=admin_time, status=1).update(status=2)
    contacts = Contact.objects.filter(user_time__gte=admin_time, status=2)
    contacts = contacts.values_list("email", flat=True)
    email_sending("Admin mail to user", "Admin will contact you to shortly", list(contacts))
    return True


def email_sending(subject, message, to_email):
    file = "{}/google.pdf".format(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email])
    with open(file, 'rb') as f:
        mail.attach(f.name, f.read(), f.name)
    mail.send()


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True > False:
            get_contact_admin_list()
            get_contact_user_list()
