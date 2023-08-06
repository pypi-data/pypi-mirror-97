import datetime
import logging

import pydoc
import json

from tornado.template import BaseLoader

from ...asyncsmtp import Mailer
from ..db import Connection, annotate_cursor_for_logging
from .notification_router import NotificationRouterConfigurationManager


logger = logging.getLogger(__name__)


def datetime_floor(t, rounding):
    """
    :param t: datetime instance
    :param rounding: seconds
    :return: rounded datetime instance
    """
    ut = t.timestamp()
    rt = ut - ut % rounding
    return datetime.datetime.fromtimestamp(rt)


class BaseReport:
    def __init__(self, generator, broadcaster):
        self.generator = generator
        self.broadcaster = broadcaster

    def __call__(self, router, cur):
        for event in self.generator.generate(router, cur):
            for address in self.broadcaster.broadcast(event, router, cur):
                router.send_email(
                    subject=event['subject'],
                    body=event['body'],
                    dest=address,
                )


class DaylyTransactionReport (BaseReport):
    class Generator:
        def generate(self, router, cur):
            pass

    class Broadcaster:
        def broadcast(self, msg, router, cur):
            pass

    # gira da cron tutte le sere (eg. alle 23)
    # TODO: daily
    pass


class WeeklyTransactionReport (BaseReport):
    # gira da cron tutte le settimane (eg. alle 23 di ogni sabato)
    # TODO: weekly
    pass


class NeverTransactionReport (BaseReport):
    # gira da cron tutte le sere (eg. alle 23)
    # TODO: never
    pass


class DeliveryDateReminder (BaseReport):
    class Generator:
        def __init__(self,
                     frequency,
                     advance,
                     rounding,
                     subject_if_covered,
                     body_if_covered,
                     subject_if_uncovered,
                     body_if_uncovered
                     ):
            """
            Struttura dei messaggi generati dal report (cfr. delivery_dates_for_notifications)
            id
            delivery_notes
            from_time
            to_time

            delivery_place

            csa
            csa_id
            address_first_line
            address_second_line
            address_description
            address_zip_code
            city

            people
              shift_role
              person_id
              first_name
              middle_name
              last_name
              contacts
                contact_address
                contact_kind



            :param frequency: (eg. 2 ore): giro alle 6am, 8am...
            :param advance: (eg. 6 ore): notifico dalle 12am alle 2pm...
            :param rounding: int, secondi (eg. 1 ora=3600): se giro alle 6:01, in realtà faccio finta di essere partito
                             alle 6 esatte
            :param fetch_covered: considera i turni coperti
            :param fetch_uncovered: considera i turni scoperti
            """
            self.frequency = datetime.timedelta(seconds=frequency)
            self.advance = datetime.timedelta(seconds=advance)
            self.rounding = rounding
            self.fetch_covered = subject_if_covered is not None
            self.fetch_uncovered = subject_if_uncovered is not None
            self.subject_if_covered = subject_if_covered
            self.subject_if_uncovered = subject_if_uncovered
            self.body_if_covered = body_if_covered
            self.body_if_uncovered = body_if_uncovered

        def generate(self, router, cur):
            now = datetime.datetime.utcnow()
            t0 = datetime_floor(now, self.rounding)
            tstart = t0 + self.advance
            tend = tstart + self.frequency
            q, a = router.sql.delivery_dates_for_notifications(
                tstart,
                tend,
                self.fetch_covered,
                self.fetch_uncovered
            )
            cur.execute(q, a)
            msgs = {}
            for msg in router.sql.iter_objects(cur):
                real_msg = msgs.setdefault(msg['id'], msg)
                people = real_msg.setdefault('people', {})
                person = people.setdefault(msg['person_id'], msg)
                contacts = person.setdefault('contacts', [])
                if person['contact_kind'] is not None:
                    contacts.append([person['contact_kind'], person['contact_address']])
            for msg in msgs.values():
                covered = msg['shift_role'] is not None
                subject = router.template(
                    self.subject_if_covered if covered else
                    self.subject_if_uncovered,
                    msg
                )
                body = router.template(
                    self.body_if_covered if covered else
                    self.body_if_uncovered,
                    msg
                )
                yield {
                    'message': msg,
                    'subject': subject,
                    'body': body
                }

    class Broadcaster:
        def __init__(self, notify_all):
            """
            :param notify_all: solo delivery_place o unknown / considera tutti
            :return:
            """
            self.notify_all = notify_all

        def broadcast(self,fmtmsg, router, cur):
            msg = fmtmsg['message']
            q, a = router.sql.people_index(
                msg['csa_id'],
                None,
                -1 if self.notify_all else msg['delivery_place_id'],
                None,
                False,
                -1,
                -1,
                None
            )
            cur.execute(q, a)
            pids = [row[0] for row in cur.fetchall()]
            q, a = router.sql.people_addresses(pids, router.sql.Ck_Email)
            cur.execute(q, a)
            return [row[1] for row in cur.fetchall()]


class NotificationRouter:
    def __init__(self, mailer: Mailer, conn: Connection, template_engine: BaseLoader, config: NotificationRouterConfigurationManager):
        self.mailer = mailer
        self.conn = conn
        self.template_engine = template_engine
        self.config = config

    def __call__(self):
        for report in self.config.configuration():
            self._process_report(report)

    def _process_report(self, report):
        with self.conn.connection().cursor() as cur:
            annotate_cursor_for_logging(cur)
            report(self, cur)

    def template(self, templ_name, namespace):
        templ = self.template_engine.load(templ_name)
        return templ.generate(**namespace)

    def send_email(self, subject, body, dest, reply_to=None):
        s = subject.decode('UTF-8')
        b = body.decode('UTF-8')
        if self.mailer is None:
            logger.info('SMTP not configured, mail not sent: dest=%s, subj=%s\n%s', dest, subject, body.decode('utf-8'))
        else:
            self.mailer.send(
                receivers=dest,
                subject=s,
                body=b,
                reply_to=reply_to,
            )


class ClassNotFound(Exception):
    pass


class NotificationRouterConfigurationManager:
    def __init__(self, conn: Connection, profile):
        self.conn = conn
        self.profile = profile

    def configuration(self):
        r = []

        with self.conn.connection().cursor() as cur:
            q, a = self.conn.sql.reports(self.profile)

            cur.execute(q, a)

            for cfg in self.conn.sql.iter_objects(cur):
                generator = self.instance(
                    cfg['generator'],
                    cfg['g_config']
                )
                broadcaster = self.instance(
                    cfg['broadcaster'],
                    cfg['b_config']
                )
                report = self.instance(
                    cfg['report'],
                    generator=generator,
                    broadcaster=broadcaster,
                )

                logger.debug('loaded report: %s', cfg['report'])

                r.append(report)

        return r

    @staticmethod
    def instance(class_name, class_config=None, **kwargs):
        cls = pydoc.locate(class_name)
        if cls is None:
            raise ClassNotFound(class_name)
        if class_config is None:
            cfg = kwargs
        else:
            cfg = json.loads(class_config)  # può lanciare json.decoder.JSONDecodeError, TypeError (se None)
            cfg.update(kwargs)
        o = cls(**cfg)  # può lanciare TypeError
        return o
