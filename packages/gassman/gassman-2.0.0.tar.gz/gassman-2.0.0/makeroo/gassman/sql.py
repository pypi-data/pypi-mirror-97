"""
Created on 03/mar/2014

@author: makeroo
"""

from datetime import datetime
from typing import Any, Iterable, Optional, Union

from .. import jsonlib
from .i18n_utils import parse_decimal


SqlQuery = tuple[str, list[Any]]

Permission = int

TransactionType = str

TransactionLog = str

NotificationFrequency = str

ContactKind = str

OrderState = str

AccountState = str

AccountType = str

JsonObject = dict[str, Any]


class SqlFactory:
    # P_membership = 1
    P_canCheckAccounts : Permission = 2
    P_canAdminPeople : Permission = 3  # very low level!
    # P_canEnterDeposit = 4 # deprecated
    P_canEnterPayments : Permission = 5
    P_canManageTransactions : Permission = 6
    P_canEnterCashExchange : Permission = 7
    # P_canEnterWithdrawal = 8 # deprecated
    P_canViewContacts : Permission = 9
    P_canEditContacts : Permission = 10
    P_canGrantPermissions : Permission = 11
    P_canEditMembershipFee : Permission = 12
    P_csaEditor : Permission = 13
    P_canCloseAccounts : Permission = 14
    P_canManageShifts : Permission = 15
    P_canPlaceOrders : Permission = 16

    Tt_Deposit : TransactionType = 'd'          # deprecated,       READ ONLY
    Tt_Error : TransactionType = 'e'
    Tt_MembershipFee : TransactionType = 'f'    # pagamento quota,  P_canEditMembershipFee
    Tt_Generic : TransactionType = 'g'          # deprecated,       READ ONLY
    Tt_Payment : TransactionType = 'p'          # pagamento merce,  P_canEnterPayments
    Tt_PaymentExpenses : TransactionType = 'q'  # deprecated,       READ ONLY (conto EXPENSES invece di KITTY per le spese)
    # TODO 'r'
    Tt_Trashed : TransactionType = 't'          # cancellata,       P_canManageTransactions or isEditor
    Tt_Unfinished : TransactionType = 'u'
    Tt_Withdrawal : TransactionType = 'w'       # deprecated,       READ ONLY
    Tt_CashExchange : TransactionType = 'x'     # scambio contante, P_canEnterCashExchange
    Tt_AccountClosing : TransactionType = 'z'   # chiusura conto,   P_canCloseAccounts

    An_EveryMovement : NotificationFrequency = 'E'
    An_Dayly : NotificationFrequency = 'D'
    An_Weekly : NotificationFrequency = 'W'
    An_Never : NotificationFrequency = 'N'

    Ck_Telephone : ContactKind = 'T'
    Ck_Mobile : ContactKind = 'M'
    Ck_Email : ContactKind = 'E'
    Ck_Fax : ContactKind = 'F'
    Ck_Id : ContactKind = 'I'
    Ck_Nickname : ContactKind = 'N'
    Ck_GooglePlusProfile : ContactKind = '+'
    Ck_Photo : ContactKind = 'P'
    Ck_Web : ContactKind = 'W'

    Ckk = {
        Ck_Telephone,
        Ck_Mobile,
        Ck_Email,
        Ck_Fax,
        Ck_Id,
        Ck_Nickname,
        Ck_GooglePlusProfile,
        Ck_Photo,
    }

    Os_draft : OrderState = 'D'
    Os_open : OrderState = 'O'
    Os_closed : OrderState = 'C'
    Os_canceled : OrderState = 'T'
    Os_completed : OrderState = 'A'

    Oss = {
        Os_draft,
        Os_open,
        Os_closed,
        Os_canceled,
        Os_closed
    }

    transactionPermissions = {
        # Tt_Deposit: READ ONLY P_canEnterDeposit,
        Tt_Payment: P_canEnterPayments,
        Tt_CashExchange: P_canEnterCashExchange,
        # Tt_Withdrawal: READ ONLY P_canEnterWithdrawal,
        Tt_MembershipFee: P_canEditMembershipFee,
        # Tt_PaymentExpenses: READ ONLY P_canEnterPayments,
        # Tt_Generic: READ ONLY P_canCheckAccounts,
    }

    editableTransactionPermissions = set(transactionPermissions.values())

    deletableTransactions = {
        Tt_Generic,
        Tt_Deposit,
        Tt_Payment,
        Tt_CashExchange,
        Tt_Withdrawal,
        Tt_MembershipFee,
        Tt_PaymentExpenses,
    }

    editableTransactions = {
        # Tt_Generic,
        # Tt_Deposit,
        Tt_Payment,
        Tt_CashExchange,
        # Tt_Withdrawal,
        # Tt_Trashed,
        Tt_MembershipFee,
        # Tt_PaymentExpenses,
        # Tt_Unfinished,
    }

    As_Open : AccountState = 'O'
    As_Closing : AccountState = 'C'
    As_closeD : AccountState = 'D'
    As_Fusion_pending : AccountState = 'F'

    Tl_Added : TransactionLog = 'A'
    Tl_Deleted : TransactionLog = 'D'
    Tl_Modified : TransactionLog = 'M'
    Tl_Error : TransactionLog = 'E'

    Tn_kitty_deposit = 'kitty_deposit'
    Tn_account_closing = 'account_closing'

    At_Asset : AccountType = 'ASSET'  # persone
    At_Expense : AccountType = 'EXPENSE'  # spese
    At_Income : AccountType = 'INCOME'  # versamenti
    At_Kitty : AccountType = 'KITTY'  # kitty

    @staticmethod
    def account_owners(account_id: int) -> SqlQuery:
        return '''
SELECT p.first_name, p.middle_name, p.last_name, p.id, ap.from_date, ap.to_date
  FROM person p
  JOIN account_person ap ON ap.person_id=p.id
 WHERE ap.account_id=%s''', [
            account_id
        ]

    @staticmethod
    def account_has_open_owners(account_id: int) -> SqlQuery:
        return 'SELECT ap.id FROM account_person ap WHERE ap.account_id=%s AND ap.to_date IS NULL', [account_id]

    @staticmethod
    def check_date_against_account_ownerships(accounts: Iterable[int], date: datetime) -> SqlQuery:
        """
        Query to verify that transaction date is contained in account ownerships interval of new transaction.
        Date is valid if *no* rows are returned.

        :param accounts: Accounts involved in new transaction.
        :param date: Transaction date.
        :return: SQL query and its arguments array.
        """

        return '''
  SELECT account_id, count(person_id) AS x
    FROM account_person
   WHERE account_id IN %s AND from_date <= %s AND (to_date IS NULL OR to_date >= %s)
GROUP BY account_id
  HAVING x = 0;
''', [set(accounts), date, date]

    @staticmethod
    def check_date_against_account_ownerships_by_trans(trans_id: int, date: datetime) -> SqlQuery:
        """
        Query to verify that cancelation date is contained in account ownerships interval of deleted transaction.
        Date is valid if *no* rows are returned.

        :param trans_id: Transaction to be deleted.
        :param date: Cancelation date.
        :return: SQL query and its arguments array.
        """
        return '''
  SELECT l.id, l.account_id, BIT_OR( IF( ap.from_date <= %s AND (ap.to_date IS NULL OR ap.to_date >= %s), 1, 0 ) ) AS x
    FROM transaction t
    JOIN transaction_line l ON l.transaction_id=t.id
    JOIN account_person ap ON ap.account_id=l.account_id
   WHERE t.id = %s
GROUP BY l.id, l.account_id
  HAVING x = 0
''', [date, date, trans_id]

    @staticmethod
    def account_description(account_id: int) -> SqlQuery:
        return 'SELECT a.gc_name, c.name, c.id FROM account a JOIN csa c ON a.csa_id=c.id WHERE a.id=%s', [account_id]

    def count_account_movements(self, account_db_id: int, filter_by: Optional[str]) -> SqlQuery:
        q = '''
SELECT count(*)
 FROM transaction t
 JOIN transaction_line l ON l.transaction_id=t.id
 JOIN currency c ON c.id=t.currency_id
 WHERE t.modified_by_id IS NULL AND t.cc_type NOT IN (%s, %s) AND l.account_id=%s
     '''
        a = [self.Tt_Unfinished, self.Tt_Error, account_db_id]
        if filter_by:
            q += ' AND (l.description LIKE %s OR t.description LIKE %s)'
            a.extend([filter_by, filter_by])
        return q, a

    def account_movements(self, account_db_id: int, filter_by: Optional[str], from_line: Optional[int], to_line: Optional[int]) -> SqlQuery:
        q = '''
SELECT t.description, t.transaction_date, l.description, l.amount, t.id, c.symbol, t.cc_type
 FROM transaction t
 JOIN transaction_line l ON l.transaction_id=t.id
 JOIN currency c ON c.id=t.currency_id
 WHERE t.modified_by_id IS NULL AND t.cc_type NOT IN (%s, %s) AND l.account_id=%s
'''
        a = [self.Tt_Unfinished, self.Tt_Error, account_db_id]
        if filter_by:
            q += ' AND (l.description LIKE %s OR t.description LIKE %s)'
            a.extend([filter_by, filter_by])
        q += ' ORDER BY t.transaction_date DESC'
        if from_line is not None:
            q += ' LIMIT %s OFFSET %s'
            a.extend([to_line - from_line + 1, from_line])
        return q, a

    def account_amount(self, account_db_id: int, return_currency_id : bool = False) -> SqlQuery:
        q = 'SELECT SUM(l.amount), c.symbol'

        if return_currency_id:
            q += ', c.id'

        q += """ FROM transaction t
     JOIN transaction_line l ON l.transaction_id=t.id
     JOIN account a on l.account_id=a.id
     JOIN currency c ON c.id=a.currency_id
     WHERE t.modified_by_id IS NULL AND t.cc_type NOT IN (%s, %s) AND l.account_id=%s"""

        return q, [self.Tt_Unfinished, self.Tt_Error, account_db_id]

    accounts_index_order_by = [
        'p.first_name, p.last_name',
        'ta',
        'td desc',
    ]

    def accounts_index(self, csa_id: int, t: Optional[str], dp: Union[str, int], o: Optional[str], ex: bool, from_line: Optional[int], to_line: Optional[int], search_contact_kinds: Optional[Iterable[ContactKind]]):
        q = '''
SELECT p.id, p.first_name, p.middle_name, p.last_name, a.id,
       sum(l.amount) AS ta, c.symbol,
       MAX(t.transaction_date) AS td, a.membership_fee
  FROM '''
        a = []

        if t and search_contact_kinds:
            q += '''
  (SELECT p.*, group_concat(ca.address, ', ') AS contacts
     FROM person p
LEFT JOIN person_contact pc ON pc.person_id=p.id
LEFT JOIN contact_address ca ON ca.id=pc.address_id
    WHERE ca.kind IS NULL OR ca.kind in %s
 GROUP BY p.id) p'''
            a.append(set(search_contact_kinds))
        else:
            q += 'person p'

        q += '''
     JOIN account_person ap ON ap.person_id=p.id
     JOIN account a on ap.account_id=a.id
     JOIN currency c ON a.currency_id=c.id
LEFT JOIN transaction_line l ON l.account_id=a.id
LEFT JOIN transaction t ON t.id=l.transaction_id
    WHERE a.csa_id=%s'''
        a.append(csa_id)

        if not ex:
            q += ' AND ap.to_date IS NULL'

        q += ''' AND t.modified_by_id IS NULL AND (t.cc_type IS NULL OR t.cc_type NOT IN (%s, %s))'''
        a.extend([self.Tt_Unfinished, self.Tt_Error])

        if t:
            q += ' AND (p.first_name LIKE %s OR p.middle_name LIKE %s OR p.last_name LIKE %s'
            a.extend([t, t, t])
            if search_contact_kinds:
                q += ' OR p.contacts LIKE %s)'
                a.append(t)
            else:
                q += ')'

        dp = int(dp)
        if dp == -2:
            q += " AND p.default_delivery_place_id IS NULL"
        elif dp != -1:
            q += " AND p.default_delivery_place_id=%s"
            a.append(dp)

        q += ' GROUP BY p.id, a.id'

        if o:
            q += ' ORDER BY ' + o

        if from_line != -1:
            q += ''' LIMIT %s OFFSET %s'''
            a.extend([
                to_line - from_line + 1,
                from_line
            ])

        return q, a

    @staticmethod
    def check_user(user_id: str, authenticator: str, kind: ContactKind) -> SqlQuery:
        return '''
SELECT p.id, p.first_name, p.middle_name, p.last_name, p.rss_feed_id
  FROM contact_address c
  JOIN person_contact pc ON c.id=pc.address_id
  JOIN person p ON p.id=pc.person_id
 WHERE c.kind=%s AND c.contact_type=%s AND c.address=%s''', [
            kind, authenticator, user_id
        ]

    @staticmethod
    def create_contact(addr: str, kind: ContactKind, contact_type: str) -> SqlQuery:
        return 'INSERT INTO contact_address (address, kind, contact_type) VALUES (%s,%s,%s)', [
            addr, kind, contact_type
        ]

    @staticmethod
    def create_person(first: str, middle: str, last: str) -> SqlQuery:
        return 'INSERT INTO person (first_name, middle_name, last_name) VALUES (%s,%s,%s)', [first, middle, last]

    @staticmethod
    def assign_rss_feed_id(person_id: int, rss_feed_id: str) -> SqlQuery:
        return 'UPDATE person SET rss_feed_id=%s WHERE id=%s', [rss_feed_id, person_id]

    @staticmethod
    def assign_contact(contact: int, person: int) -> SqlQuery:
        return 'INSERT INTO person_contact (person_id, address_id) VALUES (%s, %s)', [person, contact]

    # @staticmethod
    # def has_accounts(pid):
    #    return 'SELECT count(*) FROM account_person WHERE person_id=%s AND to_date IS NULL', [pid]

    @staticmethod
    def find_open_accounts(pid: int, csa: int) -> SqlQuery:
        return '''
SELECT b.id, b.currency_id
  FROM account b
  JOIN account_person ap ON ap.account_id=b.id
 WHERE ap.person_id=%s AND b.csa_id=%s AND ap.to_date IS NULL
        ''', [pid, csa]

    @staticmethod
    def has_account(pid: int, acc_id: int) -> SqlQuery:
        return 'SELECT count(*) FROM account_person WHERE person_id=%s AND account_id=%s AND to_date IS NULL', [
            pid, acc_id
        ]

    @staticmethod
    def has_or_had_account(pid: int, acc_id: int) -> SqlQuery:
        return 'SELECT count(*) FROM account_person WHERE person_id=%s AND account_id=%s', [pid, acc_id]

    # def find_visible_permissions (person_id):
    #    return 'SELECT id, name, description FROM permission p WHERE visibility <= (SELECT MAX(p.visibility)
    #  FROM permission p JOIN permission_grant g ON p.id=g.perm_id JOIN person u ON g.person_id=u.id WHERE u.id=%s)
    #  ORDER BY visibility, ord, name', [person_id]

    @staticmethod
    def find_user_permissions(person_id: int, csa_id: int) -> SqlQuery:
        return '''
SELECT g.perm_id
  FROM person u
  JOIN permission_grant g ON g.person_id=u.id
 WHERE u.id=%s AND g.csa_id=%s''', [person_id, csa_id]
        # return 'SELECT p.id FROM person u JOIN permission_grant g ON g.person_id=u.id
        #  JOIN permission p ON g.perm_id=p.id WHERE u.id=%s', [person_id]

    @staticmethod
    def find_user_csa(person_id: int) -> SqlQuery:
        return '''
SELECT c.id, c.name, ap.to_date IS NULL AS "active_member"
  FROM account_person ap
  JOIN account a ON a.id=ap.account_id
  JOIN csa c ON c.id=a.csa_id
 WHERE ap.person_id=%s''', [person_id]

    # def find_user_accounts (person_id):
    #    return 'SELECT a.csa_id, a.id, ap.from_date, ap.to_date FROM account_person ap
    #  JOIN account a ON ap.account_id = a.id WHERE ap.person_id = %s ORDER BY a.csa_id, ap.from_date', [person_id]

    # TODO: si ripristina se si fa la pagina di associazione conto...
    # def find_users_without_account ():
    #    return 'SELECT id, first_name, middle_name, last_name FROM person WHERE current_account_id IS NULL'

    @staticmethod
    def update_last_login(person_id: int, login_time: datetime) -> SqlQuery:
        return 'UPDATE person SET last_login=%s WHERE id=%s', [login_time, person_id]

    @staticmethod
    def update_last_visit(person_id: int, visit_time: datetime) -> SqlQuery:
        return 'UPDATE person SET last_visit=%s WHERE id=%s', [visit_time, person_id]

    def check_membership_by_kitty(self, person_id: int, acc_id: int) -> SqlQuery:
        return '''
SELECT COUNT(*)
  FROM account kitty
  JOIN account useraccount ON kitty.csa_id=useraccount.csa_id
  JOIN account_person ap   ON ap.account_id=useraccount.id
 WHERE kitty.id=%s AND ap.person_id=%s AND kitty.gc_type=%s and ap.to_date IS NULL
''', [acc_id, person_id, self.At_Kitty]

    @staticmethod
    def is_user_member_of_csa(person_id: int, csa_id: int, still_member: bool) -> SqlQuery:
        q = '''
SELECT COUNT(*)
  FROM account_person ap
  JOIN account a ON a.id=ap.account_id
 WHERE a.csa_id=%s AND ap.person_id=%s'''
        a = [csa_id, person_id]
        if still_member:
            q += ' AND ap.to_date IS NULL'
        return q, a

    @staticmethod
    def person_accounts(*people_ids: int) -> SqlQuery:
        return '''SELECT ap.id, ap.account_id, ap.person_id, ap.from_date, ap.to_date, a.csa_id, a.currency_id
                    FROM account_person ap
                    JOIN account a ON a.id = ap.account_id
                   WHERE ap.person_id IN %s''', [set(people_ids)]

    @staticmethod
    def ownership_delete(ownership_ids: int) -> SqlQuery:
        return 'DELETE FROM account_person WHERE id IN %s', [set(ownership_ids)]

    @staticmethod
    def ownership_change_to_date(ownership_id: int, to_date: datetime) -> SqlQuery:
        return 'UPDATE account_person SET to_date = %s WHERE id = %s', [to_date, ownership_id]

    @staticmethod
    def has_permission_by_account(perm: Permission, person_id: int, acc_id: int) -> SqlQuery:
        """
        Uso acc_id solo per determinare la CSA, non verifico che person_id abbia intestato acc_id,
        anzi in generale non è vero.
        Vedi il caso canCheckAccounts.
        :param perm:
        :param person_id:
        :param acc_id:
        :return:
        """
        return '''
SELECT count(*)
  FROM permission_grant g
  JOIN account a ON a.csa_id=g.csa_id
 WHERE g.perm_id=%s AND g.person_id=%s AND a.id=%s''', [perm, person_id, acc_id]
        # return 'SELECT count(*) FROM permission_grant g JOIN account a ON a.csa_id=g.csa_id
        #  JOIN account_person ap ON ap.person_id=g.person_id
        #  WHERE g.perm_id=%s AND g.person_id=%s AND a.id=%s AND ap.to_date IS NULL', [perm, person_id, acc_id]

    @staticmethod
    def has_permission_by_csa(perm: Permission, person_id: int, csa_id: int) -> SqlQuery:
        q = 'SELECT count(*) FROM permission_grant WHERE perm_id=%s AND person_id=%s AND csa_id'
        a = [perm, person_id]
        if csa_id is None:
            q += ' IS NULL'
        else:
            q += '=%s'
            a.append(csa_id)
        return q, a

    @staticmethod
    def has_permissions(perms: Iterable[Permission], person_id: int, csa_id: int) -> SqlQuery:
        return 'SELECT count(*) FROM permission_grant WHERE perm_id IN %s AND person_id=%s AND csa_id=%s', [
            set(perms),
            person_id,
            csa_id,
        ]

    @staticmethod
    def has_permission_by_order(perm: Permission, person_id: int, order_id: int) -> SqlQuery:
        return '''
SELECT count(*)
  FROM order_definition o
  JOIN permission_grant g ON g.csa_id=o.csa_id
 WHERE g.perm_id=%s AND g.person_id=%s AND o.id=%s''', [
            perm,
            person_id,
            order_id,
        ]

    @staticmethod
    def transaction_lines(tid: int) -> SqlQuery:
        return '''
SELECT id, account_id, description, amount
  FROM transaction_line
 WHERE transaction_id=%s ORDER BY id''', [tid]

    @staticmethod
    def transaction_people(tid: int) -> SqlQuery:
        # qui non verifico che account_person sia del csa giusto perché è implicito nella transazione
        # ma devo verificare che la data della transazione (quidi transaction.transaction_date e
        # non transaction_log.log_date) ricada nell'intervallo di validità di account_person
        return '''
SELECT DISTINCT l.account_id, ap.person_id, ap.from_date, ap.to_date
 FROM transaction t
 JOIN transaction_line l ON t.id=l.transaction_id
 JOIN transaction_log log ON log.transaction_id=t.id
 JOIN account_person ap ON ap.account_id=l.account_id
 WHERE t.id=%s AND
       ap.from_date <= log.log_date AND (ap.to_date IS NULL OR ap.to_date >= log.log_date)''', [tid]

    # SELECT DISTINCT p.id, p.first_name, p.middle_name, p.last_name, l.account_id
    # FROM transaction_line l
    # JOIN account_person ap ON ap.account_id=l.account_id
    # JOIN person p ON ap.person_id=p.id
    # WHERE transaction_id=%s AND ap.to_date IS NULL''', [tid]

    # def transaction_account_gc_names (tid):
    #    return 'SELECT DISTINCT a.id, a.gc_name, c.symbol FROM transaction_line l
    #  JOIN account a ON a.id=l.account_id JOIN currency c ON c.id=a.currency_id WHERE transaction_id=%s', [tid]

    def rss_feed(self, rss_id: str) -> SqlQuery:
        return '''
  SELECT t.description, t.transaction_date, l.amount, l.id, c.symbol
    FROM transaction_line l JOIN transaction t ON t.id=l.transaction_id
    JOIN account_person ap ON ap.account_id=l.account_id
    JOIN account a ON l.account_id=a.id
    JOIN person p ON p.id=ap.person_id
    JOIN currency c ON c.id=a.currency_id
   WHERE p.rss_feed_id=%s AND ap.to_date IS NULL AND t.cc_type NOT IN (%s, %s)
ORDER BY t.transaction_date DESC LIMIT 8''', [rss_id, self.Tt_Unfinished, self.Tt_Error]

    @staticmethod
    def rss_user(rss_id: str) -> SqlQuery:
        return 'SELECT first_name, middle_name, last_name FROM person WHERE rss_feed_id=%s', [rss_id]

    # def rss_id (person_id):
    #    return 'SELECT rss_feed_id FROM person WHERE id=%s', [person_id]

    @staticmethod
    def csa_info(csa_id: int) -> SqlQuery:
        return 'SELECT * FROM csa WHERE id=%s', [csa_id]

    @staticmethod
    def csa_by_account(acc_id: int) -> SqlQuery:
        return 'SELECT csa_id FROM account WHERE id=%s', [acc_id]

    @staticmethod
    def csa_update(csa: JsonObject) -> SqlQuery:
        return '''UPDATE csa SET name=%s, description=%s, default_account_threshold=%s WHERE id=%s''', [
            csa['name'],
            csa['description'],
            csa['default_account_threshold'],
            csa['id'],
        ]

    def csa_amount(self, csa_id: int) -> SqlQuery:
        return '''
  SELECT SUM(l.amount), c.symbol
    FROM transaction t
    JOIN transaction_line l ON l.transaction_id=t.id
    JOIN account a ON l.account_id=a.id
    JOIN currency c ON c.id=a.currency_id
   WHERE t.modified_by_id IS NULL AND t.cc_type NOT IN (%s, %s) AND a.gc_type in (%s, %s) AND a.csa_id=%s
GROUP BY c.symbol''', [self.Tt_Unfinished, self.Tt_Error, self.At_Asset, self.At_Kitty, csa_id]

    # def csa_account_by_account (referenceAccId, account_type):
    #    return 'SELECT b.id FROM account a JOIN account b ON a.csa_id=b.csa_id
    #  WHERE a.id=%s AND b.gc_type=%s', [referenceAccId, account_type]

    @staticmethod
    def csa_account(csa_id: int, account_type: AccountType, currency_id: Optional[int] = None, acc_id: Optional[int] = None, full: bool = False) -> SqlQuery:
        q = 'SELECT '
        q += 'a.*' if full else 'a.id'
        q += ' FROM account a WHERE a.csa_id=%s AND a.gc_type=%s'
        a = [csa_id, account_type]
        if currency_id is not None:
            q += ' AND a.currency_id=%s'
            a.append(currency_id)
        if acc_id is not None:
            q += ' AND id=%s'
            a.append(acc_id)
        return q, a

    def csa_last_kitty_deposit(self, kitty_id: int) -> SqlQuery:
        return '''
  SELECT l.log_date, t.id as tid, p.id, p.first_name, p.middle_name, p.last_name
    FROM transaction_log l
    JOIN transaction t ON t.id = l.transaction_id
    JOIN transaction_line tl ON tl.transaction_id = t.id
    JOIN person p ON p.id = l.operator_id
   WHERE l.op_type = %s AND l.notes = %s AND tl.account_id = %s AND t.modified_by_id IS NULL
ORDER BY l.log_date
   LIMIT %s''', [
            self.Tl_Added,
            self.Tn_kitty_deposit,
            kitty_id,
            1,
        ]

    @staticmethod
    def csa_list(pid: int) -> SqlQuery:
        return '''
   SELECT c.id, c.name, c.description, BIT_OR(g.id IS NOT NULL OR ap.id IS NOT NULL) AS "belong"
     FROM csa c
LEFT JOIN permission_grant g ON g.person_id=%s
LEFT JOIN account_person ap ON ap.person_id=%s
    WHERE g.csa_id IS NULL OR g.csa_id=c.id
 GROUP BY c.id''', [pid, pid]

    @staticmethod
    def csa_delivery_places(csa_id: int) -> SqlQuery:
        return '''
SELECT p.id, p.description, a.first_line, a.second_line, a.description as addr_description,
       IF(a.zip_code IS NULL, c.zip_code, a.zip_code) as zip_code, c.name as city, s.name as state
 FROM delivery_place p
 JOIN street_address a ON p.address_id=a.id
 JOIN city c ON a.city_id=c.id
 JOIN state s ON c.state_id=s.id
WHERE p.csa_id = %s''', [csa_id]

    @staticmethod
    def csa_delivery_place_check(csa_id: int, dp_id: int) -> SqlQuery:
        return 'SELECT count(*) FROM delivery_place WHERE id=%s AND csa_id=%s', [dp_id, csa_id]

    @staticmethod
    def delivery_place_check_by_order(order_id: int, dp_id: int) -> SqlQuery:
        return '''
SELECT count(*)
  FROM delivery_place dp
  JOIN order_definition o ON o.csa_id = dp.csa_id
 WHERE dp.id=%s AND o.id=%s''', [dp_id, order_id]

    @staticmethod
    def csa_delivery_dates(csa_id: int, from_date: datetime, to_date: datetime, enabled_dp : Optional[int] = None) -> SqlQuery:
        q = '''
SELECT dd.*
 FROM delivery_date dd
 JOIN delivery_place dp ON dd.delivery_place_id=dp.id
WHERE dp.csa_id=%s AND dd.from_time BETWEEN %s AND %s
    '''
        a = [csa_id, from_date, to_date]

        if enabled_dp:
            q += ' AND dp.id in %s'
            a.append(set(enabled_dp))

        return q, a

    @staticmethod
    def csa_delivery_shifts(date_id: int) -> SqlQuery:
        return '''
SELECT ds.*
  FROM delivery_shift ds
 WHERE ds.delivery_date_id=%s
    ''', [date_id]

    @staticmethod
    def csa_delivery_shift_add(shift: JsonObject) -> SqlQuery:
        q = 'INSERT INTO delivery_shift (delivery_date_id, person_id, role) VALUES (%s, %s, %s)'
        a = [shift['delivery_date_id'], shift['person_id'], shift.get('role')]
        return q, a

    @staticmethod
    def csa_delivery_shift_update(shift_id: int, role: str) -> SqlQuery:
        q = 'UPDATE delivery_shift SET role=%s WHERE id=%s'
        a = [role, shift_id]
        return q, a

    @staticmethod
    def csa_delivery_shift_check(csa_id: int, shift_id: int, user_id: Optional[int] = None) -> SqlQuery:
        q = '''
SELECT count(*)
  FROM delivery_shift ds
  JOIN delivery_date dd ON dd.id=ds.delivery_date_id
  JOIN delivery_place p ON p.id=dd.delivery_place_id
 WHERE ds.id=%s AND p.csa_id=%s'''
        a = [shift_id, csa_id]
        if user_id is not None:
            q += ' AND ds.person_id=%s'
            a.append(user_id)
        return q, a

    @staticmethod
    def csa_delivery_shift_remove_all(date_id: int) -> SqlQuery:
        return 'DELETE FROM delivery_shift WHERE delivery_date_id=%s', [date_id]

    @staticmethod
    def csa_delivery_shift_remove(shift_id: int) -> SqlQuery:
        return 'DELETE FROM delivery_shift WHERE id=%s', [shift_id]

    @staticmethod
    def csa_delivery_date_check(csa_id: int, date_id: int) -> SqlQuery:
        return '''
SELECT count(*)
  FROM delivery_date dd
  JOIN delivery_place p ON p.id=dd.delivery_place_id
 WHERE dd.id=%s AND p.csa_id=%s''', [date_id, csa_id]

    @staticmethod
    def csa_delivery_date_remove(date_id: int) -> SqlQuery:
        return 'DELETE FROM delivery_date WHERE id=%s', [date_id]

    @staticmethod
    def csa_delivery_date_update(id: int, delivery_place_id: int, from_time: str, to_time: str, notes: str) -> SqlQuery:
        return '''
UPDATE delivery_date
   SET delivery_place_id=%s,
       from_time=%s,
       to_time=%s,
       notes=%s
 WHERE id=%s''', [
            delivery_place_id,
            jsonlib.decode_date(from_time),
            jsonlib.decode_date(to_time),
            notes,
            id
        ]

    @staticmethod
    def csa_delivery_date_save(delivery_place_id: int, from_time: str, to_time: str, notes: str) -> SqlQuery:
        return '''
INSERT INTO delivery_date
            (delivery_place_id, from_time, to_time, notes)
     VALUES (%s, %s, %s, %s)''', [
            delivery_place_id,
            jsonlib.decode_date(from_time),
            jsonlib.decode_date(to_time),
            notes
        ]

    def delivery_dates_for_notifications(self, from_time: datetime, to_time: datetime, fetch_covered: bool, fetch_uncovered: bool) -> SqlQuery:
        q = '''
   SELECT dd.id, dd.notes as "delivery_notes", dd.from_time, dd.to_time,
          dp.description as "delivery_place",
          ds.role as "shift_role",
          p.id as "person_id", p.first_name, p.middle_name, p.last_name,
          pa.kind as "contact_kind", pa.address as "contact_address",
          c.id as "csa_id", c.name as "csa",
          sa.first_line as "address_first_line", sa.second_line as "address_second_line",
              sa.description as "address_description", sa.zip_code as "address_zip_code",
          sc.name as "city"
     FROM delivery_date dd
     JOIN delivery_place dp ON dp.id=dd.delivery_place_id
LEFT JOIN delivery_shift ds ON ds.delivery_date_id=dd.id
     JOIN csa c ON dp.csa_id=c.id
     JOIN street_address sa ON dp.address_id=sa.id
     JOIN city sc ON sa.city_id=sc.id
LEFT JOIN person p ON ds.person_id=p.id
LEFT JOIN person_contact pc ON p.id=pc.person_id
LEFT JOIN contact_address pa ON pa.id=pc.address_id
    WHERE dd.from_time>%s AND
          dd.from_time<%s AND
          (pa.kind IS NULL OR pa.kind IN %s)
        '''
        a = [from_time, to_time, {self.Ck_Email, self.Ck_Mobile, self.Ck_Telephone}]
        if fetch_covered and fetch_uncovered:
            pass
        elif fetch_covered:
            q += ' AND ds.id IS NOT NULL'
            # q += ' HAVING count(ds.id) > %s'
            # a.append(0)
        elif fetch_uncovered:
            q += ' AND ds.id IS NULL'
            # q += ' HAVING count(ds.id) == %s'
            # a.append(0)
        return q, a

    @staticmethod
    def account_currency(acc_id, csa_id, required_curr):
        return 'SELECT count(*) FROM account a WHERE a.id=%s AND a.csa_id=%s AND a.currency_id=%s', [
            acc_id, csa_id, required_curr
        ]

    # def account_names (csa_id):
    #    '''Tutti i nomi di conti di una comunità escluso gli Scomparsi.
    #    FIX Me: prima o poi scompariranno le colonne gc!
    #    '''
    #    return 'SELECT a.gc_name, a.id, c.id, c.symbol FROM account a JOIN currency c ON a.currency_id=c.id
    #  WHERE a.csa_id = %s AND a.gc_parent = %s AND a.gc_id <> %s', [
    #  csa_id, 'acf998ffe1edbcd44bc30850813650ac', '5ba64cec222104efb491ceafd6dd1812']

    @staticmethod
    def account_currencies(csa_id):
        """
        Tutti i conti aperti di un csa, con la data di apertura, la moneta e l'owner.
        NB: ai fini della validazione della data di transazione mi interessa il max(ap.from_date)
        ma fra quelli cointestati conta il minimo.
        :param csa_id:
        :return:
        """
        return """
SELECT a.id, c.id, c.symbol, ap.from_date, ap.person_id, p.first_name, p.middle_name, p.last_name
  FROM account a
  JOIN currency c ON a.currency_id=c.id
  JOIN account_person ap ON ap.account_id=a.id
  JOIN person p ON p.id=ap.person_id
 WHERE a.csa_id = %s AND ap.to_date IS NULL""", [
            csa_id
        ]
