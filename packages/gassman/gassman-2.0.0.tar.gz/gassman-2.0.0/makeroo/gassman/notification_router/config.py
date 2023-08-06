import logging
from ...cfglib import cfg_bool, env, optional, required_str


logger = logging.getLogger(__name__)


class Configuration:
    profile = env('PROFILE', required_str)

    db_host = env('DB_HOST', str, 'db')
    db_port = env('DB_PORT', int, 3306)
    db_user = env('DB_USER', str, 'mysql')
    db_password = env('DB_PASSWORD', str, 'example')
    db_name = env('DB_NAME', str, 'gassman')
    db_check_interval = env('DB_CHECK_INTERVAL', float, 60 * 1000)  # 1 minuto TODO use timedelta

    smtp_server = env('SMTP_SERVER', required_str)
    smtp_port = env('SMTP_PORT', int, 25)
    smtp_sender = env('SMTP_SENDER', str, 'gassman@gassmanager.org')
    smtp_num_threads = env('SMTP_NUM_THREADS', int, 2)
    smtp_queue_timeout = env('SMTP_QUEUE_TIMEOUT', float, 3)
