# encoding=utf-8
import base64
from jsonpath_rw import parse
import hashlib
import time
import uuid
import random
import os
from unittest.util import safe_repr
import shutil


class RfeLibTool:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'

    def __init__(self):
        pass

    def getValueFromJson(self, str_json, jsonpath):
        """
        获取json中某个key对应的value \n
        :param str_json: str json \n
        :param jsonpath: str jsonpath \n
        :return: obj 通过jsonpath在json中得到的value 可能是 int str obj ...\n
        """
        jsonxpr = parse(jsonpath)
        return jsonxpr.find(json.loads(str_json))[0].value

    def getFile(self, path):
        """
        读出文本中的内容 \n
        :param path: 文件路径 \n
        :return:  文件内容 \n
        """
        try:
            with open(path, 'r') as fin:
                data = fin.read()
                return data
        except Exception, e:
            raise safe_repr(e)

    def toBase64(self, img_path):
        """
        将图片转为base64编码  \n
        :param img_path: 图片路径  \n
        :return:  \n
        """
        try:
            with open(img_path, 'rb') as fin:  # 二进制方式打开图片
                image_data = fin.read()
                base64_data = base64.b64encode(image_data)
                return base64_data
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
        :return: 时间戳 \n
        """
        return int(round(time.time() * 1000))

    def getRandInt(self, min, max):
        """
        返回一个[min,max]区间的整数
        :return:
        """
        return random.randint(int(min), int(max))

    def getRandNum(self, min, max, ndigits=2):
        """
        返回 [min,max] 区间的浮点数
        :param min:
        :param max:
        :return:
        random.random() 产生[0,1]之间的小数
        """

        return round(random.random() * (float(max) - float(min)) + float(min), ndigits)

    def getRandStr(self, n=7, type=0):
        """
        生成一个指定长度为 n 的随便字符串，  \n
        :param n: 要返回的字符串长度
        :param type: type=0时（n<=10），为纯数字，type1=0时(n<=36)，为字母数字混合 \n
        :return: str
        """
        str0 = "012345678901234567890123456789"
        str1 = "abcdefghijklmnopqrstuvwxyz"
        if int(type) == 0:
            list_rs = random.sample(str0, int(n))
        else:
            list_rs = random.sample(str0 + str1, int(n))
        return "".join(list_rs)

    def listUUID(self, n=1):
        """
        批量返回全球唯一的32位字符串 \n
        :param n: 要返回字符串的个数,默认为1
        :return: list[str1,str2]
        """
        try:
            list = [self.toMD5(str(uuid.uuid1()).replace("-", "")) for i in range(int(n))]
        except Exception, e:
            raise safe_repr(e)
        return list

    def listRandFileName(self, path, n=1):
        """
        随机返回n个path路径下的文件名 \n
        :param path: 存放文件的路径 \n
        :param n: 要返回的文件名数量 \n
        :return: list[str1,str2,...]
        """
        list_file = os.listdir(path)
        return random.sample(list_file, int(n))

    def listAllFileName(self, path):
        """
        返回path路径下所有文件名称  \n
        :param path: 存放文件的路径 \n
        :return: list[str1,str2,...]
        """
        return os.listdir(path)

    def moveFile(self, resPath, tagPath):
        try:
            shutil.move(resPath, tagPath)
        except Exception, e:
            raise safe_repr(e)

    def copyFile(self, resPath, tagPath):
        try:
            shutil.copy(resPath, tagPath)
        except Exception, e:
            raise safe_repr(e)

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

    def getDate(self, format="%Y%m%d"):
        """
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
        return time.strftime(format)


if __name__ == "__main__":
    test = RfeLibTool()
    a = test.getRandNum(0.6, 1)
    print a