#        return 'SELECT a.id, c.id, c.symbol FROM account a JOIN currency c ON a.currency_id=c.id WHERE a.csa_id = %s', [
#            csa_id
#        ]

    def csa_currencies(self, csa_id, only_id=True):
        """
        Tutte le valute usate in un csa.
        :param csa_id:
        :return:
        """
        if only_id:
            return 'SELECT a.currency_id FROM account a WHERE a.csa_id=%s AND a.gc_type=%s', [csa_id, self.At_Kitty]
        else:
            return '''
SELECT a.currency_id AS "id", c.symbol
  FROM account a
  JOIN currency c ON a.currency_id = c.id
 WHERE a.csa_id = %s AND a.gc_type = %s''', [csa_id, self.At_Kitty]

    @staticmethod
    def account_people(csa_id):
        # FIXME: buttare
        return '''
SELECT p.id, p.first_name, p.middle_name, p.last_name, a.id
  FROM person p
  JOIN account_person ap ON p.id=ap.person_id
  JOIN account a ON ap.account_id=a.id
 WHERE a.csa_id=%s AND ap.to_date IS NULL''', [csa_id]

    def account_people_addresses(self, csa_id):
        return '''
SELECT c.address, p.id, a.id
  FROM person p
  JOIN account_person ap ON ap.person_id=p.id
  JOIN account a ON ap.account_id=a.id
  JOIN person_contact pc ON p.id=pc.person_id
  JOIN contact_address c ON pc.address_id=c.id
 WHERE a.csa_id=%s AND c.kind IN (%s, %s) AND ap.to_date IS NULL''', [csa_id, self.Ck_Email, self.Ck_Nickname]

    def account_owners_with_optional_email_for_notifications(self, account_ids):
        return '''
   SELECT ap.account_id, p.id, p.first_name, p.middle_name, p.last_name, c.address
     FROM account_person ap
     JOIN person p ON ap.person_id=p.id
LEFT JOIN person_contact pc ON p.id=pc.person_id
LEFT JOIN contact_address c ON pc.address_id=c.id
    WHERE ap.to_date IS NULL AND
          ap.account_id IN %s AND
          (c.kind=%s OR c.kind IS NULL) AND
          p.account_notifications=%s
 ORDER BY ap.account_id, pc.priority''', [set(account_ids), self.Ck_Email, self.An_EveryMovement]

    def account_total_for_notifications(self, account_ids):
        return '''
SELECT a.id, sum(l.amount), c.symbol
    FROM account a
    JOIN currency c ON a.currency_id=c.id
    JOIN transaction_line l ON l.account_id=a.id
    JOIN transaction t ON t.id=l.transaction_id
   WHERE
     t.modified_by_id IS NULL AND
     t.cc_type NOT IN (%s, %s) AND
     a.id IN %s
GROUP BY a.id
''', [self.Tt_Unfinished, self.Tt_Error, set(account_ids)]

    @staticmethod
    def account_update_membership_fee(csa_id, person_id, amount):
        return '''
UPDATE account a
 INNER JOIN account_person ap ON a.id=ap.account_id
 SET a.membership_fee = %s
 WHERE ap.person_id = %s AND ap.to_date IS NULL AND a.csa_id = %s''', [parse_decimal(amount), person_id, csa_id]

    @staticmethod
    def account_close(close_date_time, account_id, owner_id):
        return 'UPDATE account_person SET to_date=%s WHERE person_id=%s AND account_id = %s AND to_date IS NULL', [
            close_date_time, owner_id, account_id
        ]

    def account_create(self, name, atype, csa_id, curr_id, fee):
        return '''
INSERT INTO account (state, gc_name, gc_type, csa_id, currency_id, membership_fee)
     VALUES (%s, %s, %s, %s, %s, %s)''', [
            self.As_Open,
            name,
            atype,
            csa_id,
            curr_id,
            fee
        ]

    # def expenses_accounts (csa_id):
    #    return 'SELECT id, gc_name, currency_id FROM account where gc_type =%s AND csa_id=%s AND state=%s',
    #  [At_Expense, csa_id, As_Open]

    # def expenses_line_descriptions (csa_id):
    #    return 'SELECT DISTINCT l.description FROM transaction_line l JOIN account a ON l.account_id=a.id
    #  WHERE a.gc_type=%s AND a.csa_id=%s AND l.description IS NOT NULL', [At_Expense, csa_id]

    # def expenses_transaction_descriptions (csa_id):
    #    return 'SELECT DISTINCT t.description FROM transaction_line l JOIN account a ON l.account_id=a.id
    #  JOIN transaction t ON l.transaction_id=t.id WHERE a.gc_type=%s AND a.csa_id=%s AND t.description IS NOT NULL',
    #  [At_Expense, csa_id]

    @staticmethod
    def insert_transaction(desc, tdate, cc_type, currency_id, csa_id):
        return '''
INSERT INTO transaction (description, transaction_date, cc_type, currency_id, csa_id)
     SELECT %s, %s, %s, id, %s
       FROM currency
      WHERE id=%s''', [desc, tdate, cc_type, csa_id, currency_id]

    @staticmethod
    def insert_transaction_line(tid, desc, amount, acc_id):
        return '''
INSERT INTO transaction_line (transaction_id, account_id, description, amount)
     SELECT %s, a.id, %s, %s FROM account a WHERE a.id = %s''', [tid, desc, parse_decimal(amount), acc_id]

    def insert_transaction_line_membership_fee(self, tid, amount, csa_id, currency_id):
        return '''
INSERT INTO transaction_line (transaction_id, account_id, description, amount)
 SELECT %s, a.id, %s, - a.membership_fee * %s
  FROM account a
  JOIN account_person ap on ap.account_id=a.id
  WHERE a.csa_id = %s AND a.currency_id = %s AND a.gc_type = %s AND a.membership_fee > 0
    AND ap.to_date IS NULL
  GROUP BY a.id
  ''', [tid, '', parse_decimal(amount), csa_id, currency_id, self.At_Asset]

    @staticmethod
    def check_transaction_coherency(tid):
        return '''
SELECT DISTINCT a.currency_id, a.csa_id
  FROM transaction_line l
  JOIN account a ON a.id=l.account_id
 WHERE l.transaction_id = %s''', [tid]

    @staticmethod
    def transaction_calc_last_line_amount(tid, tline_id):
        return 'SELECT - SUM(amount) FROM transaction_line WHERE transaction_id = %s AND id != %s', [tid, tline_id]

    @staticmethod
    def transaction_fix_amount(tline_id, amount):
        return 'UPDATE transaction_line SET amount = %s WHERE id = %s', [parse_decimal(amount), tline_id]

    @staticmethod
    def finalize_transaction(tid, ttype):
        return 'UPDATE transaction SET cc_type=%s WHERE id=%s', [ttype, tid]

    @staticmethod
    def transaction_fetch_lines_to_compare(old_trans_id, new_trans_id):
        """
        Metodo usato per calcolare le differenze introdotte dalla modifica di una transazione.
        :param old_trans_id:
        :param new_trans_id:
        :return:
        """
        return '''
SELECT transaction_id, account_id, amount, description
  FROM transaction_line
 WHERE transaction_id in (%s, %s)''', [old_trans_id, new_trans_id]

    @staticmethod
    def transaction_edit(tid):
        return '''
SELECT t.description, t.transaction_date as date, t.cc_type,
       c.id as "currency[__cid", c.symbol as "currency[__csym",
       t.modified_by_id as modified_by, t2.id as "modifies",
       l.log_date, l.op_type,
       p.id as operator__pid, p.first_name as operator__first_name,
       p.middle_name as operator__middle_name, p.last_name as operator__last_name
 FROM transaction t
 JOIN transaction_log l ON l.transaction_id=t.id
 JOIN person p ON l.operator_id = p.id
 LEFT JOIN transaction t2 ON t.id=t2.modified_by_id
 JOIN currency c ON c.id=t.currency_id
 WHERE t.id=%s''', [tid]

    @staticmethod
    def log_transaction(tid, person_id, log_type, log_desc, tdate):
        return '''
INSERT INTO transaction_log (log_date, operator_id, op_type, transaction_id, notes)
     VALUES (%s, %s, %s, %s, %s)''', [tdate, person_id, log_type, tid, log_desc]

    @staticmethod
    def log_transaction_check_operator(person_id, trans_id):
        return 'SELECT COUNT(*) FROM transaction_log WHERE transaction_id=%s AND operator_id=%s', [trans_id, person_id]

    def transaction_on_kitty_and_user_is_member(self, trans_id, person_id):
        return '''
SELECT count(*)
  FROM transaction_line l
  JOIN account a ON l.account_id=a.id
  JOIN account a2 ON a.csa_id=a2.csa_id
  JOIN account_person ap ON a2.id=ap.account_id
 WHERE transaction_id=%s AND a.gc_type=%s AND ap.person_id=%s AND ap.to_date IS NULL;
    ''', [trans_id, self.At_Kitty, person_id]

    @staticmethod
    def transaction_is_involved(trans_id, person_id):
        return '''
SELECT COUNT(*)
  FROM transaction_line l
  JOIN account a ON l.account_id=a.id
  JOIN account_person ap ON a.id=ap.account_id
 WHERE l.transaction_id=%s AND ap.person_id=%s
''', [trans_id, person_id]

    @staticmethod
    def transaction_previuos(trans_id):
        return 'SELECT id FROM transaction WHERE modified_by_id = %s', [trans_id]

    @staticmethod
    def transaction_type(trans_id):
        return 'SELECT cc_type, description, modified_by_id FROM transaction WHERE id = %s', [trans_id]

    @staticmethod
    def update_transaction(old_trans_id, new_trans_id):
        return 'UPDATE transaction SET modified_by_id = %s WHERE id = %s', [new_trans_id, old_trans_id]

    transactions_editable_order_by = [
        'l.log_date DESC',
        't.transaction_date DESC',
        'p.first_name,p.last_name',
        't.description',
    ]

    Lo_Added = 'A'
    Lo_Modified = 'M'
    Lo_Deleted = 'D'

    def transactions_count_all(self, csa_id, q):
        return '''
SELECT count(l.id)
  FROM transaction_log l
  JOIN transaction t ON t.id=l.transaction_id
  JOIN person p ON l.operator_id= p.id
 WHERE t.csa_id=%s AND l.op_type IN (%s, %s, %s) AND
      (p.first_name LIKE %s OR p.middle_name LIKE %s OR p.last_name LIKE %s OR t.description LIKE %s)
''', [
            csa_id,
            self.Lo_Added, self.Lo_Modified, self.Lo_Deleted,
            q, q, q, q,
        ]

    def transactions_all(self, csa_id, q, o, from_line, to_line):
        return '''
  SELECT l.id, l.log_date, l.op_type,
         t.id, t.description, t.transaction_date, t.modified_by_id, t.cc_type,
         p.id, p.first_name, p.middle_name, p.last_name
    FROM transaction_log l
    JOIN transaction t ON t.id=l.transaction_id
    JOIN person p ON l.operator_id= p.id
   WHERE t.csa_id=%s AND l.op_type IN (%s, %s, %s) AND
         (p.first_name LIKE %s OR p.middle_name LIKE %s OR p.last_name LIKE %s OR t.description LIKE %s)
ORDER BY ''' + o + ''' LIMIT %s OFFSET %s''', [
            csa_id,
            self.Lo_Added, self.Lo_Modified, self.Lo_Deleted,
            q, q, q, q,
            to_line - from_line + 1,
            from_line
           ]

    def transactions_count_by_editor(self, csa_id, operator, q):
        return '''
SELECT count(l.id)
  FROM transaction_log l
  JOIN transaction t ON t.id=l.transaction_id
  JOIN person p ON l.operator_id= p.id
 WHERE t.csa_id=%s AND l.operator_id=%s AND l.op_type IN (%s, %s, %s) AND
       (t.description LIKE %s)''', [
            csa_id,
            operator,
            self.Lo_Added, self.Lo_Modified, self.Lo_Deleted,
            q,
        ]

    def transactions_by_editor(self, csa_id, operator, q, o, from_line, to_line):
        return '''
  SELECT l.id, l.log_date, l.op_type,
         t.id, t.description, t.transaction_date, t.modified_by_id, t.cc_type,
         p.id, p.first_name, p.middle_name, p.last_name
    FROM transaction_log l
    JOIN transaction t ON t.id=l.transaction_id
    JOIN person p ON l.operator_id= p.id
   WHERE t.csa_id=%s AND l.operator_id=%s AND l.op_type IN (%s, %s, %s) AND
         (t.description LIKE %s)
ORDER BY ''' + o + ''' LIMIT %s OFFSET %s''', [
            csa_id,
            operator,
            self.Lo_Added, self.Lo_Modified, self.Lo_Deleted,
            q,
            to_line - from_line + 1,
            from_line
           ]

    @staticmethod
    def count_people(csa_id, t, dp, ex, search_contact_kinds):
        q = 'SELECT count(p.id) FROM '
        a = []

        if t and search_contact_kinds:
            q += '''
  (SELECT p.*, group_concat(ca.address, ', ') AS contacts
     FROM person p
LEFT JOIN person_contact pc ON pc.person_id=p.id
LEFT JOIN contact_address ca ON ca.id=pc.address_id
    WHERE ca.kind IS NULL OR ca.kind in %s
 GROUP BY p.id) p'''
            a.append(set(search_contact_kinds))
        else:
            q += 'person p'

        q += '''
 JOIN account_person ap ON ap.person_id=p.id
 JOIN account a ON a.id=ap.account_id
WHERE a.csa_id=%s'''
        a.append(csa_id)

        if not ex:
            q += ' AND ap.to_date IS NULL'

        if t:
            q += ' AND (p.first_name LIKE %s OR p.middle_name LIKE %s OR p.last_name LIKE %s'
            a.extend([t, t, t])
            if search_contact_kinds:
                q += ' OR p.contacts LIKE %s)'
                a.append(t)
            else:
                q += ')'

        dp = int(dp)
        if dp == -2:
            q += " AND p.default_delivery_place_id IS NULL"
        elif dp != -1:
            q += " AND p.default_delivery_place_id=%s"
            a.append(dp)

        return q, a

    @staticmethod
    def people_index(csa_id, t, dp, o, ex, from_line, to_line, search_contact_kinds):
        q = 'SELECT p.id, p.first_name, p.middle_name, p.last_name FROM '
        a = []

        if t and search_contact_kinds:
            q += '''
  (SELECT p.*, group_concat(ca.address, ', ') AS contacts
     FROM person p
LEFT JOIN person_contact pc ON pc.person_id=p.id
LEFT JOIN contact_address ca ON ca.id=pc.address_id
    WHERE ca.kind IS NULL OR ca.kind IN %s
 GROUP BY p.id) p'''
            a.append(set(search_contact_kinds))
        else:
            q += 'person p'

        q += '''
 JOIN account_person ap ON ap.person_id=p.id
 JOIN account a ON a.id=ap.account_id
 WHERE a.csa_id=%s'''
        a.append(csa_id)

        if not ex:
            q += ' AND ap.to_date IS NULL'

        if t:
            q += ' AND (p.first_name LIKE %s OR p.middle_name LIKE %s OR p.last_name LIKE %s'
            a.extend([t, t, t])
            if search_contact_kinds:
                q += ' OR p.contacts LIKE %s)'
                a.append(t)
            else:
                q += ')'

        dp = int(dp)
        if dp == -2:
            q += " AND p.default_delivery_place_id IS NULL"
        elif dp != -1:
            q += " AND p.default_delivery_place_id=%s"
            a.append(dp)

        if o:
            q += ''' ORDER BY ''' + o

        if from_line != -1:
            q += ''' LIMIT %s OFFSET %s'''
            a.extend([
               to_line - from_line + 1,
               from_line
            ])

        return q, a

    @staticmethod
    def people_profiles2(csa_id, pids):
        return (
            '''
SELECT ap.from_date, ap.to_date, ap.person_id, a.*
  FROM account_person ap JOIN account a ON ap.account_id=a.id
 WHERE ap.person_id in %s AND a.csa_id=%s''',
            '''
SELECT csa_id, person_id, perm_id
  FROM permission_grant
 WHERE person_id IN %s AND csa_id=%s OR csa_id IS NULL''',
            [set(pids), csa_id],
        )

    @staticmethod
    def people_profiles1(pids):
        return (
            'SELECT * FROM person WHERE id IN %s',
            '''
  SELECT pc.person_id, pc.priority, a.*
    FROM person_contact pc
    JOIN contact_address a ON a.id=pc.address_id
   WHERE pc.person_id IN %s
ORDER BY pc.priority''',
            [set(pids)],
        )

    @staticmethod
    def people_addresses(pids, contact_kind):
        return '''
SELECT p.id, c.address
  FROM person p
  JOIN person_contact pc ON p.id=pc.person_id
  JOIN contact_address c ON pc.address_id=c.id
 WHERE c.kind=%s AND p.id in %s
        ''', [contact_kind, set(pids)]

    @staticmethod
    def people_with_transaction_report(frequency):
        return '''
SELECT p.id, p.account_notifications, ap.account_id
  FROM person p
  JOIN account_person ap on ap.person_id=p.id
 WHERE p.account_notifications=%s
''', [frequency]

    def person_notification_email(self, pid):
        # FIXME: scrivere a tutte le email
        return '''
SELECT c.address
 FROM person p
 JOIN person_contact pc ON p.id=pc.person_id
 JOIN contact_address c ON pc.address_id=c.id
WHERE c.kind=%s AND p.id=%s ORDER BY pc.priority LIMIT 1''', [
            self.Ck_Email, pid
        ]

    @staticmethod
    def profile_update(p):
        return '''
UPDATE person
   SET first_name = %s,
       middle_name = %s,
       last_name = %s,
       account_notifications = %s,
       cash_treshold = %s,
       default_delivery_place_id = %s
 WHERE id = %s''', [
            p['first_name'],
            p['middle_name'],
            p['last_name'],
            p['account_notifications'],
            p['cash_treshold'],
            p['default_delivery_place_id'],
            p['id'],
        ]

    @staticmethod
    def privacy_update(person_id: int, privacy_consent: str) -> SqlQuery:
        return 'UPDATE person SET privacy_consent = %s WHERE id = %s', [privacy_consent, person_id]

    # @staticmethod
    # def contact_address_remove(aId):
    #    return 'DELETE FROM contact_address WHERE id=%s', [aId]

    # @staticmethod
    # def removePersonContact(pcId):
    #    return 'DELETE FROM person_contact WHERE id=%s', [pcId]

    @staticmethod
    def contact_address_remove(aids):
        return 'DELETE FROM contact_address WHERE id in %s', [set(aids)]

    @staticmethod
    def person_contact_remove(aids):
        return 'DELETE FROM person_contact WHERE address_id in %s', [set(aids)]
        #    # cfr. http://stackoverflow.com/a/4429409
        #    return (
        # '''DELETE person_contact p FROM person_contact p,
        #          (SELECT pc.id
        #           FROM person_contact pc
        #           JOIN contact_address a ON pc.address_id = a.id
        #           WHERE pc.person_id = %s AND a.kind != %s) t
        #    WHERE p.id = t.id''', [pid, Ck_Id]
        #            )

    @staticmethod
    def person_contact_remove_by_id(pcids):
        return 'DELETE FROM person_contact WHERE id in %s', [set(pcids)]

    @staticmethod
    def contact_address_insert(addr, kind, ctype):
        return '''INSERT INTO contact_address (address, kind, contact_type) VALUES (%s, %s, %s)''', [addr, kind, ctype]

    @staticmethod
    def contact_address_update(pk, addr, ctype):
        return '''UPDATE contact_address SET address=%s, contact_type=%s WHERE id=%s''', [addr, ctype, pk]

    @staticmethod
    def person_contact_insert(pid, aid, pri):
        return '''INSERT INTO person_contact (person_id, address_id, priority) VALUES (%s, %s, %s)''', [pid, aid, pri]

    def contacts_fetch(self, pid):
        return '''
SELECT a.id
  FROM person_contact pc
  JOIN contact_address a ON pc.address_id=a.id
 WHERE pc.person_id=%s AND a.kind != %s''', [pid, self.Ck_Id]
        # return 'SELECT pc.id, pc.priority, a.id, a.kind, a.address, a.contact_type FROM person_contact pc
        #  JOIN contact_address a ON pc.address_id=a.id WHERE pc.person_id=%s ORDER BY pc.priority', [pid]

    @staticmethod
    def contacts_fetch_all(*pids):
        return '''
SELECT pc.id, a.id, a.kind, a.contact_type, a.address
  FROM person_contact pc
  JOIN contact_address a ON pc.address_id=a.id
 WHERE pc.person_id IN %s''', [set(pids)]

    @staticmethod
    def permission_revoke(pid, csa_id, pp):
        return ('DELETE FROM permission_grant WHERE person_id=%s AND csa_id=%s AND perm_id in %s', [
            pid, csa_id, set(pp)
        ])

    @staticmethod
    def permission_grant(pid, perm, csa_id):
        return '''INSERT INTO permission_grant (person_id, perm_id, csa_id) VALUES (%s, %s, %s)''', [pid, perm, csa_id]

    def is_unique_email(self, pid, email):
        return '''
SELECT COUNT(a.id)
  FROM contact_address a
  JOIN person_contact pc ON pc.address_id=a.id
 WHERE pc.person_id != %s AND a.address = %s AND a.kind = %s''', [pid, email, self.Ck_Email]

    admin_people_index_order_by = [
        None,  # nessun ordinamento
        'p.last_visit desc',
        'p.first_name, p.last_name',
        'p.last_login',
    ]

    @staticmethod
    def admin_people_index(t, csa_id, order, from_line, to_line, search_contact_kinds):
        q = 'SELECT p.id, p.first_name, p.middle_name, p.last_name FROM '
        a = []

        if t and search_contact_kinds:
            q += '''
  (SELECT p.*, group_concat(ca.address, ', ') AS contacts
     FROM person p
LEFT JOIN person_contact pc ON pc.person_id=p.id
LEFT JOIN contact_address ca ON ca.id=pc.address_id
    WHERE ca.kind IS NULL OR ca.kind IS NULL OR ca.kind IN %s
 GROUP BY p.id) p'''
            a.append(set(search_contact_kinds))
        else:
            q += 'person p'

        q += '''
 WHERE p.id NOT IN
  (SELECT ap.person_id
     FROM account_person ap'''
        if csa_id:
            q += ' JOIN account a WHERE a.csa_id=%s AND ap.to_date IS NULL'
            a.append(csa_id)
        else:
            q += ' WHERE ap.to_date IS NULL'
        q += ')'

        if t:
            q += ' AND (p.first_name LIKE %s OR p.middle_name LIKE %s OR p.last_name LIKE %s'
            a.extend([t, t, t])
            if search_contact_kinds:
                q += ' OR p.contacts LIKE %s)'
                a.append(t)
            else:
                q += ')'

        if order:
            q += ' ORDER BY ' + order

        if from_line is not None:
            q += ' LIMIT %s OFFSET %s'
            a.extend([to_line - from_line + 1, from_line])

        return q, a

    @staticmethod
    def admin_count_people(t, csa_id, search_contact_kinds):
        q = 'SELECT count(*) FROM '
        a = []

        if t and search_contact_kinds:
            q += '''
  (SELECT p.*, group_concat(ca.address, ', ') AS contacts
     FROM person p
LEFT JOIN person_contact pc ON pc.person_id=p.id
LEFT JOIN contact_address ca ON ca.id=pc.address_id
    WHERE ca.kind IS NULL OR ca.kind IN %s
 GROUP BY p.id) p'''
            a.append(set(search_contact_kinds))
        else:
            q += 'person p'

        q += '''
 WHERE p.id NOT IN
  (SELECT ap.person_id
     FROM account_person ap'''
        if csa_id:
            q += ' JOIN account a WHERE a.csa_id=%s AND ap.to_date IS NULL'
            a.append(csa_id)
        else:
            q += ' WHERE ap.to_date IS NULL'
        q += ')'

        if t:
            q += ' AND (p.first_name LIKE %s OR p.middle_name LIKE %s OR p.last_name LIKE %s'
            a.extend([t, t, t])
            if search_contact_kinds:
                q += ' OR p.contacts LIKE %s)'
                a.append(t)
            else:
                q += ')'

        return q, a

    @staticmethod
    def contacts_reassign(newpid, oldpid):
        return 'UPDATE person_contact SET person_id=%s WHERE person_id=%s', [newpid, oldpid]

    @staticmethod
    def permissions_reassign(newpid, oldpid):
        return 'UPDATE permission_grant SET person_id=%s WHERE person_id=%s', [newpid, oldpid]

    @staticmethod
    def accounts_reassign(newpid, oldpid):
        return 'UPDATE account_person SET person_id=%s WHERE person_id=%s', [newpid, oldpid]

    @staticmethod
    def person_delete(pid):
        return 'DELETE FROM person WHERE id=%s', [pid]

    @staticmethod
    def contact_address_delete(pid):
        return 'DELETE FROM contact_address WHERE id IN (SELECT address_id FROM person_contact WHERE person_id=%s)', [
            pid
        ]

    @staticmethod
    def contact_person_delete(pid):
        return 'DELETE FROM person_contact WHERE person_id=%s', [pid]

    @staticmethod
    def permission_revoke_all(pid):
        return 'DELETE FROM permission_grant WHERE person_id=%s', [pid]

    @staticmethod
    def permission_all(*pids):
        return 'SELECT id, csa_id, person_id, perm_id FROM permission_grant WHERE person_id IN %s', [set(pids)]

    @staticmethod
    def permission_revoke_by_grant(grant_ids):
        return 'DELETE FROM permission_grant WHERE id IN %s', [set(grant_ids)]

    @staticmethod
    def account_grant(pid, acc, from_date):
        return 'INSERT INTO account_person (person_id, account_id, from_date) VALUES (%s, %s, %s)', [
            pid, acc, from_date
        ]

    @staticmethod
    def order_exists(order_id):
        return 'SELECT count(id) FROM order_definition WHERE id=%s', [order_id]

    @staticmethod
    def order_state(order_id):
        return 'SELECT state, `lock` FROM order_definition WHERE id=%s', [order_id]

    @staticmethod
    def order_fetch(order_id):
        return '''
SELECT o.id, o.csa_id, o.state, o.lock, o.description, o.notes, o.account_threshold, o.profile_required,
       o.submission_exp,
       o.producer_id,
       o.currency_id, cc.symbol
  FROM order_definition o
  JOIN currency cc ON cc.id = o.currency_id
 WHERE o.id = %s
''', [order_id]

    @staticmethod
    def order_delivery(order_ids, state=None):
        multiple_deliveries = type(order_ids) is list

        q = 'SELECT od.id, od.delivery_date_id, d.from_time, d.to_time, d.notes, d.delivery_place_id'
        if multiple_deliveries:
            q += ', od.order_id'

        q += '''
  FROM order_delivery_date od
  JOIN delivery_date d ON od.delivery_date_id = d.id'''
        a = []

        if state is not None:
            q += ' JOIN order_definition po ON po.id = od.order_id' \
                 ' WHERE po.state = %s AND po.id'''
            a.append(state)
        else:
            q += ' WHERE od.order_id'

        if type(order_ids) is list:
            q += ' IN %s'
            a.append(set(order_ids))
        else:
            q += ' = %s'
            a.append(order_ids)

        return q, a

    @staticmethod
    def order_definition_is_referent(order_id, person_id):
        return 'SELECT count(*) FROM order_referent WHERE order_id=%s AND person_id=%s', [
            order_id, person_id
        ]

    @staticmethod
    def order_products(order_id):
        return '''
  SELECT id, description
    FROM order_product
   WHERE order_id = %s
ORDER BY position''', [order_id]

    @staticmethod
    def order_product_quantities(order_id):
        return '''
  SELECT p.id AS "product", q.id, q.description, q.amount, q.max
    FROM order_product_quantity q
    JOIN order_product p ON p.id = q.product_id
    JOIN order_definition o ON o.id = p.order_id
   WHERE o.id = %s
ORDER BY p.position, q.position''', [order_id]

    def order_save(self, order_def):
        csa_id = order_def['csa_id']

        producer_id = order_def['producer_id']
        currency_id = order_def['currency_id']

        q = '''
INSERT INTO order_definition (csa_id, state, description, notes, submission_exp, account_threshold, profile_required,
                           producer_id, currency_id)
     SELECT a.csa_id, %s, %s, %s, %s, %s, %s
'''
        a = [
            order_def['state'],
            order_def['description'],
            order_def['notes'],
            jsonlib.decode_date(order_def['submission_exp']) if order_def['submission_exp_known'] else None,
            order_def['account_threshold'] if order_def['apply_account_threshold'] else None,
            order_def['profile_required'],
        ]

        if producer_id is None:
            q += ', NULL'
        else:
            q += ', p.id'

        if currency_id is None:
            q += ', NULL'
        else:
            q += ', a.currency_id'

        q += ' FROM account a'

        if producer_id is not None:
            q += ''', person p
 JOIN account_person ap ON p.id = ap.person_id
 JOIN account apa ON ap.account_id = apa.id AND ap.to_date IS NULL'''

        q += ' WHERE a.csa_id = %s AND a.currency_id = %s AND a.gc_type = %s'
        a.append(csa_id)
        a.append(currency_id)
        a.append(self.At_Kitty)

        if producer_id is not None:
            q += ' AND p.id = %s AND apa.csa_id = %s'
            a.append(producer_id)
            a.append(csa_id)

        return q, a

    def order_update(self, order_def):
        producer_id = order_def.get('producer_id')
        currency_id = order_def.get('currency_id')

        if currency_id is None:
            if producer_id is None:
                q = '''
UPDATE order_definition o
   SET o.lock=o.lock + 1, o.description=%s, o.notes=%s, o.account_threshold=%s, o.profile_required=%s,
       o.currency_id=%s, o.producer_id=%s, o.submission_exp=%s
 WHERE o.id=%s AND o.lock=%s
                '''
                a = [
                    order_def.get('description'),
                    order_def.get('notes'),
                    order_def.get('account_threshold') if order_def['apply_account_threshold'] else None,
                    order_def['profile_required'],
                    None,
                    None,
                    jsonlib.decode_date(order_def['submission_exp'])
                        if order_def['submission_exp_known'] else None,
                    order_def['id'],
                    order_def['lock'],
                ]
            else:
                q = '''
UPDATE order_definition o
  JOIN account a ON a.csa_id=o.csa_id
  JOIN account_person ap ON ap.account_id=a.id
  JOIN person p ON p.id=ap.person_id
   SET o.lock=o.lock + 1, o.description=%s, o.notes=%s, o.account_threshold=%s, o.profile_required=%s,
       o.currency_id=%s, o.producer_id=p.id, o.submission_exp=%s
 WHERE o.id=%s AND ap.to_date IS NULL AND p.id=%s AND o.lock=%s'''
                a = [
                    order_def.get('description'),
                    order_def.get('notes'),
                    order_def.get('account_threshold') if order_def['apply_account_threshold'] else None,
                    order_def['profile_required'],
                    None,
                    jsonlib.decode_date(order_def['submission_exp'])
                        if order_def['submission_exp_known'] else None,
                    order_def['id'],
                    producer_id,
                    order_def['lock'],
                ]
        elif producer_id is None:
            q = '''
UPDATE order_definition o
  JOIN account a ON a.csa_id=o.csa_id
   SET o.lock=o.lock + 1, o.description=%s, o.notes=%s, o.account_threshold=%s, o.profile_required=%s,
       o.currency_id=a.currency_id, o.producer_id=%s, o.submission_exp=%s
 WHERE o.id=%s AND a.currency_id=%s AND a.gc_type=%s AND o.lock=%s'''
            a = [
                order_def.get('description'),
                order_def.get('notes'),
                order_def.get('account_threshold') if order_def['apply_account_threshold'] else None,
                order_def['profile_required'],
                None,
                jsonlib.decode_date(order_def['submission_exp'])
                    if order_def['submission_exp_known'] else None,
                order_def['id'],
                currency_id,
                self.At_Kitty,
                order_def['lock'],
            ]
        else:
            q = '''
UPDATE order_definition o
  JOIN account a ON a.csa_id=o.csa_id
  JOIN account_person ap ON ap.account_id=a.id
  JOIN person p ON p.id=ap.person_id
   SET o.lock=o.lock + 1, o.description=%s, o.notes=%s, o.account_threshold=%s, o.profile_required=%s,
       o.currency_id=a.currency_id, o.producer_id=p.id, o.submission_exp=%s
 WHERE o.id=%s AND ap.to_date IS NULL AND p.id=%s AND a.currency_id=%s AND o.lock=%s'''
            a = [
                order_def.get('description'),
                order_def.get('notes'),
                order_def.get('account_threshold') if order_def['apply_account_threshold'] else None,
                order_def['profile_required'],
                jsonlib.decode_date(order_def['submission_exp'])
                    if order_def['submission_exp_known'] else None,
                order_def['id'],
                producer_id,
                currency_id,
                order_def['lock'],
            ]

        return q, a

    @staticmethod
    def order_cleanup_products(order_id, valid_product_ids):
        q = '''
   DELETE p, q
     FROM order_product p
LEFT JOIN order_product_quantity q ON p.id=q.product_id
    WHERE p.order_id=%s'''
        a = [order_id]

        if valid_product_ids:
            q += ' AND p.id NOT IN %s'
            a.append(set(valid_product_ids))

        return q, a

    @staticmethod
    def order_cleanup_quantities(product_id, valid_quantity_ids):
        q = 'DELETE FROM order_product_quantity WHERE product_id=%s'
        a = [product_id]

        if valid_quantity_ids:
            q += ' AND id NOT IN %s'
            a.append(set(valid_quantity_ids))

        return q, a

    @staticmethod
    def order_insert_product(order_id, position, product):
        return 'INSERT INTO order_product (order_id, position, description) VALUES (%s, %s, %s)', [
            order_id,
            position,
            product.get('description'),
        ]

    @staticmethod
    def order_update_product(order_id, product_id, position, product):
        return 'UPDATE order_product SET position=%s, description=%s WHERE id=%s AND order_id=%s', [
            position,
            product.get('description'),
            product_id,
            order_id,
        ]

    @staticmethod
    def order_insert_product_quantity(product_id, position, quantity):
        return '''
INSERT INTO order_product_quantity (product_id, position, description, amount, max) VALUES (%s, %s, %s, %s, %s)''', [
            product_id,
            position,
            quantity.get('description'),
            parse_decimal(quantity.get('amount')),
            quantity.get('max', 0)
        ]

    @staticmethod
    def order_update_product_quantity(product_id, quantity_id, position, quantity):
        return '''
UPDATE order_product_quantity SET position=%s, description=%s, amount=%s, max=%s WHERE product_id=%s AND id=%s''', [
            position,
            quantity.get('description'),
            parse_decimal(quantity.get('amount')),
            quantity.get('max', 0),
            product_id,
            quantity_id,
        ]

    @staticmethod
    def order_remove(order_id):
        return '''
   DELETE o, oref, dp, p, pq, po, poq
     FROM order_definition o
LEFT JOIN order_referent oref ON oref.order_id=o.id
LEFT JOIN order_delivery_date dp ON dp.order_id=o.id
LEFT JOIN order_product p ON p.order_id=o.id
LEFT JOIN order_product_quantity pq ON pq.product_id=p.id
LEFT JOIN purchase_order po ON po.order_id=o.id
LEFT JOIN purchase_order_quantity poq ON poq.order_id=po.id
    WHERE o.id=%s
''', [
            order_id,
        ]

    @staticmethod
    def order_cleanup_deliveries(order_id):
        return 'DELETE FROM order_delivery_date WHERE order_id=%s', [order_id]

    @staticmethod
    def order_lock(order_id, order_lock):
        return 'UPDATE order_definition SET `lock`=`lock`+1 WHERE id=%s AND `lock`=%s', [order_id, order_lock]

    @staticmethod
    def order_insert_deliveries(order_id, deliveries):
        q = 'INSERT INTO order_delivery_date (order_id, delivery_date_id) VALUES ' + ', '.join(
            ['(%s, %s)'] * len(deliveries)
        )
        a = [x
             for d in deliveries
             for x in (order_id, d['delivery_date_id'])
             ]
        return q, a

    #@staticmethod
    #def order_remove_product(order_id):
    #    return '', []

    #@staticmethod
    #def order_remove_product_quantity(order_id):
    #    return '', []

    @staticmethod
    def order_change_state(order_id, lock, to_state):
        return 'UPDATE order_definition SET state=%s, `lock`=`lock`+1 WHERE id=%s AND `lock`=%s', [
            to_state, order_id, lock
        ]

    def order_check_delivery_date(self, order_id, delivery_date_id):
        return '''
SELECT count(*)
  FROM delivery_date dd
  JOIN delivery_place dp ON dp.id = dd.delivery_place_id
  JOIN order_definition d ON dp.csa_id=d.csa_id
 WHERE dd.id=%s AND d.id=%s
''', [delivery_date_id, order_id]

    def orders_search(self, csa_id, states, from_idx, to_idx):
        q = '''
SELECT o.id, o.state, o.description, o.notes, o.submission_exp, o.account_threshold, o.profile_required,
       c.id as "currency_id", c.symbol
  FROM order_definition o
  JOIN currency c ON o.currency_id=c.id
  WHERE o.csa_id=%s'''
        a = [csa_id]

        if states is not None:
            q += ' AND o.state IN %s'
            a.append(set(states))

        q += ' ORDER BY ISNULL(o.submission_exp), o.submission_exp ASC'

        if from_idx:
            q += ' LIMIT %s OFFSET %s'
            a.extend([to_idx - from_idx + 1, from_idx])

        return q, a

    def orders_count(self, csa_id, states):
        q = '''
        SELECT count(*)
          FROM order_definition o
          WHERE o.csa_id=%s'''
        a = [csa_id]

        if states is not None:
            q += ' AND o.state IN %s'
            a.append(set(states))

        return q, a

    def order_purchase_of_order(self, order_id, person_id):
        return '''
   SELECT po.id, po.account_id, po.delivery_place_id, po.delivery_date_id, po.created, po.last_modified,
          po.order_id, po.order_lock,
          q.quantity_id, q.quantity
     FROM purchase_order po
LEFT JOIN purchase_order_quantity q ON po.id=q.order_id
     JOIN account_person ap ON po.account_id=ap.account_id
    WHERE po.order_id=%s AND ap.person_id=%s
        ''', [order_id, person_id]

    def order_purchase_of_order_slim(self, order_id, person_id):
        return '''
   SELECT po.id, po.account_id
     FROM purchase_order po
     JOIN account_person ap ON po.account_id=ap.account_id
    WHERE po.order_id=%s AND ap.person_id=%s
        ''', [order_id, person_id]

    @staticmethod
    def purchase_order_new(order_id, order_lock, account_id, delivery_date_id, delivery_place_id):
        return '''
INSERT INTO purchase_order (order_id, order_lock, account_id, created, delivery_date_id, delivery_place_id) 
     VALUES                (%s,       %s,         %s,         now(),   %s,               %s)
        ''', [order_id, order_lock, account_id, delivery_date_id, delivery_place_id]

    @staticmethod
    def purchase_order_update(
                db_purchase_order_id,
                order_lock,
                # last_modified
                delivery_date_id,
                delivery_place_id,
            ):
        return '''
UPDATE purchase_order
   SET order_lock=%s,
       delivery_date_id=%s,
       delivery_place_id=%s
 WHERE id=%s''', [order_lock, delivery_date_id, delivery_place_id, db_purchase_order_id]

    @staticmethod
    def purchase_order_clean_quantities(db_purchase_order_id):
        return 'DELETE FROM purchase_order_quantity WHERE quantity_id=%s', [db_purchase_order_id]

    @staticmethod
    def purchase_order_insert_quantities(db_purchase_order_id, quantities):
        return 'INSERT INTO purchase_order_quantity (order_id, quantity_id, quantity) VALUES ' + ', '.join(
            ['(%s, %s, %s)'] * len(quantities)
        ), [x
            for quantity_id, quantity in quantities.items()
            for x in (db_purchase_order_id, quantity_id, quantity)
            ]

    @staticmethod
    def purchase_order_remove(user_id, order_id):
        q = '''
           DELETE p, q
             FROM purchase_order p
        LEFT JOIN purchase_order_quantity q ON p.id=q.order_id
             JOIN account_person ap ON ap.account_id=p.account_id
            WHERE p.order_id=%s AND ap.person_id=%s'''
        a = [order_id, user_id]

        return q, a

    @staticmethod
    def reports(profile: str) -> SqlQuery:
        return 'SELECT * FROM reports_configuration WHERE profile=%s', [profile]

    @staticmethod
    def template(name):
        return 'SELECT template FROM templates WHERE name=%s', [name]

    @staticmethod
    def template_update(name, content):
        return 'UPDATE templates SET template=%s WHERE name=%s', [content, name]

    @staticmethod
    def template_insert(name, content):
        return 'INSERT INTO templates (name, template) VALUES (%s, %s)', [name, content]

    @staticmethod
    def connection_check():
        return 'SELECT 1'

    @staticmethod
    def column_names(cur):
        return [f[0] for f in cur.description]

    def iter_objects(self, cur):
        cn = self.column_names(cur)
        return [dict(zip(cn, x)) for x in list(cur)]

    def fetch_object(self, cur, return_if_none=None):
        v = cur.fetchone()
        return dict(zip(self.column_names(cur), v)) if v else return_if_none

    def fetch_struct(self, cur):
        def seqmode(c, mk, mv):
            c.append(mv)
            return mv

        def mapmode(c, mk, mv):
            return c.setdefault(mk, mv)

        seqmode.value = lambda: []
        mapmode.value = lambda: {}
        r = {}
        row = cur.fetchone()
        if row is None:
            raise Exception('no rows feched')
        for k, v in zip(self.column_names(cur), row):
            pp = k.split('__')
            if len(pp) > 1:
                t = r
                mode = mapmode
                nextmode = None
                for p in pp[:-1]:
                    if p.endswith('['):
                        p = p[:-1]
                        nextmode = seqmode
                    else:
                        nextmode = mapmode
                    t = mode(t, p, nextmode.value())
                    mode = nextmode
                mode(t, pp[-1], v)
            else:
                r[k] = v
        return r
