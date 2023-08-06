from argparse import Namespace
from pymysql.cursors import Cursor


class Command:
    def run(self, cur: Cursor, args: Namespace) -> None:
        cond = ''
        qargs = []
        sep = ' WHERE'

        if args.kind:
            cond += f'{sep} kind=%s'
            qargs.append(args.kind)
            sep = ' AND'

        if args.type:
            cond += f'{sep} contact_type=%s'
            qargs.append(args.type)

        q = f'SELECT id FROM contact_address{cond}'

        cur.execute(q, qargs)

        to_be_deleted = {
            row[0]
            for row in cur.fetchall()
        }

        if not to_be_deleted:
            print('nothing to remove')
            return

        cur.execute('DELETE FROM person_contact WHERE address_id IN %s', [to_be_deleted])
        cur.execute('DELETE FROM contact_address WHERE id IN %s', [to_be_deleted])

        print(f'removed {cur.rowcount} contacts')
