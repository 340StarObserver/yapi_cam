# -*- coding: utf-8 -*-

""" 所有的数据库连接都在这里定义 """

from account.conf import conf_common

from sqlalchemy                 import create_engine
from sqlalchemy.orm             import scoped_session
from sqlalchemy.orm             import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_ENGINE_AUTH  = create_engine(
    "mysql://%s:%s@%s:%d/%s?charset=%s" % (
        conf_common.CONF_DB_AUTH["user"],
        conf_common.CONF_DB_AUTH["pass"],
        conf_common.CONF_DB_AUTH["host"],
        conf_common.CONF_DB_AUTH["port"],
        conf_common.CONF_DB_AUTH["dbname"],
        conf_common.CONF_DB_AUTH["encode"]
    ),
    pool_recycle = conf_common.CONF_DB_AUTH["recycle"]
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
