import sys
import logging
import datetime

from tornado.web import Application, StaticFileHandler
from tornado.escape import json_encode

from ... import loglib
from ...tornadolib import PackagedTemplateLoader
from ...static_resource_provider import static_path


from .config import Configuration
from .web import HomeHandler, Person, rss_feed_id
from .auth import AuthenticationSessionManager, KeycloakAuthLoginStartHandler, KeycloakAuthLoginEndHandler, AuthLogoutHandler, AuthXsrfHandler
from .sys import SysVersionHandler
from .account import AccountOwnerHandler, AccountMovementsHandler, AccountAmountHandler, AccountXlsHandler,\
    AccountCloseHandler
from .accounts import AccountsIndexHandler, AccountsNamesHandler
from .transaction import TransactionEditHandler, TransactionSaveHandler
from .transactions import TransactionsEditableHandler
from .csa import CsaInfoHandler, CsaUpdateHandler, CsaListHandler, CsaChargeMembershipFeeHandler,\
    CsaRequestMembershipHandler, CsaDeliveryPlacesHandler, CsaDeliveryDatesHandler, CsaAddShiftHandler,\
    CsaRemoveShiftHandler, CsaCurrenciesHandler
from .rss import RssFeedHandler
from .people import PeopleProfilesHandler, PeopleNamesHandler
from .person import PersonSaveHandler, PersonCheckEmailHandler, PersonSetFeeHandler, PersonPrivacyHandler
from .event import EventSaveHandler, EventRemoveHandler
from . import orders
from .admin import AdminPeopleIndexHandler, AdminPeopleProfilesHandler, AdminPeopleRemoveHandler,\
    AdminPeopleJoinHandler, AdminPeopleAddHandler, AdminPeopleCreateAccountHandler, AdminPeopleCreateHandler,\
    PermissionGrantHandler, PermissionRevokeHandler


logger = logging.getLogger(__name__)


