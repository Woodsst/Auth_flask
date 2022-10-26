import redis
from config.settings import default_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

redis_conn = redis.Redis(
    host=default_settings.redis_host,
    port=default_settings.redis_port,
    db=0,
)

engine = create_engine(default_settings.postgres, convert_unicode=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()
