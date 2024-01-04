import smtplib
import ssl
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    def _set_message(self):
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = self.email
        msg["To"] = ", ".join(self.recipient_list)
        msg.set_content(self.message)
        return msg

    def _send_mail(self):
        """ send email """
        try:
            server = smtplib.SMTP(self.host, self.port) if self.use_tls else smtplib.SMTP_SSL(self.host, self.port)
            if self.use_tls:
                server.starttls(context=ssl.create_default_context())
            if self.email and self.password:
                server.login(self.email, self.password)

            server.send_message(self._set_message())
            server.close()
        except smtplib.SMTPServerDisconnected:
            return
        except smtplib.SMTPException:
            return
        
            
        