class GassmanWebApp (Application):
    def __init__(self, conn, notify_service, template_loader: PackagedTemplateLoader, configuration: Configuration, authentication_session_manager: AuthenticationSessionManager):

        static_files_path = static_path(__name__)

        handlers = [
            (r'^/home.html$', HomeHandler),
            (r'^/static/(.*)$', StaticFileHandler, {
                'path': static_files_path,
            }),

            (r'^/gm/auth/keycloak$', KeycloakAuthLoginStartHandler, {
                'published_url': configuration.published_url,
                'keycloak_published_url': configuration.keycloak_published_url,
                'serverl_url': configuration.keycloak_server_url,
                'realm_name': configuration.keycloak_realm_name,
                'client_id': configuration.keycloak_client_id,
                'authentication_session_manager': authentication_session_manager,
            }),
            (r'^/gm/auth/keycloak_return$', KeycloakAuthLoginEndHandler),
            (r'^/gm/auth/logout$', AuthLogoutHandler, {
                'published_url': configuration.published_url,
                'keycloak_published_url': configuration.keycloak_published_url,
                'realm_name': configuration.keycloak_realm_name,
            }),
            (r'^/gm/auth/xsrf', AuthXsrfHandler),

            (r'^/gm/sys/version$', SysVersionHandler),

            (r'^/gm/account/(\d+)/owner$', AccountOwnerHandler),
            (r'^/gm/account/(\d+)/movements/(\d+)/(\d+)$', AccountMovementsHandler),
            (r'^/gm/account/(\d+)/amount$', AccountAmountHandler),
            (r'^/gm/account/(\d+)/xls$', AccountXlsHandler),
            (r'^/gm/account/(\d+)/close$', AccountCloseHandler),

            (r'^/gm/accounts/(\d+)/index/(\d+)/(\d+)$', AccountsIndexHandler),
            (r'^/gm/accounts/(\d+)/names$', AccountsNamesHandler),

            (r'^/gm/transaction/(\d+)/(\d+)/edit$', TransactionEditHandler),
            (r'^/gm/transaction/(\d+)/save$', TransactionSaveHandler, {
                'published_url': configuration.published_url,
            }),
            (r'^/gm/transactions/(\d+)/editable/(\d+)/(\d+)$', TransactionsEditableHandler),

            (r'^/gm/csa/(\d+)/info$', CsaInfoHandler),
            (r'^/gm/csa/(\d+)/currencies', CsaCurrenciesHandler),
            (r'^/gm/csa/update$', CsaUpdateHandler),
            (r'^/gm/csa/list', CsaListHandler),
            (r'^/gm/csa/(\d+)/charge_membership_fee$', CsaChargeMembershipFeeHandler),
            (r'^/gm/csa/(\d+)/request_membership$', CsaRequestMembershipHandler),
            (r'^/gm/csa/(\d+)/delivery_places$', CsaDeliveryPlacesHandler),
            (r'^/gm/csa/(\d+)/delivery_dates$', CsaDeliveryDatesHandler),
            (r'^/gm/csa/(\d+)/add_shift', CsaAddShiftHandler),
            (r'^/gm/csa/(\d+)/remove_shift', CsaRemoveShiftHandler),

            (r'^/gm/rss/(.+)$', RssFeedHandler),

            (r'^/gm/people/(null|\d+)/profiles$', PeopleProfilesHandler),
            (r'^/gm/people/(\d+)/names$', PeopleNamesHandler),
            (r'^/gm/person/(null|\d+)/save$', PersonSaveHandler),
            (r'^/gm/person/(\d+)/check_email$', PersonCheckEmailHandler),
            (r'^/gm/person/(\d+)/set_fee$', PersonSetFeeHandler),
            (r'^/gm/person/privacy$', PersonPrivacyHandler),

            (r'^/gm/event/(\d+)/save$', EventSaveHandler),
            (r'^/gm/event/(\d+)/remove$', EventRemoveHandler),

            (r'^/gm/order$', orders.OrdersFetch),
            (r'^/gm/order_save$', orders.OrdersSave),
            (r'^/gm/order_remove$', orders.OrdersRemove),
            (r'^/gm/order_update_deliveries$', orders.OrdersUpdateDeliveries),
            (r'^/gm/order_open$', orders.OrdersOpen),
            (r'^/gm/orders/(\d+)/search/(\d+)/(\d+)$', orders.OrdersSearch),
            (r'^/gm/orders/(\d+)/deliveries$', orders.OrdersDeliveries),

            (r'^/gm/purchase_order$', orders.OrdersPurchaseOrderHandler),
            (r'^/gm/purchase_order_save$', orders.OrdersPurchaseOrderSaveHandler),
            (r'^/gm/purchase_order_remove$', orders.OrdersPurchaseOrderRemoveHandler),

            (r'^/gm/admin/people/index/(\d+)/(\d+)$', AdminPeopleIndexHandler),
            (r'^/gm/admin/people/profiles$', AdminPeopleProfilesHandler),
            (r'^/gm/admin/people/remove$', AdminPeopleRemoveHandler),
            (r'^/gm/admin/people/join$', AdminPeopleJoinHandler, {
                'published_url': configuration.published_url,
            }),
            (r'^/gm/admin/people/add$', AdminPeopleAddHandler, {
                'published_url': configuration.published_url,
            }),
            (r'^/gm/admin/people/create_account$', AdminPeopleCreateAccountHandler),
            (r'^/gm/admin/people/create$', AdminPeopleCreateHandler),

            (r'^/gm/permission/(\d+)/grant$', PermissionGrantHandler),
            (r'^/gm/permission/(\d+)/revoke$', PermissionRevokeHandler),
        ]

        super().__init__(
            handlers=handlers,
            cookie_secret=configuration.cookie_secret,
            template_loader=template_loader,
            xsrf_cookies=True,
            #google_oauth={
            #    "key": configuration.oauth2_client_id,
            #    "secret": configuration.oauth2_secret,
            #},
            #google_oauth_redirect=configuration.oauth2_redirect,
            debug=configuration.debug_mode,

            cookie_max_age_days=configuration.cookie_max_age_days,
        )

        self.conn = conn
        self.notify_service = notify_service
        self.viewable_contact_kinds = [
            self.conn.sql_factory.Ck_Telephone,
            self.conn.sql_factory.Ck_Mobile,
            self.conn.sql_factory.Ck_Email,
            self.conn.sql_factory.Ck_Fax,
            self.conn.sql_factory.Ck_Nickname,
        ]

    def has_account(self, cur, pid, acc_id):
        cur.execute(*self.conn.sql_factory.has_account(pid, acc_id))
        return cur.fetchone()[0] > 0

    def has_or_had_account(self, cur, pid, acc_id):
        cur.execute(*self.conn.sql_factory.has_or_had_account(pid, acc_id))
        return cur.fetchone()[0] > 0

    def add_contact(self, cur, pid, addr, kind, notes):
        if addr:
            cur.execute(*self.conn.sql_factory.create_contact(addr, kind, notes))
            cid = cur.lastrowid
            cur.execute(*self.conn.sql_factory.assign_contact(cid, pid))

    async def check_profile(self, request_handler, user):
        with self.conn.connection().cursor() as cur:
            auth_mode = (user.userId, user.authenticator, self.conn.sql_factory.Ck_Id)

            cur.execute(*self.conn.sql_factory.check_user(*auth_mode))

            pp = list(cur)

            if len(pp) == 0:
                logger.debug('profile not found: credentials=%s', auth_mode)
                auth_mode = (user.email, 'verified', self.conn.sql_factory.Ck_Email)
                cur.execute(*self.conn.sql_factory.check_user(*auth_mode))
                pp = list(cur)

            if len(pp) == 0:
                logger.info('profile not found: credentials=%s', auth_mode)
                p = None
            else:
                p = Person(*pp[0])
                if len(pp) == 1:
                    logger.debug('found profile: credentials=%s, person=%s', auth_mode, p)
                if len(pp) > 1:
                    self.notify_service.notify(
                        subject='[ERROR] Multiple auth id for, check credentials: id=%s, cred=%s' % (p, auth_mode),
                    )

        try:
            await user.load_full_profile()

            attrsToAdd = {
                self.conn.sql_factory.Ck_Email: (user.email, 'verified'),
                self.conn.sql_factory.Ck_Id: (user.userId, user.authenticator),
            }

            attrsToUpdate = {
                self.conn.sql_factory.Ck_GooglePlusProfile: [user.gProfile, None, None],
                self.conn.sql_factory.Ck_Photo: [user.picture, None, None],
            }

            with self.conn.connection().cursor() as cur:
                if p is None:
                    cur.execute(*self.conn.sql_factory.create_person(user.firstName, user.middleName, user.lastName))
                    p_id = cur.lastrowid
                    rfi = rss_feed_id(self.settings['cookie_secret'], p_id)
                    cur.execute(*self.conn.sql_factory.assign_rss_feed_id(p_id, rfi))
                    p = Person(p_id, user.firstName, user.middleName, user.lastName, rfi)
                    logger.info('profile created: newUser=%s', p)
                else:
                    cur.execute(*self.conn.sql_factory.contacts_fetch_all(p.id))
                    for pc_id, a_id, kind, contact_type, addr in list(cur):
                        v = attrsToAdd.get(kind)
                        if v == (addr, contact_type):
                            attrsToAdd.pop(kind)
                            continue
                        v = attrsToUpdate.get(kind)
                        if v is None:
                            continue
                        elif v[0] == addr and v[1] == contact_type:
                            attrsToUpdate.pop(kind)
                        else:
                            v[2] = a_id

                # userId e email eventualmente li vado ad aggiungere
                # picture e gProfile invece li vado a sostituire
                for kind, (addr, ctype) in attrsToAdd.items():
                    if len(addr) > 255:
                        logger.warning('address too long, it will be cropped to 255 chars: person=%s, addr=%s', p.id, addr)

                        addr = addr[:255]

                    self.add_contact(cur, p.id, addr, kind, ctype)

                for kind, (addr, ctype, addrPk) in attrsToUpdate.items():
                    if len(addr) > 255:
                        logger.warning('address too long, it will be cropped to 255 chars: person=%s, addr=%s', p.id, addr)

                        addr = addr[:255]

                    if addrPk is None:
                        self.add_contact(cur, p.id, addr, kind, ctype)
                    else:
                        cur.execute(*self.conn.sql_factory.contact_address_update(addrPk, addr, ctype))

        except:
            etype, evalue, tb = sys.exc_info()
            logger.error('profile creation failed: cause=%s/%s\nfull stacktrace:\n%s',
                              etype, evalue, loglib.TracebackFormatter(tb))
            self.notify_service.notify(
                subject='[ERROR] User profile creation failed',
                body='Cause: %s/%s\nAuthId: %s\nTraceback:\n%s' %
                           (etype, evalue, user, loglib.TracebackFormatter(tb))
            )

        if p is not None:
            request_handler.set_secure_cookie("user", json_encode(p.id))

            # qui registro chi si è autenticato
            with self.conn.connection().cursor() as cur:
                cur.execute(*self.conn.sql_factory.update_last_login(p.id, datetime.datetime.utcnow()))

        return p

