# condig:utf-8
"""
    html 转图片主程序
"""
import config
from mathexpress import findmath
from selenium import webdriver

def html2pic(rules_path, html_path=None, html_content=None, driver=None):
    """
        return: 返回一组相关源码和源码存储的图片地址
    """
    if driver is None:
        driver = webdriver.Chrome()


    #return {math:pic_path}


