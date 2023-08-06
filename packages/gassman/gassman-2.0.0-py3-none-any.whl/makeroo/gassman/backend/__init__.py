"""
Created on 01/mar/2014

@author: makeroo
"""


def main():
    from logging.config import dictConfig

    from . import gassman_settings as settings

    dictConfig(settings.LOG)

    from .config import Configuration

    cfg = Configuration()

    from ...asyncsmtp import Mailer

    if cfg.smtp_server == '':
        mailer = None

    else:
        mailer = Mailer(
            smtp_server=cfg.smtp_server,
            smtp_port=cfg.smtp_port,
            num_threads=cfg.smtp_num_threads,
            queue_timeout=cfg.smtp_queue_timeout,
            default_sender=cfg.smtp_sender,
        )

    from ..notification_service import NotifyService

    notify_service = NotifyService(
        mailer,
        cfg.devops_email
    )

    from ..sql import SqlFactory

    sql_factory = SqlFactory()

    from ..db import Connection

    db_conn = Connection(
        conn_args=dict(
            host=cfg.db_host,
            port=cfg.db_port,
            user=cfg.db_user,
            passwd=cfg.db_password,
            db=cfg.db_name,
            charset='utf8',
        ),
        db_check_interval=cfg.db_check_interval,
        sql_factory=sql_factory,
        notify_service=notify_service,
    )

    from .auth import AuthenticationSessionManager

    asm = AuthenticationSessionManager(
        nonce_duration=cfg.nonce_duration,
    )

    from ...tornadolib import PackagedTemplateLoader

    template_loader = PackagedTemplateLoader(__name__)

    from .app import GassmanWebApp

    application = GassmanWebApp(
        conn=db_conn,
        notify_service=notify_service,
        template_loader=template_loader,
        configuration=cfg,
        authentication_session_manager=asm,
    )

    application.listen(cfg.http_port)

    from logging import getLogger

    logger = getLogger(__name__)

    logger.info('GASsMAN web server up and running...')

    from tornado.ioloop import IOLoop

    IOLoop.current().start()
