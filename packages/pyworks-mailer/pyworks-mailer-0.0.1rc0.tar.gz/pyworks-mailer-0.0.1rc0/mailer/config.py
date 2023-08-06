import os
from dotenv import load_dotenv
from .utils import scandir

load_dotenv()


class Config(object):

    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MAIL_PROVIDER_SUPPORTED = ['gmail', 'yandex', 'ses']
        self.MAIL_PROVIDER = os.getenv('MAIL_PROVIDER')
        self.MAIL_HOST = os.getenv('MAIL_HOST')
        self.MAIL_PORT = os.getenv('MAIL_PORT')
        self.MAIL_TLS = os.getenv('MAIL_TLS', True)
        self.MAIL_USERNAME = os.getenv('MAIL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
        self.MAIL_RECEIVERS = os.getenv('MAIL_RECEIVERS')

        if self.MAIL_RECEIVERS is not None and self.MAIL_RECEIVERS.find(',') > -1:
            self.MAIL_RECEIVERS = self.MAIL_RECEIVERS.split(',')

        self.MAIL_TEMPLATES_ROOT = f'{self.ROOT_DIR}/templates'
        self.MAIL_TEMPLATES = scandir(self.MAIL_TEMPLATES_ROOT)

config = Config()
print(config)

