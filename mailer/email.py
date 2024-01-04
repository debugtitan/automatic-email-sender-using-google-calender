import smtplib
import ssl
from email import charset as Charset
from email.mime.text import MIMEText
from email.utils import formatdate

from mailer.config import AppConfig


class EmailClient(AppConfig):
    """ Email Client"""

    __slots__ = ("subject","message","recipient_list")
    content_subtype = "plain"
    mixed_subtype = "mixed"
    encoding = Charset.Charset("utf-8")
    def __init__(self, subject: str, message: str, to=None,bcc=None):
        
        super().__init__()
        self.subject = subject
        self.body = message
        self.to = to
        self.bcc = bcc
        self.extra_headers =  {}



    def _set_message(self):
        msg = MIMEText(self.body, self.content_subtype, self.encoding)
        msg["Subject"] = self.subject
        msg["From"] = self.extra_headers.get("From", self.email)
        self._set_list_header_if_not_empty(msg, "To", self.to)
        self._set_list_header_if_not_empty(msg, "Bcc", self.bcc)

        header_names = [key.lower() for key in self.extra_headers]
        if "date" not in header_names:
            msg["Date"] = formatdate(localtime=True)
        for name, value in self.extra_headers.items():
            if name.lower() != "from":  # From is already handled
                msg[name] = value
        return msg
    
    
    def _set_list_header_if_not_empty(self, msg, header, values):
        """
        Set msg's header, either from self.extra_headers, if present, or from
        the values argument.
        """
        if values:
            try:
                value = self.extra_headers[header]
            except KeyError:
                value = ", ".join(str(v) for v in values)
            msg[header] = value

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
        
            
        