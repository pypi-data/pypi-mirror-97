import logging
from datetime import timedelta

from ...cfglib import cfg_bool, env, optional, required_str


logger = logging.getLogger(__name__)


class Configuration:
    published_url = env('PUBLISHED_URL', required_str)

    debug_mode = env('DEBUG_MODE', cfg_bool)

    smtp_server = env('SMTP_SERVER', required_str)
    smtp_port = env('SMTP_PORT', int, 25)
    smtp_sender = env('SMTP_SENDER', str, 'gassman@gassmanager.org')
    smtp_num_threads = env('SMTP_NUM_THREADS', int, 2)
    smtp_queue_timeout = env('SMTP_QUEUE_TIMEOUT', float, 3)

    http_port = env('HTTP_PORT', int, 8180)

    db_host = env('DB_HOST', str, 'db')
    db_port = env('DB_PORT', int, 3306)
    db_user = env('DB_USER', str, 'mysql')
    db_password = env('DB_PASSWORD', str, 'example')
    db_name = env('DB_NAME', str, 'gassman')
    db_check_interval = timedelta(seconds=env('DB_CHECK_INTERVAL', float, 60))

    cookie_secret = env('COOKIE_SECRET', required_str)
    cookie_max_age_days = env('COOKIE_MAX_AGE_DAYS', float, 31)

    keycloak_client_id = env('KEYCLOAK_CLIENT_ID', str, 'gassman')
    keycloak_realm_name = env('KEYCLOAK_REALM_NAME', str, 'gassman')
    keycloak_published_url = env('KEYCLOAK_PUBLISHED_URL', str, '/auth')
    # keycloak_return_url = env('KEYCLOAK_RETURN_URL', str, '/gm/auth/keycloak_return')
    keycloak_server_url = env('KEYCLOAK_SERVER_URL', str, 'http://keycloak:8080/auth')
    nonce_duration = timedelta(seconds=env('NONCE_DURATION', float, 60))

    # TODO: restore google

    devops_email = env('DEVOPS_EMAIL', optional)
