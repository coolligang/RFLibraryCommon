# encoding=utf-8
import requests
import json
import base64
from jsonpath_rw import parse
from unittest.util import safe_repr
import hashlib
import time
from RfeLibTool import RfeLibTool


class RfeLibrary:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'

    longMessage = False

    def __init__(self):
        self.s = requests.session()

    def _formatMessage(self, msg, standardMsg):
        """Honour the longMessage attribute when generating failure messages.
        If longMessage is False this means:
        * Use only an explicit message if it is provided
        * Otherwise use the standard message for the assert

        If longMessage is True:
        * Use the standard message
        * If an explicit message is provided, plus ' : ' and the explicit message
        """
        if not self.longMessage:
            return msg or standardMsg
        if msg is None:
            return standardMsg
        try:
            # don't switch to '{}' formatting in Python 2.X
            # it changes the way unicode input is handled
            return '%s : %s' % (standardMsg, msg)
        except UnicodeDecodeError:
            return '%s : %s' % (safe_repr(standardMsg), safe_repr(msg))

    def assertJson(self, expected, actual, assertType=1, msg=None):
        """
        Checks whether actual is a superset of expected. \n
        :param expected:  \n
        :param actual:  \n
        :param assertType: 0 模糊匹配  1 精确匹配  \n
        :param msg:  \n
        :return:  \n
        """
        expected = json.loads(expected)
        actual = json.loads(actual)
        assertType = int(assertType)
        missing = []
        mismatched = []
        for key, value in expected.iteritems():
            if key not in actual:
                missing.append(key)
            elif value != actual[key]:
                if assertType == 0 and type(value) == type(actual[key]):
                    continue
                mismatched.append(
                    '%s(expected: %s, actual: %s)' % (safe_repr(key), safe_repr(value), safe_repr(actual[key])))
        if not (missing or mismatched):
            return
        standardMsg = ''
        if missing:
            standardMsg = 'Missing: %s' % ','.join(safe_repr(m) for m in missing)
        if mismatched:
            if standardMsg:
                standardMsg += '; '
            standardMsg += 'Mismatched values: %s' % ','.join(mismatched)
        raise AssertionError(self._formatMessage(msg, standardMsg))

    def getValueFromJson(self, str_json, jsonpath):
        """
        获取json中某个key对应的value \n
        :param str_json: str json \n
        :param jsonpath: str jsonpath \n
        :return: obj 通过jsonpath在json中得到的value 可能是 int str obj ... \n
        """
        jsonxpr = parse(jsonpath)
        return jsonxpr.find(json.loads(str_json))[0].value

    def reqByJson(self, method, url, json=None, headers=None, cookies=None):
        """
        通过 Json 的方式发起请求\n
        :param method: post\get\...\n
        :param url: str\n
        :param json: dictionary\n
        :param headers: dictionary\n
        :param cookies: response_obj
        :return: response_obj
        """
        res = self.s.request(method.upper(), url, json=json, headers=headers, cookies=cookies)
        return res

    def getFile(self, path):
        with open(path, 'r') as fin:
            data = fin.read()
            return data

    def toBase64(self, img_path):
        """
        将图片转为base64编码  \n
        :param img_path: 图片路径  \n
        :return:  \n
        """
        with open(img_path, 'rb') as fin:  # 二进制方式打开图片
            image_data = fin.read()
            base64_data = base64.b64encode(image_data)
            return base64_data

    def decodingFromBase64(self, coding, file_name="", path=""):
        """
        将Base64编码解码为jpg图片
        :param coding:
        :param file_name: 默认为当前时间
        :param path: 默认为当前根目录
        :return:
        """
        if file_name == "":
            rfeTool = RfeLibTool()
            file_name = rfeTool.getDate("%Y%m%d%H%M%S")
        try:
            with open(path + file_name + ".jpg", "wb") as fout:
                fout.write(coding)
        except Exception, e:
            raise safe_repr(e)

    def toMD5(self, str_content):
        """
        将传入字符串进行md5加密  \n
        :param str_content: 要加密的字符串  \n
        :return: \n
        """
        m = hashlib.md5()
        m.update(str_content)
        str_encoding = m.hexdigest()
        return str_encoding

    def getTimestamp(self):
        """
        返回毫秒级时间戳 \n
        :return:
        """
        return int(round(time.time() * 1000))


if __name__ == "__main__":
    rfeLib = RfeLibrary()
    apiId = "BOxALFZsYGw0GNzebQck1xKs"
    apiKey = "1285384ddfb057814bad78127bc789be"
    url = "/api/v1/face/facerecognize"
    timestamp = rfeLib.getTimestamp()
    pre_sign = "api/v1/facerecognize" + apiKey + str(timestamp)
    sign = rfeLib.toMD5(pre_sign)
    feature = "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"
    fId = "A123143B"
    user1 = {"fId": fId, "feature": feature}
    faceInfos = [user1]
    body = {"apiId": apiId, "timestamp": timestamp, "cameraId": "A0000001", "sign": sign, "cameraIp": "10.23.25.44",
            "faceInfos": faceInfos}
    rs = rfeLib.reqByJson("post", "http://172.16.31.36:9090" + url, body)
    print rs.content
