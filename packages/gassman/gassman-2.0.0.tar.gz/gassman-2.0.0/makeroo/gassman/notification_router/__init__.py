def main():
    # command line parsing

    # logging setup

    import logging

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    from .config import Configuration

    cfg = Configuration()

    from ...asyncsmtp import Mailer

    mailer = Mailer(
        smtp_server=cfg.smtp_server,
        smtp_port=cfg.smtp_port,
        num_threads=cfg.smtp_num_threads,
        queue_timeout=cfg.smtp_queue_timeout,
        default_sender=cfg.smtp_sender,
    )

    from .. import sql

    sql_factory = sql.SqlFactory()

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
        notify_service=None,  # FIXME: restore: notify_service,
    )

    from ..notification_router.notification_router import NotificationRouterConfigurationManager

    notification_cfg = NotificationRouterConfigurationManager(
        db_conn,
        cfg.profile,
    )

    from ..tornadolib import DbLoader

    template_engine = DbLoader(
        db_conn,
    )

    from .notification_router import NotificationRouter

    notification_router = NotificationRouter(
        mailer=mailer,
        conn=db_conn,
        template_engine=template_engine,
        config=notification_cfg,
    )

    logger.info('Notification Router running...')

    from tornado.ioloop import IOLoop

    # FIXME: refactor into daemon / worker receiving tasks from rabbitmq
    IOLoop.current().run_sync(notification_router)

    logger.info('Notification Router completed.')
