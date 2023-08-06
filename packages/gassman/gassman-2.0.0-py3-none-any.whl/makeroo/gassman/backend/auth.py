import uuid
import logging
from datetime import timedelta

from urllib.parse import urlencode

from tornado.web import RequestHandler
from tornado.auth import GoogleOAuth2Mixin, OAuth2Mixin
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.escape import json_decode
from tornado.ioloop import IOLoop

from ... import oauth2lib


logger = logging.getLogger(__name__)


class GoogleUser (object):
    authenticator = 'Google2'

    def __init__(self, id_token):
        oauth2token = oauth2lib.extract_payload_from_oauth2_id_token(id_token['id_token'])
        self.userId = oauth2token['sub']
        self.email = oauth2token['email']
        self.access_token = id_token['access_token']

    @coroutine
    def load_full_profile(self):
        http = AsyncHTTPClient()

        response = yield http.fetch(
            'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + self.access_token,
            method="GET"
        )
        if response.error:
            raise Exception('Google auth error: %s' % str(response))

        profile = json_decode(response.body)
        self.firstName = profile.get('given_name')
        self.middleName =  None
        self.lastName = profile.get('family_name')
        self.gProfile = profile.get('link')
        self.picture = profile.get('picture')
        # altri attributi: id, email, gender, locale


class GoogleAuthLoginHandler (RequestHandler, GoogleOAuth2Mixin):
    @coroutine
    def get(self):
        if self.get_argument('code', False):
            id_token = yield self.get_authenticated_user(
                redirect_uri=self.settings['google_oauth_redirect'],
                code=self.get_argument('code')
                )
            token_user = GoogleUser(id_token)
            # check_profile ritorna person ma a me interessa solo la registrazione su db
            yield self.application.check_profile(self, token_user)
            self.redirect("/home.html")
        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings['google_oauth_redirect'],
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


class AuthenticationSessionManager:
    def __init__(self, nonce_duration: timedelta) -> None:
        self.nonce_duration = nonce_duration

        self.nonces = {}

    def new_session(self) -> str:
        nonce = str(uuid.uuid4())

        logger.info('authentication session started: nonce=%s', nonce)

        def invalidate_nonce():
            logger.info('authentication session expired: nonce=%s', nonce)

            self.nonces.pop(nonce, None)

        ioloop = IOLoop.current()

        timeout_handle = ioloop.add_timeout(self.nonce_duration, invalidate_nonce)

        self.nonces[nonce] = timeout_handle

        return nonce

    def validate_nonce(self, nonce: str) -> None:
        timeout_handle = self.nonces.pop(nonce, None)

        if timeout_handle is None:
            raise KeyError('nonce expired')

        ioloop = IOLoop.current()

        ioloop.remove_timeout(timeout_handle)

        logger.info('authentication session succeded: nonce=%s', nonce)


class KeycloakUser (object):
    authenticator = 'Keycloak'

    def __init__(self, serverl_url: str, realm_name: str, id_token):
        self.serverl_url = serverl_url
        self.realm_name = realm_name

        oauth2token = oauth2lib.extract_payload_from_oauth2_id_token(id_token['id_token'])

        self.userId = oauth2token['sub']
        self.email = oauth2token['email']
        self.access_token = id_token['access_token']
        self.username = oauth2token['preferred_username']
        self.nonce = oauth2token['nonce']
        # other keys: exp, iat, auth_time: unix time
        # jti: uuid (?)
        # iss: issuer, keycloak url
        # aud: realm
        # typ: ID
        # azp: realm?
        # at_hash: ?
        # acr: ?
        # session_state: ?

    async def load_full_profile(self):
        http = AsyncHTTPClient()

        req = HTTPRequest(
            f'{self.serverl_url}/realms/{self.realm_name}/protocol/openid-connect/userinfo',
            method="GET",
            headers={
                'Authorization': f'Bearer {self.access_token}',
            }
        )

        response = await http.fetch(req)

        if response.error:
            raise Exception('Keycloak auth error: %s' % str(response))

        profile = json_decode(response.body)

        self.firstName = profile.get('given_name')
        self.middleName =  None
        self.lastName = profile.get('family_name')
        self.gProfile = profile.get('link')
        self.picture = profile.get('picture')
        # altri attributi: id, email, gender, locale

    def __str__(self) -> str:
        return f'{self.email} {self.username} {self.userId}'


class KeycloakOAuth2Mixin (OAuth2Mixin):
    # server_url =
    # realm_name =
    # client_id =

    @property
    def obtain_from_code_url(self):
        return f'{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/token'

    async def get_authenticated_user(
        self, redirect_uri: str, code: str
    ) -> dict[str, any]:
        http_client = AsyncHTTPClient()

        req = HTTPRequest(
            self.obtain_from_code_url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            method='POST',
            body=urlencode({
                'client_id': self.client_id,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
                # 'client_session_state': None,
                # 'client_session_host': None,
            }).encode('ascii'),
        )

        resp = await http_client.fetch(req)

        token = json_decode(resp.body)

        return token


class KeycloakAuthLoginStartHandler (RequestHandler, KeycloakOAuth2Mixin):
    def initialize(self, published_url: str, keycloak_published_url: str, serverl_url: str, realm_name: str, client_id: str, authentication_session_manager: AuthenticationSessionManager) -> None:
        self.published_url = published_url
        self.keycloak_published_url = keycloak_published_url
        self.server_url = serverl_url
        self.realm_name = realm_name
        self.client_id = client_id
        self.authentication_session_manager = authentication_session_manager

        self.redirect_url = f'{self.published_url}/gm/auth/keycloak_return'
        self._OAUTH_AUTHORIZE_URL = f'{self.keycloak_published_url}/realms/{self.realm_name}/protocol/openid-connect/auth'

    async def get(self):
        state = str(uuid.uuid4())

        nonce = self.authentication_session_manager.new_session()

        logger.debug('generated: nonce=%s, state=%s', nonce, state)

        self.authorize_redirect(
            redirect_uri=self.redirect_url,
            client_id=self.client_id,
            response_type='code',
            scope=['openid'],
            extra_params={
                'nonce': nonce,
                'state': state,
                'response_mode': 'fragment',
            },
        )

    async def post(self):
        state = self.get_argument('state')
        session_state = self.get_argument('session_state')
        code = self.get_argument('code')

        id_token = await self.get_authenticated_user(
            redirect_uri=self.redirect_url,
            code=code
        )

        token_user = KeycloakUser(self.server_url, self.realm_name, id_token)

        try:
            self.authentication_session_manager.validate_nonce(token_user.nonce)

            # check_profile ritorna person ma a me interessa solo la registrazione su db
            await self.application.check_profile(self, token_user)

        except KeyError:
            # present home.html again, it will return to the login state
            # TODO: present some error

            pass

        self.redirect("/home.html")

    def check_xsrf_cookie(self):
        pass


class KeycloakAuthLoginEndHandler (RequestHandler):
    def get(self):
        self.render('keycloak_return.html')


class AuthLogoutHandler (RequestHandler):
    def initialize(self, published_url: str, keycloak_published_url: str, realm_name: str) -> None:
        self.keycloak_published_url = keycloak_published_url
        self.realm_name = realm_name

        self.redirect_url = f'{published_url}/home.html'

    def get(self):
        self.redirect(f'{self.keycloak_published_url}/realms/{self.realm_name}/protocol/openid-connect/logout?redirect_uri={self.redirect_url}')


class AuthXsrfHandler (RequestHandler):
    def get(self):
        self.xsrf_token  # generate the _xsrf cookie
