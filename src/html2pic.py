# coding:utf-8
"""html 转图片主程序"""
import config
from mathexpress import findmath
from selenium import webdriver
from PIL import Image
import os
import time
import codecs
import sys


def _generate_valid_html(math_express, css_path=None):
    """将匹配成功的代码添加标签"""
    if css_path is None:
        css_path = u'style.css'
    return u"""<html> <head><link rel="stylesheet" type="text/css"
    href="{css_path}"></head><body><div id="replace_div"><span
    id='replace_span'>{math_express}</span></div>
    </body></html>""".format(math_express=math_express, css_path=css_path)


def _save_valid_html(html):
    valid_html = _generate_valid_html(html)
    filename = str(long(time.time() * 10000)) + '.html'
    file_path = os.path.join(config.html_save_tmp_path, filename)
    with codecs.open(filename=file_path, mode='wb', encoding='utf-8') as f:
        f.write(valid_html)
    return file_path


def _delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception:
        pass


def _crop(div, span, screenshot_path):
    """截图 这儿通过传入一个span获得需要截取部分的长度,传入一个div获得
    对象的高度来保证在截图时不会截取过长同时又不会纵向截取缺失"""
    img = Image.open(screenshot_path)
    left = int(div.location ['x'])
    top = int(div.location ['y'])
    right = left + span.size ['width']
    bottom = top + div.size ['height']
    window = (left, top, right, bottom)
    region = img.crop(window)
    png_name = str(long(time.time() * 10000)) + '.png'
    png_path = os.path.join(config.png_path, png_name)
    region.save(png_path)
    return png_path


def _draw(driver, html):
    """传入的html代码进行截图"""
    html_path = _save_valid_html(html)
    url = "file://" + html_path
    driver.get(url)
    div = driver.find_element_by_xpath('//*[@id="replace_div"]')
    span = driver.find_element_by_xpath('//*[@id="replace_span"]')
    screenshot_name = str(long(time.time() * 10000)) + '.png'
    screenshot_path = os.path.join(config.screenshot_path, screenshot_name)
    driver.save_screenshot(screenshot_path)
    png_path = _crop(div=div, span=span, screenshot_path=screenshot_path)
    # 删除生成的临时文件
    _delete_file(html_path)
    _delete_file(screenshot_path)
    return png_path


def _replace_start(data_str, src_str, des_str=u''):
    if data_str.startswith(src_str):
        return des_str + data_str[len(src_str):]
    return data_str


def html2pic(rules_path, html_path=None, html_content=None, driver=None):
    """
        rules_path: 规则文件路径
        html_path: 需要转图片的html文件路径
        html_content:需要转图片的html文本内容，在没有提供html_path的时候启用
        return: 返回一组相关源码和源码存储的图片地址
    """
    if driver is None:
        driver = webdriver.Chrome()
    match_htmls = findmath(rules_path, html_path, html_content)
    print("match length:{length}".format(length=len(match_htmls)))
    html2pics = dict()
    for html in match_htmls:
        print html[0:100]
        # html = _replace_start(html, u'/>')
        # html = _replace_start(html, u'A.')
        # html = _replace_start(html, u'B.')
        # html = _replace_start(html, u'C.')
        # html = _replace_start(html, u'D.')
        # html = _replace_start(html, u'nbsp;')
        html2pics.update({html: _draw(driver, html)})
    return html2pics


def test_from_db():
    import MySQLdb
    db = MySQLdb.connect(host='172.18.4.81', user='admintest', passwd='dsjw2015',
                         db='homework', port=3307, charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        """select option_a,option_b,option_c,option_d,title,parse,answer1,
        answer2 from questions where subjectId=9 limit 0, 10""")
    data_list = cursor.fetchall()
    driver = webdriver.Chrome()
    results = list()
    for data in data_list:
        for item in data:
            if item is None or len(item) == 0:
                pass
            else:
                print(item)
                result = html2pic("/Users/lovechenao/gitroom/html2pic/"
                                  "src/okay/rules/chemistry.rule",
                                  html_content=item,driver=driver)
                results.append(result)
    driver.close()




if __name__ == '__main__':
    # args = sys.argv
    # if len(args) != 3:
    #     print("""
    #    example: python html2pic rules_path html_path
    #    """)
    # driver = webdriver.Chrome()
    # try:
    #     print html2pic(rules_path=args[1], html_path=args[2], driver=driver)
    # except Exception as e:
    #     print e
    # driver.close()
    test_from_db()
