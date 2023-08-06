def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Transaction date consistency validator'
    )

    parser.add_argument('--verbose', '-v', action='count', default=0, help='increment verbosity')

    parser.add_argument('--fix', action='store_true', help='fix dates')

    parser.add_argument('--db-host', default='db')
    parser.add_argument('--db-port', type=int, default=3306)
    parser.add_argument('--db-user', default='mysql')
    parser.add_argument('--db-password', default='example')
    parser.add_argument('--db-name', default='gassman')

    args = parser.parse_args()

    import logging

    logging.basicConfig(level=max(logging.ERROR - 10 * args.verbose, logging.DEBUG))

    from ..sql import SqlFactory

    sql_factory = SqlFactory()

    from ..db import Connection

    db_conn = Connection(
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

    from .model import CheckTransactionDate

    app = CheckTransactionDate(db_conn, logging)

    app.collect()

    app.analyze()

    app.sql_report(args.fix)
