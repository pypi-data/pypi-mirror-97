from argparse import Namespace
from pymysql.cursors import Cursor


class Command:
    def run(self, cur: Cursor, args: Namespace) -> None:
        cur.execute('SELECT kind, contact_type, COUNT(*) FROM contact_address GROUP BY kind, contact_type ORDER BY kind, contact_type', [])

        for kind, contact_type, count in cur.fetchall():
            print('{} {:<10}: {:>5}'.format(kind, contact_type or '', count))