#    def session(self, request_handler):
#        xt = request_handler.xsrf_token
#        s = self.sessions.get(xt, None)
#        if s is None:
#            s = Session(self)
#            self.sessions[xt] = s
#        return s

    def check_membership_by_kitty(self, cur, person_id, acc_id):
        cur.execute(*self.conn.sql_factory.check_membership_by_kitty(person_id, acc_id))
        r = int(cur.fetchone()[0]) > 0
        logger.debug('check membership by kitty: user=%s, acc=%s, r=%s', person_id, acc_id, r)
        return r

    def has_permission_by_account(self, cur, perm, person_id, acc_id):
        cur.execute(*self.conn.sql_factory.has_permission_by_account(perm, person_id, acc_id))
        r = int(cur.fetchone()[0]) > 0
        logger.debug('has permission: user=%s, perm=%s, r=%s', person_id, perm, r)
        return r

    def is_member_of_csa(self, cur, person_id, csa_id, stillMember):
        cur.execute(*self.conn.sql_factory.is_user_member_of_csa(person_id, csa_id, stillMember))
        r = int(cur.fetchone()[0]) > 0
        logger.debug('is member: user=%s, csa=%s, still=%s, r=%s', person_id, csa_id, stillMember, r)
        return r

    def has_permission_by_csa(self, cur, perm, person_id, csa_id):
        if perm is None:
            return False
        cur.execute(*self.conn.sql_factory.has_permission_by_csa(perm, person_id, csa_id))
        r = int(cur.fetchone()[0]) > 0
        logger.debug('has permission: user=%s, perm=%s, r=%s', person_id, perm, r)
        return r

    def has_permission_by_order(self, cur, perm, person_id, order_id):
        if perm is None:
            return False
        cur.execute(*self.conn.sql_factory.has_permission_by_order(perm, person_id, order_id))
        r = int(cur.fetchone()[0]) > 0
        logger.debug('has permission: user=%s, perm=%s, r=%s', person_id, perm, r)
        return r

    def has_permissions(self, cur, perms, person_id, csa_id):
        cur.execute(*self.conn.sql_factory.has_permissions(perms, person_id, csa_id))
        r = int(cur.fetchone()[0]) > 0
        logger.debug('has permissions: user=%s, perm=%s, r=%s', person_id, perms, r)
        return r

    def is_kitty_transition_and_is_member(self, cur, trans_id, person_id):
        cur.execute(*self.conn.sql_factory.transaction_on_kitty_and_user_is_member(trans_id, person_id))
        r = int(cur.fetchone()[0]) > 0
        logger.debug('member can view kitty transation: user=%s, trans=%s, r=%s', person_id, trans_id, r)
        return r

    def is_transaction_editor(self, cur, trans_id, person_id):
        """
        Una transazione può essere creata/modificata da chi ha canEnterXX
        o da chi ha manageTrans.
        Per verificare devo risalire la catena delle sovrascritture.
        """
        while trans_id is not None:
            cur.execute(*self.conn.sql_factory.log_transaction_check_operator(person_id, trans_id))
            if cur.fetchone()[0] > 0:
                return True
            cur.execute(*self.conn.sql_factory.transaction_previuos(trans_id))
            l = cur.fetchone()
            trans_id = l[0] if l is not None else None
        return False

    def isInvolvedInTransaction(self, cur, trans_id, person_id):
        while trans_id is not None:
            cur.execute(*self.conn.sql_factory.transaction_is_involved(trans_id, person_id))
            if cur.fetchone()[0] > 0:
                return True
            cur.execute(*self.conn.sql_factory.transaction_previuos(trans_id))
            l = cur.fetchone()
            trans_id = l[0] if l is not None else None
        return False
