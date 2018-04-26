# -*- coding: utf-8 -*-

import time
import json
import hmac
import random
import base64
import hashlib
import urllib2

class OpenApi(object):
    def __init__(self, secretId, secretKey, module, action, region, params):
        self._url  = "http://cloud.yapi/cloud/interface"

        self._data = {
            "module"    : module,
            "action"    : action,
            "reqTime"   : int(time.time()),
            "reqNonce"  : random.randint(10000000, 99999999),
            "reqRegion" : region,
            "secretId"  : secretId,
            "params"    : params
        }

        self._data["signature"] = self._signature(self._data, secretKey)
        self._data["params"] = json.loads(self._data["params"])

    def _signature(self, content, secretKey):
        content["params"] = json.dumps(content["params"], sort_keys = True)

        paraList = sorted(content.iteritems(), key = lambda kv : kv[0], reverse = False)
        n = len(paraList)
        i = 0
        while i < n:
            paraList[i] = "%s=%s" % (paraList[i][0], paraList[i][1])
            i += 1

        srcStr = "&".join(paraList)
        sig = hmac.new(str(secretKey), str(srcStr), digestmod = hashlib.sha256).hexdigest()
        return base64.b64encode(sig)

    def reqUrl(self):
        return self._url

    def reqData(self):
        return self._data

    def request(self):
        dataStr = json.dumps(self._data).encode("utf-8")

        req = urllib2.Request(self._url, dataStr)
        req.add_header("Content-Type"  , "application/json; charset=utf-8")
        req.add_header("Content-Length", len(dataStr))

        return json.loads(urllib2.urlopen(req).read())


if __name__ == "__main__":
    api = OpenApi(
        secretId  = "AKIDZCj57L6Gk5VCXHu89J8Kl25KWGi2WAj1",
        secretKey = "ZCj57AXAk5VCXHu89J8Kl25KWGi2WAj1",
        module    = "grant",
        action    = "GetStrategyList",
        region    = "sz",
        params    = {
            "pageId"   : 1,
            "pageSize" : 10
        }
    )

    print "req url  : " + api.reqUrl()
    print "req data : " + json.dumps(api.reqData(), indent = 4)
    print "rsp data : " + json.dumps(api.request(), indent = 4)
