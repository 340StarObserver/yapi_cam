# -*- coding: utf-8 -*-

import json
import hmac
import base64
import hashlib

def calcSignature(content, keyList, secretKey):
    content["params"] = json.dumps(content["params"], sort_keys = True)

    paraDict = {}
    for k in keyList:
        paraDict[k] = content[k]

    paraList = sorted(paraDict.iteritems(), key = lambda kv : kv[0], reverse = False)
    n = len(paraList)
    i = 0
    while i < n:
        paraList[i] = "%s=%s" % (paraList[i][0], paraList[i][1])
        i += 1

    srcStr = "&".join(paraList)
    sig = hmac.new(str(secretKey), str(srcStr), digestmod = hashlib.sha256).hexdigest()
    sig = base64.b64encode(sig)
    
    return sig
