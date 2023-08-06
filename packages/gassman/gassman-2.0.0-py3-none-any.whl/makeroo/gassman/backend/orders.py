import logging

from ..i18n_utils import parse_decimal

from .web import JsonBaseHandler, GDataException
from . import error_codes


logger = logging.getLogger(__name__)


class OrdersFetch (JsonBaseHandler):
    def do(self, cur):
        order_id = self.payload['order_id']
        uid = self.current_user

        if uid is None:
            raise GDataException(error_codes.E_not_authenticated, 401)

        # autorizzazioni:
        # un permesso può essere visto da tutti i membri di un gas
        #  purché non sia draft
        # se è draft può essere visto solo da i membri del gas che hanno permesso canPlaceOrders

        q, a = self.application.conn.sql_factory.order_fetch(order_id)
        cur.execute(q, a)

        r = self.application.conn.sql_factory.fetch_object(cur)

        if r is None:
            return None

        csa_id = r['csa_id']
        state = r['state']

        if not(
                self.application.has_permission_by_csa(
                    cur, self.application.conn.sql_factory.P_canPlaceOrders, uid, csa_id
                ) if state != self.application.conn.sql_factory.Os_draft else
                self.application.is_member_of_csa(cur, uid, csa_id, False)
        ):
            raise GDataException(error_codes.E_permission_denied, 403)

        q, a = self.application.conn.sql_factory.order_delivery(order_id)
        cur.execute(q, a)
        r['delivery'] = self.application.conn.sql_factory.iter_objects(cur)

        q, a = self.application.conn.sql_factory.order_products(order_id)
        cur.execute(q, a)
        products_array = self.application.conn.sql_factory.iter_objects(cur)

        r['products'] = products_array

        if products_array:
            products_index = {
                p['id']: p
                for p in products_array
            }

            q, a = self.application.conn.sql_factory.order_product_quantities(order_id)
            cur.execute(q, a)

            for q in self.application.conn.sql_factory.iter_objects(cur):
                p = products_index[q['product']]
                p.setdefault('quantities', []).append(q)

        return r


class OrdersSave (JsonBaseHandler):
    def do(self, cur):
        order_draft = self.payload
        uid = self.current_user

        if uid is None:
            raise GDataException(error_codes.E_not_authenticated, 401)

        try:
            order_id = order_draft['id']
            csa_id = order_draft['csa_id']
            cleanup_products = order_draft['state'] == self.application.conn.sql_factory.Os_draft and order_id != 'new'

            if order_draft['profile_required'] not in ('Y', 'N'):
                raise GDataException(error_codes.E_illegal_payload)

            for p in order_draft['products']:
                for q in p.get('quantities', []):
                    amount = parse_decimal(q.get('amount'), as_decimal=True)
                    if amount is None:
                        continue
                    if float(amount) < 0.0:
                        raise GDataException(error_codes.E_illegal_amount)
        except KeyError:
            raise GDataException(error_codes.E_illegal_payload)
        except ValueError:
            raise GDataException(error_codes.E_illegal_amount)

        if not self.application.has_permission_by_csa(
                    cur, self.application.conn.sql_factory.P_canPlaceOrders, uid, csa_id
                ):
            raise GDataException(error_codes.E_permission_denied, 403)

        if order_id == 'new':
            # nuovo ordine
            q, a = self.application.conn.sql_factory.order_save(order_draft)
            cur.execute(q, a)
            order_id = cur.lastrowid
        else:
            # aggiornamento ordine
            q, a = self.application.conn.sql_factory.order_update(order_draft)
            cur.execute(q, a)
            if cur.rowcount == 0:
                q, a = self.application.conn.sql_factory.order_exists(order_id)
                cur.execute(q, a)
                raise GDataException(error_codes.E_illegal_order if cur.fetchone()[0] == 0 else
                                     error_codes.E_already_modified)
            elif cur.rowcount > 1:
                logger.error('inconsistent db? update order, wrong rowcount: order=%s, rowcount=%s',
                                  order_id, cur.rowcount)
                raise GDataException(error_codes.E_illegal_order)

            #q, a = self.application.conn.sql_factory.order_cleanup_products(order_id)
            #cur.execute(q, a)

        try:
            products = order_draft['products']

            if cleanup_products:
                q, a = self.application.conn.sql_factory.order_cleanup_products(
                    order_id,
                    [p['id'] for p in products if p.get('id') is not None]
                )
                cur.execute(q, a)

            for p, idx in zip(products, range(len(products))):
                quantities = p.get('quantities', [])

                product_id = p.get('id')
                if product_id is None:
                    q, a = self.application.conn.sql_factory.order_insert_product(
                        order_id, idx, p
                    )
                else:
                    q, a = self.application.conn.sql_factory.order_update_product(
                        order_id, product_id, idx, p
                    )
                cur.execute(q, a)
                if product_id is None:
                    product_id = cur.lastrowid

                if cleanup_products:
                    q, a = self.application.conn.sql_factory.order_cleanup_quantities(
                        product_id,
                        [quantity['id'] for quantity in quantities if quantity.get('id') is not None]
                    )
                    cur.execute(q, a)

                for quantity, qidx in zip(quantities, range(len(quantities))):
                    quantity_id = quantity['id']

                    if quantity_id is None:
                        q, a = self.application.conn.sql_factory.order_insert_product_quantity(
                            product_id, qidx, quantity
                        )
                    else:
                        q, a = self.application.conn.sql_factory.order_update_product_quantity(
                            product_id, quantity_id, qidx, quantity
                        )
                    cur.execute(q, a)
        except (KeyError, TypeError):
            raise GDataException(error_codes.E_illegal_payload)

        return [order_id]


