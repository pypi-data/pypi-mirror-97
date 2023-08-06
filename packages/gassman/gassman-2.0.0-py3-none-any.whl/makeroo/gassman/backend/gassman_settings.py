"""
Created on 03/mar/2014

@author: makeroo
"""

LOG = {
    'version': 1,
    'root': {
        'level': 'DEBUG',
        'handlers': ['codeHandler'],
    },
    'loggers': {
        'tornado.access': {
            'level': 'DEBUG',
            'handlers': ['accessHandler'],
            'qualname': 'access',
            'propagate': 0
        },
    },
    'handlers': {
        'codeHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simpleFormatter',
            'stream': 'ext://sys.stdout',
        },
        'accessHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simpleFormatter',
            'stream': 'ext://sys.stdout',
        },
    },
    'formatters': {
        'simpleFormatter': {
            '()': 'makeroo.loglib.ColoredFormatter',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '',
            'colors': {
                'CRITICAL': '$RED$BOLD',
                'FATAL': '$RED$BOLD',
                'ERROR': '$RED',
                'WARNING': '$YELLOW',
                'INFO': '',
                'DEBUG': '$CYAN',
            },
        },
    },
}
