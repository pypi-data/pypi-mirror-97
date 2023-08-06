import logging


logger = logging.getLogger(__name__)


class NotifyService:
    def __init__(self, mailer, default_receiver):
        self.mailer = mailer
        self.default_receiver = default_receiver

    def notify(self, subject, body, receivers=None, reply_to=None):
        if self.mailer is None:
            logger.info('SMTP not configured, mail not sent: dest=%s, subj=%s\n%s', receivers, subject, body)
        else:
            self.mailer.send(
                receivers=receivers or self.default_receiver,
                subject='[GASsMan] %s' % subject,
                body=body,
                # sender=None,
                reply_to=reply_to,
            )
