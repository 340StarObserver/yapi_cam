# -*- coding: utf-8 -*-

from cloud.conf.config import CONF_DB_API
from cloud.conf.config import CONF_DB_LOG

from sqlalchemy                 import create_engine
from sqlalchemy.orm             import scoped_session
from sqlalchemy.orm             import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ----------------------------------------
# db_yapi_data

DB_ENGINE_API = create_engine(
    "mysql://%s:%s@%s:%d/%s?charset=%s" % (
        CONF_DB_API["user"],
        CONF_DB_API["pass"],
        CONF_DB_API["host"],
        CONF_DB_API["port"],
        CONF_DB_API["dbname"],
        CONF_DB_API["encode"]
    ),
    pool_recycle  = CONF_DB_API["recycle"],
    pool_size     = CONF_DB_API["size"],
    pool_pre_ping = True
)

DB_SESSION_API = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush  = False,
        bind       = DB_ENGINE_API
    )
)

DB_BASE_API = declarative_base()
DB_BASE_API.query = DB_SESSION_API.query_property()
DB_BASE_API.metadata.create_all(bind = DB_ENGINE_API)

# ----------------------------------------
# db_yapi_log

DB_ENGINE_LOG = create_engine(
    "mysql://%s:%s@%s:%d/%s?charset=%s" % (
        CONF_DB_LOG["user"],
        CONF_DB_LOG["pass"],
        CONF_DB_LOG["host"],
        CONF_DB_LOG["port"],
        CONF_DB_LOG["dbname"],
        CONF_DB_LOG["encode"]
    ),
    pool_recycle  = CONF_DB_LOG["recycle"],
    pool_size     = CONF_DB_LOG["size"],
    pool_pre_ping = True
)

DB_SESSION_LOG = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush  = False,
        bind       = DB_ENGINE_LOG
    )
)

DB_BASE_LOG = declarative_base()
DB_BASE_LOG.query = DB_SESSION_LOG.query_property()
DB_BASE_LOG.metadata.create_all(bind = DB_ENGINE_LOG)
