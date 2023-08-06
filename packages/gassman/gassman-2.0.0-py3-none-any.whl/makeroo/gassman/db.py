import sys
import logging
from datetime import timedelta

from pymysql import connect
from pymysql.err import OperationalError

from tornado.ioloop import PeriodicCallback

from .. import loglib
from .sql import SqlFactory


logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, conn_args, db_check_interval: timedelta, sql_factory: SqlFactory, notify_service):
        self.conn_args = conn_args
        self.db_check_interval = db_check_interval.total_seconds() * 1000  # milliseconds
        self.conn = None
        self.sql_factory = sql_factory
        self.notify_service = notify_service

    def connection(self):
        if self.conn is None:
            self._connect()

        return self.conn

    def _connect(self):
        if self.conn is not None:
            try:
                self.conn.close()
                self.conn = None
            except:
                pass

        self.conn = connect(**self.conn_args)

        PeriodicCallback(self._check_conn, self.db_check_interval).start()

    def _check_conn(self):
        try:
            try:
                with self.conn.cursor() as cur:
                    cur.execute(self.sql_factory.connection_check())
                    cur.fetchall()

            except OperationalError as e:
                if e.args[0] == 2013:
                    # pymysql.err.OperationalError: (2013, 'Lost connection to MySQL server during query')
                    # provo a riconnettermi
                    logger.warning('mysql closed connection, reconnecting')
                    self.connect()

                else:
                    raise

        except:
            etype, evalue, tb = sys.exc_info()
            logger.fatal('db connection failed: cause=%s/%s', etype, evalue)

            self.notify_service.notify(
                subject='[FATAL] No db connection',
                body='Connection error: %s/%s.\nTraceback:\n%s' % (etype, evalue, loglib.TracebackFormatter(tb)),
            )


def annotate_cursor_for_logging(cur):
    m = cur.execute

    def logging_execute(stmt, *args):
        logm = logger.debug if stmt.upper().strip().startswith('SELECT') else logger.info
        logm('SQL: %s / %s', stmt, args)
        m(stmt, *args)

    cur.execute = logging_execute