class OrdersRemove (JsonBaseHandler):
    def do(self, cur):
        order_draft = self.payload
        uid = self.current_user

        if uid is None:
            raise GDataException(error_codes.E_not_authenticated, 401)

        try:
            order_id = order_draft['order_id']
            # order_lock = order_draft['lock']
        except KeyError:
            raise GDataException(error_codes.E_illegal_payload)

        if not self.application.has_permission_by_order(
                    cur, self.application.conn.sql_factory.P_canPlaceOrders, uid, order_id
                ):
            raise GDataException(error_codes.E_permission_denied, 403)

        q, a = self.application.conn.sql_factory.order_remove(order_id)
        cur.execute(q, a)

        if cur.rowcount == 0:
            raise GDataException(error_codes.E_already_modified)


class OrdersUpdateDeliveries (JsonBaseHandler):
    def do(self, cur):
        uid = self.current_user
        p = self.payload

        try:
            order_id = p['order_id']
            order_lock = p['lock']
            deliveries = p['deliveries']
        except KeyError:
            raise GDataException(error_codes.E_illegal_payload)

        if not self.application.has_permission_by_order(
                    cur, self.application.conn.sql_factory.P_canPlaceOrders, uid, order_id
                ):
            raise GDataException(error_codes.E_permission_denied, 403)

        q, a = self.application.conn.sql_factory.order_lock(order_id, order_lock)
        cur.execute(q, a)

        if cur.rowcount == 0:
            raise GDataException(error_codes.E_already_modified)

        q, a = self.application.conn.sql_factory.order_cleanup_deliveries(order_id)
        cur.execute(q, a)

        if deliveries:
            q, a = self.application.conn.sql_factory.order_insert_deliveries(order_id, deliveries)
            cur.execute(q, a)


class OrdersOpen (JsonBaseHandler):
    def do(self, cur):
        order_draft = self.payload
        uid = self.current_user

        if uid is None:
            raise GDataException(error_codes.E_not_authenticated, 401)

        try:
            order_id = order_draft['order_id']
            order_lock = order_draft['lock']
        except KeyError:
            raise GDataException(error_codes.E_illegal_payload)

        if not self.application.has_permission_by_order(
                    cur, self.application.conn.sql_factory.P_canPlaceOrders, uid, order_id
                ):
            raise GDataException(error_codes.E_permission_denied, 403)

        q, a = self.application.conn.sql_factory.order_change_state(
            order_id,
            order_lock,
            self.application.conn.sql_factory.Os_open
        )
        cur.execute(q, a)

        if cur.rowcount == 0:
            raise GDataException(error_codes.E_already_modified)


class OrdersSearch (JsonBaseHandler):
    def do(self, cur, csa_id, from_idx, to_idx):
        uid = self.current_user
        p = self.payload
        state = p.get('state', self.application.conn.sql_factory.Os_open)

        if not(
                self.application.has_permission_by_csa(
                    cur, self.application.conn.sql_factory.P_canPlaceOrders, uid, csa_id
                ) if state != self.application.conn.sql_factory.Os_draft else
                self.application.is_member_of_csa(cur, uid, csa_id, False)
        ):
            raise GDataException(error_codes.E_permission_denied, 403)

        q, a = self.application.conn.sql_factory.orders_search(
            csa_id,
            state,
            int(from_idx),
            int(to_idx)
        )
        cur.execute(q, a)

        r = {
            'items': self.application.conn.sql_factory.iter_objects(cur),
        }

        if len(r['items']):
            q, a = self.application.conn.sql_factory.orders_count(csa_id, state)
            cur.execute(q, a)

            r['count'] = cur.fetchone()[0]
        else:
            r['count'] = 0

        return r


class OrdersDeliveries (JsonBaseHandler):
    def do(self, cur, csa_id):
        uid = self.current_user
        p = self.payload
        order_ids = p['order_ids']

        if self.application.has_permission_by_csa(
            cur, self.application.conn.sql_factory.P_canPlaceOrders, uid, csa_id
        ):
            state = None
        elif self.application.is_member_of_csa(cur, uid, csa_id, False):
            state = self.application.conn.sql_factory.Os_draft
        else:
            raise GDataException(error_codes.E_permission_denied, 403)

        q, a = self.application.conn.sql_factory.order_delivery(order_ids, state)
        cur.execute(q, a)

        return self.application.conn.sql_factory.iter_objects(cur)


