# coding:utf-8
import os


# 文件当前路径
current_dir_path = "/Users/lovechenao/gitroom/html2pic/src/okay"
# current_dir_path = os.getcwd()


# 规则注释标记
annotate = '#'


# 占位符
placeholder = u'回家吃饭了'


# html 暂存路径
html_save_tmp_path = os.path.join(current_dir_path, 'html_tmp')


# png 存储路径
png_path = os.path.join(current_dir_path, 'pngs')


# screenshot 临时存储路径
screenshot_path = os.path.join(current_dir_path, 'screenshot')
