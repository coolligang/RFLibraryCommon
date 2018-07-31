# encoding=utf-8
import requests
import json
from jsonpath_rw import parse
from unittest.util import safe_repr
import time
import hashlib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

""" pip install poster """
import urllib2
import re


class RfeLibrary:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'

    longMessage = False

    def __init__(self):
        self._type_equality_funcs = {}
        self.s = requests.session()

    def _baseAssertEqual(self, first, second, msg=None):
        """The default assertEqual implementation, not type specific."""
        if not first == second:
            standardMsg = '%s != %s' % (safe_repr(first), safe_repr(second))
            msg = self._formatMessage(msg, standardMsg)
            raise AssertionError(msg)

    def _getAssertEqualityFunc(self, first, second):
        """Get a detailed comparison function for the types of the two args.

        Returns: A callable accepting (first, second, msg=None) that will
        raise a failure exception if first != second with a useful human
        readable error message for those types.
        """
        #
        # NOTE(gregory.p.smith): I considered isinstance(first, type(second))
        # and vice versa.  I opted for the conservative approach in case
        # subclasses are not intended to be compared in detail to their super
        # class instances using a type equality func.  This means testing
        # subtypes won't automagically use the detailed comparison.  Callers
        # should use their type specific assertSpamEqual method to compare
        # subclasses if the detailed comparison is desired and appropriate.
        # See the discussion in http://bugs.python.org/issue2578.
        #
        if type(first) is type(second):
            asserter = self._type_equality_funcs.get(type(first))
            if asserter is not None:
                if isinstance(asserter, basestring):
                    asserter = getattr(self, asserter)
                return asserter

        return self._baseAssertEqual

    def assertEqual(self, first, second, msg=None):
        """
        Fail if the two objects are unequal as determined by the '==' operator.
        """
        assertion_func = self._getAssertEqualityFunc(first, second)
        assertion_func(first, second, msg=msg)

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

    def reqByParams(self, method, url, params=None, headers=None, cookies=None):
        """
        通过Params的方式发起请求 \n
        :param method: \n
        :param url: \n
        :param params: dictionary \n
        :param headers: \n
        :param cookies: \n
        :return: \n
        """
        res = self.s.request(method.upper(), url, params=params, headers=headers, cookies=cookies)
        return res

    def reqByForm(self, method, url, form=None, headers=None, cookies=None):
        """
        通过form方式发起请求 \n
        :param method: \n
        :param url: \n
        :param form: dictionary \n
        :param headers: \n
        :param cookies: \n
        :return: \n
        """
        res = self.s.request(method.upper(), url, form=form, headers=headers, cookies=cookies)
        return res

    def reqByDataform(self, url, dataform=None, headers=None):
        """
        当post方式发起请求，且请求体为multipart/form-data时，用此方法
        :param url: str
        :param dataform: Dictionary
        :param headers: Dictionary
        :return:
        """
        register_openers()
        datagen, re_headers = multipart_encode(dataform)
        request = urllib2.Request(url, datagen, re_headers)
        if headers != None:
            for key, value in headers.iteritems():
                request.add_header(key, value)
        res = urllib2.urlopen(request).read()
        return res

    def getTimestamp(self):
        """
        返回毫秒级时间戳 \n
        :return:
        """
        return str(int(round(time.time() * 1000)))

    def getTimestampFormat(self, format="%Y%m%d%H%M%S000"):
        """
        返回需要的日期格式时间字符串 \n
        :param format:
        :return:
        %a 星期几的简写
        %A 星期几的全称
        %b 月分的简写
        %B 月份的全称
        %c 标准的日期的时间串
        %C 年份的后两位数字
        %d 十进制表示的每月的第几天
        %D 月/天/年
        %e 在两字符域中，十进制表示的每月的第几天
        %F 年-月-日
        %g 年份的后两位数字，使用基于周的年
        %G 年分，使用基于周的年
        %h 简写的月份名
        %H 24小时制的小时
        %I 12小时制的小时
        %j 十进制表示的每年的第几天
        %m 十进制表示的月份
        %M 十时制表示的分钟数
        %n 新行符
        %p 本地的AM或PM的等价显示
        %r 12小时的时间
        %R 显示小时和分钟：hh:mm
        %S 十进制的秒数
        %t 水平制表符
        %T 显示时分秒：hh:mm:ss
        %u 每周的第几天，星期一为第一天 （值从0到6，星期一为0）
        %U 第年的第几周，把星期日做为第一天（值从0到53）
        %V 每年的第几周，使用基于周的年
        %w 十进制表示的星期几（值从0到6，星期天为0）
        %W 每年的第几周，把星期一做为第一天（值从0到53）
        %x 标准的日期串
        %X 标准的时间串
        %y 不带世纪的十进制年份（值从0到99）
        %Y 带世纪部分的十制年份
        %z，%Z 时区名称，如果不能得到时区名称则返回空字符。
        %% 百分号
        """
        return str(time.strftime(format))

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

    def appendList(self, res_list, obj):
        """
        将对象obj添加到list中
        :param res_list: old list
        :param obj: object
        :return: new list
        """
        if isinstance(res_list, list):
            res_list.append(obj)
            return res_list

    def stringValueByPattern(self, pattern, string):
        """
        根据正则表达式获取字符串
        :return:
        """
        strValue = re.search(pattern, string).groups()
        return strValue[0]


if __name__ == "__main__":
    test = RfeLibrary()
    str0 = test.stringValueByPattern("你好(.*)!", "你好122324!")
    print str0

#     url = "http://10.10.253.5:8760/api/u/v1/user/app/code"
#     body_value = {"phone": "15300000000"}
#     headers = {"TRACE_ID": "#TV-)DiW", "TIMESTAMP": "20180709182733000", "EXTRA": "phone=15023363527","SIGN": "3c46a0428610d6122b02f70d7d897d97"}
#     bb = test.reqByDataform(url, body_value, headers)
#     print bb
