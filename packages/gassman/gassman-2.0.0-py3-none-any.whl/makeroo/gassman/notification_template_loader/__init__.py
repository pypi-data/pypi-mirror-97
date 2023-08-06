def main():
    # command line parsing

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--template-dir", help="path to templates directory")

    parser.add_argument('--db-host', default='db')
    parser.add_argument('--db-port', type=int, default=3306)
    parser.add_argument('--db-user', default='mysql')
    parser.add_argument('--db-password', default='example')
    parser.add_argument('--db-name', default='gassman')

    args = parser.parse_args()

    # logging setup

    import logging

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    # validate cli args

    import sys
    from os.path import isdir

    if args.template_dir is None:
        logger.error('missing template dir')
        sys.exit(1)

    if not isdir(args.template_dir):
        logger.error('template dir is not a directory')
        sys.exit(1)

    from ..db import annotate_cursor_for_logging

    from ..sql import SqlFactory

    sql_factory = SqlFactory()

    from ..db import Connection

    db = Connection(
        conn_args=dict(
            host=args.db_host,
            port=args.db_port,
            user=args.db_user,
            passwd=args.db_password,
            db=args.db_name,
            charset='utf8',
        ),
        db_check_interval=0,
        sql_factory=sql_factory,
        notify_service=None,
    )

    # perform work

    from os import listdir
    from os.path import join, isfile

    for f in listdir(args.template_dir):
        fp = join(args.template_dir, f)

        if not isfile(fp):
            logger.debug('skipping %s', f)

        with open(fp, 'rb') as fh:
            tpl = fh.read()

        with db.connection().cursor() as cur:
            annotate_cursor_for_logging(cur)

            q, a = db.sql_factory.template(f)
            cur.execute(q, a)

            if cur.fetchone() is None:
                q, a = db.sql_factory.template_insert(f, tpl)
                cur.execute(q, a)
                logger.info('new template %s', f)
            else:
                q, a = db.sql_factory.template_update(f, tpl)
                cur.execute(q, a)
                logger.info('updated template %s', f)
