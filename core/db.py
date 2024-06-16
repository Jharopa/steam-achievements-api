from . import settings

DB_CONN_STRING = 'postgres://%s:%s@%s/%s' % (
    settings.POSTGRES_USER,
    settings.POSTGRES_PASSWORD,
    settings.POSTGRES_HOST,
    settings.POSTGRES_DB
)
