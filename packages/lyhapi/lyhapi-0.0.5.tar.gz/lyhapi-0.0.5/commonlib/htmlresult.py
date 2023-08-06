# coding=utf-8
"""
zx08443 生成HTML测试报告
"""

from HTMLTestRunner import HTMLTestRunner


def result():
    filename = 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：')
    return runner, fp  # 为什么要返回fp呢，因为调用这个方法的时候，还没有执行用例，所以返回fp，执行完用例，在关闭文件。
