# -*- coding: utf-8 -*-

""" 所有的数据库连接都在这里定义 """

from atlas.conf import conf_common

from sqlalchemy                 import create_engine
from sqlalchemy.orm             import scoped_session
from sqlalchemy.orm             import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ----------------------------------------
# db_yapi_data

DB_ENGINE_API = create_engine(
    "mysql://%s:%s@%s:%d/%s?charset=%s" % (
        conf_common.CONF_DB_API["user"],
        conf_common.CONF_DB_API["pass"],
        conf_common.CONF_DB_API["host"],
        conf_common.CONF_DB_API["port"],
        conf_common.CONF_DB_API["dbname"],
        conf_common.CONF_DB_API["encode"]
    ),
    pool_recycle = conf_common.CONF_DB_API["recycle"]
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
        conf_common.CONF_DB_LOG["user"],
        conf_common.CONF_DB_LOG["pass"],
        conf_common.CONF_DB_LOG["host"],
        conf_common.CONF_DB_LOG["port"],
        conf_common.CONF_DB_LOG["dbname"],
        conf_common.CONF_DB_LOG["encode"]
    ),
    pool_recycle = conf_common.CONF_DB_LOG["recycle"]
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
