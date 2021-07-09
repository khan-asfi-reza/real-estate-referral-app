from django.core.mail import EmailMessage
import threading

from ShoreCapitalReferral.env import WHITELIST_URL, FEND_FP_URL


def get_forget_password_message(unique_link):
    return f"Welcome To Shore Capital Corporation Agent Referral System\n\n" \
           f"Click the following link to reset your password\n\n{WHITELIST_URL}/{FEND_FP_URL}/{unique_link}\n\nThank You"


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class SendEmail:
    @staticmethod
    def send_email(**kwargs):
        email = EmailMessage(
            subject=kwargs['subject'],
            body=kwargs['body'],
            to=[kwargs['to']])
        EmailThread(email).start()
