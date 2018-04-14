# -*- coding: utf-8 -*-

import sys
import json
import urllib2

reload(sys)
sys.setdefaultencoding("utf-8")

def callService(url, data):
    data = json.dumps(data).encode("utf-8")
    req  = urllib2.Request(url, data)
    req.add_header("Content-Type"  , "application/json; charset=utf-8")
    req.add_header("Content-Length", len(data))
    res  = urllib2.urlopen(req)
    return json.loads(res.read())

def readFile(fileName):
    f = open(fileName, "r")
    d = f.read()
    f.close()
    return d

reqUrl  = "http://atlas.yapi/atlas/interface"

reqData = {
    "version"       : "1.0",
    "componentName" : "yapi.atlas",
    "eventId"       : 1445599887,
    "timestamp"     : 1445599887,
    "interface"     : {
        "interfaceName" : "yapi.atlas.createAction",
        "para"          : {
            "loginUin"  : 909619752,
            "ownerUin"  : 909619400,
            "module"    : "vpc",
            "action"    : "AddRoute",
            "actionName": u"新建路由表",
            "urlName"   : "vpc.k8s.mc.py",
            "isAuth"    : 1,
            "isRate"    : 1,
            "minRate"   : 100,
            "funcReq"       : readFile("funcReq.txt"),
            "funcRsp"       : readFile("funcRsp.txt"),
            "funcResource"  : readFile("funcResource.txt"),
            "funcCondition" : readFile("funcCondition.txt")
        }
    }
}

print "request : "
print json.dumps(reqData, indent = 2)

print "response : "
print json.dumps(callService(reqUrl, reqData), indent = 2)
