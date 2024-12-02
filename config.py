from decouple import config 
class Config:
    SECRET_KEY = '|b2Jqw)h)35LHmKX'

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST='swalbd2024.c9soamye8quw.us-east-1.rds.amazonaws.com'
    MYSQL_USER='admin'
    MYSQL_PASSWORD='Adminroot'
    MYSQL_DB='swal_bd2'
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS = True
    MAIL_USERNAME='20213tn161@utez.edu.mx'
    MAIL_PASSWORD=''
    
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
#FS/5o3f71KbIPv@]
