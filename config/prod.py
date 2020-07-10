from config.settings import *
DEBUG = False
ALLOWED_HOSTS = ['*', 'lemorning.cjhgpvhhqfel.ap-northeast-2.rds.amazonaws.com']
INSTALLED_APPS += ['storages',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
        'ATOMIC_REQUESTS': True,
  }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-ap-northeast-2-470546451617'
AWS_STATIC_BUCKET_NAME ='lemorning-django-static'
AWS_S3_REGION_NAME = 'ap-northeast-2'

AWS_S3_CUSTOM_DOMAIN = '%s.s3-%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME )
AWS_S3_STATIC_DOMAIN = '%s.s3-%s.amazonaws.com' % (AWS_STATIC_BUCKET_NAME, AWS_S3_REGION_NAME )
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
AWS_PRIVATE_MEDIA_LOCATION = 'media/private'

AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static'
AWS_MEDIA_LOCATION = 'media'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_STATIC_DOMAIN, AWS_LOCATION)
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

# STATICFILES_STORAGE = ''
DEFAULT_FILE_STORAGE = 'config.storage_backends.PublicMediaStorage'

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://9898247f6897422ba330b484e34659c4@o402738.ingest.sentry.io/5264312",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
