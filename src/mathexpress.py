# coding:utf-8
"""
    通过加载rules配置文件中的规则获取目标源码中的符合规则的的html源码代码段
"""
import re
import sys
import codecs
import config


def _findmath(rules, html):
    if rules is None or len(rules) == 0:
        return set()
    print("rules length:{length}".format(length = len(rules)))
    rule = rules[0]
    partern = re.compile(rule)
    groups = partern.findall(html)
    math_set = set()
    for group in groups:
        # 将已经提取的数据用占位符替换
        html = html.replace(group, config.placeholder)
        math_set.add(group)
    return math_set.union(_findmath(rules[1:], html))


def _parse_rules(rules_path):
    rules = list()
    with codecs.open(rules_path, mode='rb', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n\r\t')
            if not line.startswith(config.annotate) and len(line) >= 1\
            and line != u'':
                rules.append(line)
    print('=='*10+'rule'+'=='*10)
    print(rules)
    print('=='*10+'rule'+'=='*10)
    return rules


def _get_html(html_path):
    with codecs.open(html_path, mode='rb', encoding='utf-8') as f:
        html = f.read()
    print('=='*10+'html'+'=='*10)
    print(html[0:100])
    print('=='*10+'html'+'=='*10)
    return html


def findmath(rules_path, html_path=None, html_content=None):
    rules = _parse_rules(rules_path)
    if html_content is None:
        html = _get_html(html_path)
    else:
        html = html_content
    if html is None:
        raise Exception('html 不能为空')
    elif not isinstance(html, unicode):
        raise Exception('需要提供unicode编码的html')
    return _findmath(rules, html)

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print("""
        HELP Example:
            python mathexpress.py rules_path html_path
        """)
        sys.exit(0)
    print(findmath(args[1], args[2]))
