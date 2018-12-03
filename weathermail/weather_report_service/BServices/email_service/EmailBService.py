import logging

from django.core.mail import send_mail


class EmailBService(object):
    """
        Email Service for sending out emails
    """
    @staticmethod
    def send_html_message(
            subject,
            recipient,
            plaintext_message,
            html_message,
            bcc=None,
            sender=None,):
        """
            Email service to send html emails.

            @type subject: str
            @type recipient: str
            @type plaintext_message: str
            @type html_message: str
            @type bcc: str
            @type sender: None or str
        """

        assert isinstance(subject, str), type(subject)
        assert isinstance(recipient, str), type(recipient)
        assert recipient
        assert isinstance(plaintext_message, str), type(plaintext_message)
        assert isinstance(html_message, str), type(html_message)
        assert bcc is None or isinstance(bcc, str), type(bcc)
        assert sender is None or isinstance(sender, str), type(sender)

        recipient_list = [recipient]
        if bcc:
            recipient_list.append(bcc)

        send_mail(
            subject=subject,
            message=plaintext_message,
            html_message=html_message,
            from_email=sender,
            recipient_list=recipient_list,
            fail_silently=False
        )

    __LOGGER = logging.getLogger(__name__)
    """ logger for this class """