class OrdersPurchaseOrderHandler (JsonBaseHandler):
    def do(self, cur):
        uid = self.current_user
        p = self.payload
        order_id = p['order_id']

        q, a = self.application.conn.sql_factory.order_purchase_of_order(order_id, uid)
        cur.execute(q, a)

        rows = self.application.conn.sql_factory.iter_objects(cur)

        if len(rows):
            po = rows[0]

            po['quantities'] = {
                row['quantity_id']: row['quantity']
                for row in rows
            }

            po.pop('quantity_id')
            po.pop('quantity')

            return po
        else:
            return None


class OrdersPurchaseOrderSaveHandler (JsonBaseHandler):
    def do(self, cur):
        uid = self.current_user
        p = self.payload

        if uid is None:
            raise GDataException(error_codes.E_not_authenticated, 401)

        try:
            purchase_order_id = p['id']
            order_id = p['order_id']
            order_lock = p['order_lock']
            account_id = p['account_id']

            delivery_date_id = p.get('delivery_date_id')
            delivery_place_id = p.get('delivery_place_id')

            quantities = {
                k: v
                for k, v in p['quantities'].items()
                if v > 0
            }
        except (AttributeError, KeyError, TypeError):
            raise GDataException(error_codes.E_illegal_payload)

        if not quantities:
            raise GDataException(error_codes.E_illegal_payload)

        # requirements to be allowed to modify a purchase order:
        # 1. given order lock match order definition lock
        # 2. order definition state is open
        # 3. the user is the issuer (ie. account owner) OR the order referent

        q, a = self.application.conn.sql_factory.order_state(order_id)
        cur.execute(q, a)
        row = cur.fetchone()
        if row is None:
            raise GDataException(error_codes.E_illegal_order)
        if row[0] != self.application.conn.sql_factory.Os_open:
            raise GDataException(error_codes.E_purchase_order_no_more_allowed)
        if row[1] != order_lock:
            raise GDataException(error_codes.E_already_modified)

        if self.application.has_account(cur, uid, account_id):
            owner = True
        else:
            q, a = self.application.conn.sql_factory.order_definition_is_referent(order_id, uid)
            cur.execute(q, a)

            if cur.fetchone()[0]:
                owner = False
            else:
                raise GDataException(error_codes.E_permission_denied, 403)

        # delivery date/place validation

        if delivery_date_id is not None:
            q, a = self.application.conn.sql_factory.order_check_delivery_date(
                order_id,
                delivery_date_id
            )
            cur.execute(q, a)

            if cur.fetchone()[0] == 0:
                raise GDataException(error_codes.E_permission_denied, 403)

        elif delivery_place_id is not None:
            q, a = self.application.conn.sql_factory.delivery_place_check_by_order(
                order_id,
                delivery_place_id
            )
            cur.execute(q, a)

            if cur.fetchone()[0] == 0:
                raise GDataException(error_codes.E_permission_denied, 403)

        else:
            logger.error('purchase_order without ddate and dplace: id=%s', purchase_order_id)
            raise GDataException(error_codes.E_illegal_payload)

        # verify that there is purchase_order for every (order_def, account) at most

        q, a = self.application.conn.sql_factory.order_purchase_of_order_slim(order_id, uid)
        cur.execute(q, a)
        row = cur.fetchone()

        if row is None:
            if purchase_order_id != 'new':
                logger.error('purchase_order_does_not_exist, ignoring: id=%s, user=%s, order=%s',
                                  purchase_order_id, uid, order_id)

            if not owner:
                logger.info('purchase_order creation delegated: referent=%s, order=%s, account=%s',
                                 uid, order_id, account_id)

            q, a = self.application.conn.sql_factory.purchase_order_new(
                order_id,
                order_lock,
                account_id,
                # created
                # last_modified
                delivery_date_id,
                delivery_place_id,
            )
            cur.execute(q, a)
            db_purchase_order_id = cur.lastrowid
        else:
            db_purchase_order_id = row[0]

            if purchase_order_id == 'new':
                logger.error(
                    'trying to create new purchase_order, ignoring and updating: id=%s, user=%s, order=%s',
                    db_purchase_order_id, uid, order_id
                )

            q, a = self.application.conn.sql_factory.purchase_order_update(
                db_purchase_order_id,
                order_lock,
                # last_modified
                delivery_date_id,
                delivery_place_id,
            )
            cur.execute(q, a)

            q, a = self.application.conn.sql_factory.purchase_order_clean_quantities(db_purchase_order_id)
            cur.execute(q, a)

        q, a = self.application.conn.sql_factory.purchase_order_insert_quantities(db_purchase_order_id, quantities)
        cur.execute(q, a)

        return [db_purchase_order_id]


class OrdersPurchaseOrderRemoveHandler (JsonBaseHandler):
    def do(self, cur):
        uid = self.current_user
        p = self.payload
        order_id = p['order_id']

        if uid is None:
            raise GDataException(error_codes.E_not_authenticated, 401)

        q, a = self.application.conn.sql_factory.purchase_order_remove(uid, order_id)
        cur.execute(q, a)

        return {
            'removed': cur.rowcount > 0,
        }
