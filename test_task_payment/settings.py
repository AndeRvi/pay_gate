import os

LOG_FORMAT = '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s'

base_setting = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///payment.db',
    'PIASTRIX_SHOP_ID': 5,
    'PIASTRIX_SECRET_KEY': "SecretKey01",
    'PIASTRIX_BASE_URL': 'https://core.piastrix.com/',
}

class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = base_setting.get('SQLALCHEMY_DATABASE_URI')
    PIASTRIX_SHOP_ID = base_setting.get('PIASTRIX_SHOP_ID')
    PIASTRIX_SECRET_KEY = base_setting.get('PIASTRIX_SECRET_KEY')
    PIASTRIX_BASE_URL = base_setting.get("PIASTRIX_BASE_URL")


