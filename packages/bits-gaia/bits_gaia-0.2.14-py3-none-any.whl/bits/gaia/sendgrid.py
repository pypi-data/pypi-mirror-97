# -*- coding: utf-8 -*-
"""SendGrid class for Gaia."""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import Email
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import To


class SendGrid:
    """SendGrid class."""

    def __init__(self, api_key):
        """Initialize a class instance."""
        self.api_key = api_key
        self.sendgrid = SendGridAPIClient(api_key=api_key)

    def send_text_email(self, from_email, to_emails, subject, content):
        """Send a text email with sendgrid."""
        message = Mail(
            from_email=Email(from_email),
            to_emails=To(to_emails),
            subject=subject,
            plain_text_content=Content("text/plain", content),
        )
        return self.sendgrid.client.mail.send.post(request_body=message.get())
