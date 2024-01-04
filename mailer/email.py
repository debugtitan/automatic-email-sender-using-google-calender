import os
import smtplib
import ssl
from email import charset as Charset
from email.mime.text import MIMEText
from email.utils import formatdate
from jinja2 import Template

from mailer.config import AppConfig, BASE_DIR


class EmailClient(AppConfig):
    """Email Client"""

    __slots__ = ("subject", "body", "to", "bcc", "extra_headers")
    content_subtype = "plain"
    mixed_subtype = "mixed"
    encoding = Charset.Charset("utf-8")

    def __init__(self, subject: str, message: str, to=None, bcc=None,button_text="Follow Me",link=None):
        super().__init__()
        self.subject = subject
        self.body = message
        self.to = to
        self.bcc = bcc
        self.button = button_text
        self.link = link if link else "https://github.com/debugtitan"
        self.extra_headers = {}

    def _set_jinja(self):
        template_path = os.path.join(BASE_DIR, 'mail.html')
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()

    def _render_html_template(self):
        jinja_template = Template(self._set_jinja())
        return jinja_template.render(
            subject = self.subject,
            body = self.body,
            names = self.bcc,
            link = self.link,
            button = self.button
        )

    def _set_message(self):
        html_content = self._render_html_template()
        msg = MIMEText(html_content, 'html', self.encoding)
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
        if values:
            try:
                value = self.extra_headers[header]
            except KeyError:
                value = ", ".join(str(v) for v in values)
            msg[header] = value

    def _send_mail(self):
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
