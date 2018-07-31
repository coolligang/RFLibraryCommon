# encoding:utf-8
import datetime
import testlink


# pip install TestLink-API-Python-client


class TestlinkAPIClient:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'

    url = "http://10.10.253.3/testlink/lib/api/xmlrpc/v1/xmlrpc.php"

    def __init__(self):
        pass

    def reportTLRusult(self, devkey, testplanid, buildid, testcaseid, status, notes):
        """
        将执行结果上报至testlink \n
        :param testplanid: 计划ID \n
        :param buildid: 版本ID \n
        :param testcaseexternalid: 用例ID \n
        :param status: 执行结果 ：p 通过   f 失败   b 锁定  \n
        :param notes: 执行结果备注 \n
        :return:
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        server = testlink.TestlinkAPIClient(self.url, devkey)
        server.reportTCResult(testplanid=int(testplanid), buildid=int(buildid),
                              testcaseexternalid=testcaseid,
                              status=status,
                              notes=notes, timestamp=timestamp)

    def reportTL(self, devkey, testplanid, buildid, testcaseid, status, notes="auto", reportup=0):
        """
        将执行结果上报至testlink, 如果testcaseid是列表，则批量上报，否则只上报一个
        :param devkey: 用户key
        :param testplanid: 测试计划ID
        :param buildid: 计划版本ID
        :param testcaseid: str/list 用例ID
        :param status:  执行结果 ：p 通过   f 失败   b 锁定
        :param notes: 执行结果备注 \n
        :param reportup: 1: 将结果上传至testlink ,否则不上传
        :return:
        """
        if int(reportup) == 1:
            if isinstance(testcaseid, list):
                for caseid in testcaseid:
                    self.reportTLRusult(devkey, testplanid, buildid, caseid, status, notes)
            else:
                self.reportTLRusult(devkey, testplanid, buildid, testcaseid, status, notes)
        else:
            print "*INFO* Not report to testlink!(reportup != 1)"


if __name__ == "__main__":
    key = "2b478cdd85194ee74a0702ad4fbced95"
    test = TestlinkAPIClient()
    test.reportTL(key, 1202, 6, ["mt-189", "mt-190", "mt-191"], "p", "auto", 1)
    print "OK"
