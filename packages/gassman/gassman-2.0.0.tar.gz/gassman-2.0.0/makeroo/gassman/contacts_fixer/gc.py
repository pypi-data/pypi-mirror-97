from argparse import Namespace
from pymysql.cursors import Cursor


class Command:
    def run(self, cur: Cursor, args: Namespace) -> None:
        #if args.help:
        #    print('remove addresses not referred by any person')
        #    return

        cur.execute('SELECT a.id, COUNT(pc.id) FROM contact_address a LEFT JOIN person_contact pc ON pc.address_id = a.id GROUP BY a.id', [])

        to_be_removed = set()

        for address_id, use_count in cur.fetchall():
            if use_count == 0:
                to_be_removed.add(address_id)

        if not to_be_removed:
            print('no contact to remove')
            return

        print(f'{len(to_be_removed)} unused contacts to remove')

        cur.execute('DELETE FROM contact_address WHERE id IN %s', to_be_removed)
