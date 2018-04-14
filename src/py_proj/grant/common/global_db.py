# -*- coding: utf-8 -*-

from grant.conf.conf_base import CONF_DB_AUTH

from sqlalchemy                 import create_engine
from sqlalchemy.orm             import scoped_session
from sqlalchemy.orm             import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_ENGINE_AUTH = create_engine(
    "mysql://%s:%s@%s:%d/%s?charset=%s" % (
        CONF_DB_AUTH["user"],
        CONF_DB_AUTH["pass"],
        CONF_DB_AUTH["host"],
        CONF_DB_AUTH["port"],
        CONF_DB_AUTH["dbname"],
        CONF_DB_AUTH["encode"]
    ),
    pool_recycle  = CONF_DB_AUTH["recycle"],
    pool_size     = CONF_DB_AUTH["size"],
    pool_pre_ping = True
)

DB_SESSION_AUTH = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush  = False,
        bind       = DB_ENGINE_AUTH
    )
)

DB_BASE_AUTH = declarative_base()
DB_BASE_AUTH.query = DB_SESSION_AUTH.query_property()
DB_BASE_AUTH.metadata.create_all(bind = DB_ENGINE_AUTH)
