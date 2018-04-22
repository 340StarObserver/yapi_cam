# -*- coding: utf-8 -*-

import time
import json
import hmac
import random
import base64
import urllib2
import hashlib

def callService(url, data):
    data = json.dumps(data).encode("utf-8")
    req  = urllib2.Request(url, data)
    req.add_header("Content-Type"  , "application/json; charset=utf-8")
    req.add_header("Content-Length", len(data))
    res  = urllib2.urlopen(req)
    return json.loads(res.read())

def signature(data, secretKey):
    content = dict(data["interface"]["para"]["content"])
    content["params"] = json.dumps(content["params"], sort_keys = True)
    
    paraDict = {}
    for k in content.keys():
        if k in data["interface"]["para"]["header"]["keyList"]:
            paraDict[k] = content[k]

    paraList = sorted(paraDict.iteritems(), key = lambda kv : kv[0], reverse = False)
    n = len(paraList)
    i = 0
    while i < n:
        paraList[i] = "%s=%s" % (paraList[i][0], paraList[i][1])
        i += 1

    srcStr = "&".join(paraList)
    sig = hmac.new(secretKey, srcStr, digestmod = hashlib.sha256).hexdigest()
    sig = base64.b64encode(sig)
    data["interface"]["para"]["content"]["signature"] = sig


secretId  = "AKIDZCj57L6Gk5VCXHu89J8Kl25KWGi2WAj1"
secretKey = "ZCj57AXAk5VCXHu89J8Kl25KWGi2WAj1"

url  = "http://swoole.yapi/swoole/interface"
data = {
    "version"       : "1.0",
    "componentName" : "yapi.swoole",
    "eventId"       : int(time.time()),
    "timestamp"     : int(time.time()),
    "interface"     : {
        "interfaceName" : "yapi.swoole.auth",
        "para"          : {
            "header"    : {
                "mode"      : 0,
                "resource"  : [
                    "yapi:region/gz:grant:ownerUin/909619800",
                ],
                "condition" : [
                    {
                        "condKey"   : "pageSize",
                        "condValue" : 50
                    }
                ],
                "keyList"   : [
                    "module", "action", "reqTime", "reqNonce", "reqRegion", "secretId", "params"
                ]
            },
            "content"   : {
                "module"    : "grant",
                "action"    : "GetStrategyList",
                "reqTime"   : int(time.time()),
                "reqNonce"  : random.randint(100000, 999999),
                "reqRegion" : "gz",
                "secretId"  : secretId,
                "signature" : "",
                "params"    : {
                    "loginUin" : 909623456,
                    "ownerUin" : 909619400,
                    "pageId"   : 1,
                    "pageSize" : 50
                }
            }
        }
    }
}

signature(data, secretKey)

print "request :"
print json.dumps(data, indent = 2)

print "respond :"
print json.dumps(callService(url, data), indent = 2)
