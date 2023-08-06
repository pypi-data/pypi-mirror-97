"""
Created on 18/mar/2014

@author: makeroo
"""

def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--db-host', default='db')
    parser.add_argument('--db-port', type=int, default=3306)
    parser.add_argument('--db-user', default='mysql')
    parser.add_argument('--db-password', default='example')
    parser.add_argument('--db-name', default='gassman')

    args = parser.parse_args()

    import pymysql

    conn = pymysql.connect(
        host=args.db_host,
        port=args.db_port,
        user=args.db_user,
        passwd=args.db_password,
        db=args.db_name,
        charset='utf8'
    )

    import uuid

    with conn as cur:
        cur.execute('SELECT id FROM person where rss_feed_id IS NULL')

        for pid in [l[0] for l in cur]:
            cur.execute(
                'UPDATE person SET rss_feed_id=%s WHERE id=%s', [
                    str(uuid.uuid4()),
                    pid
            ])
