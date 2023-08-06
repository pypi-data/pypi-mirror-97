def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--action', help="action: one of remove, count, gc")

    parser.add_argument('-k', '--kind', help='contact kind: one of T, M, E, F, I, N, +, P, W')
    parser.add_argument('-t', '--type', help='contact type')

    #parser.add_argument('-h', '--help', action='store_true', help='use with -a to obtain action help')

    parser.add_argument('--db-host', default='db')
    parser.add_argument('--db-port', type=int, default=3306)
    parser.add_argument('--db-user', default='root')
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
        charset='utf8',
    )

    import sys
    import importlib

    if args.action is None:
        print('specify an action')
        return

    try:
        command_module = importlib.import_module(f'makeroo.gassman.contacts_fixer.{args.action}')

        command = getattr(command_module, 'Command')()

    except ImportError:
        print('illegal action')

        sys.exit(1)

    with conn.cursor() as cur:
        command.run(cur, args)


if __name__ == '__main__':
    main()
