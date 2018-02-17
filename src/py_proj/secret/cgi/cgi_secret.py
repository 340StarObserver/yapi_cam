# -*- coding: utf-8 -*-

import sys
from datetime import datetime

from secret.conf   import conf_code
from secret.common import global_db
from secret.common import global_tool
from secret.model  import model_user
from secret.model  import model_secret

def cgi_createSecret(para):
    return {
        "returnCode"    : conf_code.CONF_CODE["success"][0],
        "returnMessage" : conf_code.CONF_CODE["success"][1],
        "data"          : {
            "test"      : "just test"
        }
    }
