import smtplib
import ssl
from mailer.config import AppConfig


class EmailClient(AppConfig):
    """ Email Client"""

    __slots__ = ("subject","message","recipient_list")
    def __init__(self, subject: str, message: str, recipient_list: list[str]):
        """
        Initialize the EmailClient with the provided subject, message, and recipient list.

        :param subject: Subject of the email.
        :param message: Body of the email.
        :param recipient_list: List of email addresses to send the email to.
        """

        super().__init__()
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list

    def _send_mail(self):
        """ send email """

        server = smtplib.SMTP(self.host, self.port)
        if self.use_tls:
            server.starttls(context=ssl.create_default_context())
        if self.email and self.password:
            server.login(self.email, self.password)

        server.sendmail(self.email, self.recipient_list, self.message)
            
        