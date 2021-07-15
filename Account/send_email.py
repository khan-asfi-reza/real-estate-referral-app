from django.core.mail import EmailMessage
import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from ShoreCapitalReferral.settings import WHITELIST_URL, FEND_FP_URL, EMAIL_HOST_USER


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
    def send_email(subject="", body="", to="", **kwargs):
        """
            param: subject: Email subject
            param: body: Email body
            param: to: param mail receiver
        """
        email = EmailMessage(
            subject=subject,
            body=body,
            to=[to])

        EmailThread(email).start()

    @staticmethod
    def send_html_email(template, subject="", body="", to="", **kwargs):
        """
            param: template: Email Template
            param: subject: Email subject
            param: body: Email body
            param: to: param mail receiver
        """
        # Gets HTML from template
        html_message = render_to_string(template, {'context': body})
        # Creates HTML Email
        msg = EmailMultiAlternatives(subject, from_email=EMAIL_HOST_USER, to=[to])
        # Send Email
        msg.attach_alternative(html_message, "text/html")
        EmailThread(msg).start()