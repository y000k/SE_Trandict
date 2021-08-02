# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.7.28 00:51
# @Author : Synthesis 杜品赫
# @File : Debug.py
# @Software : PyCharm
# https://github.com/SynthesisDu/SE_Trandict

import urllib.request
import urllib.error
import sqlite3
import re
from bs4 import BeautifulSoup

def DescTable(connect, table):
    c = connect.cursor()
    c.execute('select * from sqlite_master where type="table" and name="%s";' % table)
    for p in c.fetchall():
        for pp in p:
            print(pp)

def ShowTable(connect, rea = False):
    """
    re = True  直接print所有表
    re = False 返回带序号的表名字典
    """
    if not rea:
        try:
            cur = connect.cursor()
            cur.execute("select name from sqlite_master where type='table' order by name")
            print(cur.fetchall())
        except Exception as e:
            print(e)
    else:
        try:
            cur = connect.cursor()
            cur.execute("select name from sqlite_master where type='table' order by name")
            ret = {}
            i = 0
            for e in cur.fetchall():
                ret[i] = str(e).replace("('", '').replace("',)", '')
                i += 1
            return ret
        except Exception as e:
            print(e)

def DropTable(connect, table = '', tables = []):
    """
    @ ShowTable()
    """
    if not table == '' or not tables == []:
        if not tables:
            tables = [table]
        try:
            cur = connect.cursor()
            for table in tables:
                cur.execute("drop table %s" % table)
            print("===Delete tables %s successful!" % str(tables))
        except Exception as e:
            print("===Delete tables %s error: " % str(tables) + e)
    else:
        print('===Choose the tables you want to drop, "exit" to exit:')
        while True:
            tabs = ShowTable(connect, re = True)
            for key in tabs:
                print(str(key) + ':' + str(tabs[key]))
            try:
                inp = input('>>>')
                if inp == 'exit':
                    break
                else:
                    cur = connect.cursor()
                    cur.execute("drop table %s" % tabs[int(inp)])
                    print("===Delete table %s successful!" % tabs[int(inp)])
            except Exception as e:
                print('===Input should be the int number, try again:')

def SelectTableField(connect, table, field):
    cur = connect.cursor()
    cur.execute('select %s from %s;' % (field, table))
    ret = []
    for e in cur.fetchall():
        ret.append(str(e).replace("('", '').replace("',)", ''))
    return ret

def YouDao(connect, wordlist):
    cur = connect.cursor()
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    # wordlist = ['run']
    for word in wordlist:
        if word != '(None,)':
            request = urllib.request.Request("https://www.youdao.com/w/" + word, headers = head)
            try:
                response = urllib.request.urlopen(request)
                htmlChar = response.read().decode("utf-8")
                bs = BeautifulSoup(htmlChar, 'html.parser')
                transContainer = bs.find_all(class_ = "trans-container")
                additional = str(str(bs.find_all(class_="additional")))
            except urllib.error.URLError as e:
                if hasattr(e, 'reason'):
                    print("===Url error: " + e.reason)
                else:
                    print("===Url error: " + e)
            except Exception as e:
                print("===Error: " + e)
            try:
                """
                | 3    | 名词       | noun              | n    |
                | 4    | 代词       | pronoun           | pron |
                | 5    | 形容词     | adjective         | adj  |
                | 6    | 副词       | adverb            | adv  |
                | 7    | 动词       | verb              | v    |
                | 8    | 不及物动词 | intransitive verb | vi   |
                | 9    | 及物动词   | transitive verb   | vt   |
                | 10   | 助动词     | auxiliary verb    | aux  |
                | 11   | 数词       | numeral           | num  |
                | 12   | 冠词       | article           | art  |
                | 13   | 介词       | preposition       | prep |
                | 14   | 连词       | conjunction       | conj |
                | 15   | 感叹词     | interjection      | int  |
                | 16   | 缩写       | abbreviation      | abbr |
                """
                if transContainer is None:
                    print('========================================================================', word)
                    continue
                getIn = ''
                try:
                    getIn = str(transContainer[0])
                except Exception as e:
                    print(e)
                TransMain(cur, getIn, word)
            except Exception as e:
                print("===Error: " + e)
            try:
                if '<p class="additional">[' in additional:
                    additional = additional[additional.find('<p class="additional">[')+23:]
                    additional = additional[:additional.find(']')]
                    additional = additional.replace(' ', '').replace('\n', ', ')
                    additional = additional.replace('数, ', '数<').replace('词, ', '词<').replace('式, ', '式<').replace('时, ', '时<')
                    additional = additional.replace(', ', '>, ')[3:-2].replace('或', '><').replace('"', "'")
                    cur.execute('UPDATE vocab SET wyy_additional = "%s" WHERE vocab = "%s";' % (additional, word))
                    print('UPDATE vocab SET wyy_additional = "%s" WHERE vocab = "%s";' % (additional, word))
                    con.commit()
                    # print(additional)
            except Exception as e:
                print(e)

def TransMain(cur, getIn, word):
    TransContainer(cur, getIn, word, '<li>n.', 7, 'noun')
    TransContainer(cur, getIn, word, '<li>porn.', 10, 'pronoun')
    TransContainer(cur, getIn, word, '<li>adj.', 9, 'adjective')
    TransContainer(cur, getIn, word, '<li>adv.', 9, 'adverb')
    TransContainer(cur, getIn, word, '<li>v.', 7, 'verb')
    TransContainer(cur, getIn, word, '<li>vi.', 8, 'intransitive_verb')
    TransContainer(cur, getIn, word, '<li>vt.', 8, 'transitive_verb')
    TransContainer(cur, getIn, word, '<li>aux.', 9, 'auxiliary_verb')
    TransContainer(cur, getIn, word, '<li>num.', 9, 'numeral')
    TransContainer(cur, getIn, word, '<li>art.', 9, 'article')
    TransContainer(cur, getIn, word, '<li>prep.', 10, 'preposition')
    TransContainer(cur, getIn, word, '<li>conj.', 10, 'conjunction')
    TransContainer(cur, getIn, word, '<li>int.', 9, 'interjection')
    TransContainer(cur, getIn, word, '<li>abbr.', 10, 'abbreviation')

def TransContainer(cur, getIn, word, key, iKey, lKey, add = ''):
    """
    # 直接覆盖原有释义
    """
    try:
        if key in getIn:
            get = getIn[getIn.find(key) + iKey:]
            reGet = get[get.find('</li>'):]
            get = get[:get.find('</li>')].replace('&lt;', '<').replace('&gt;', '>')
            get = get.replace('，', '; ').replace('；', '; ').replace('……', '...').replace(') ', ')')
            get = get.replace('（', ' (').replace('）', ') ').replace(';;', ';').replace('…', '...').replace(') ', ')')
            get = get.replace(';  (', '; (').replace(') ;', ');').replace(')  ;', ');').replace(') ', ')').replace(')', ') ')
            get = get.replace(';(', '; (')
            if add != '':
                get = add + ';' + get
            if key in reGet:
                TransContainer(cur, reGet, word, key, iKey, lKey, add = get)
            else:
                cur.execute('UPDATE vocab SET %s = "%s" WHERE vocab = "%s";' % (lKey, get, word))
                print('UPDATE vocab SET %s = "%s" WHERE vocab = "%s";' % (lKey, get, word))
                con.commit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    con = sqlite3.connect('Database.db')
    YouDao(con, SelectTableField(con, "vocab", "vocab")[189500:])
    # cur = con.cursor()
    # cur.execute('SELECT * FROM vocab;')
    # print(cur.fetchall())
    con.close()


"""
Table vocab
0. (自增约束主键)
1. (词本体)
2. 名词
3. 代词
4. 形容词
5. 副词
6. 动词
7. 不及物动词
8. 及物动词
9. 助动词
10. 数词
11. 冠词
12. 介词
13. 连词
14. 感叹词
15. (是否星标)
16. (最后搜索时间)
# lines = []
# with open("words.txt", "r") as f:
#     for line in f.readlines():
#         line = line.strip('\n')  # 去掉列表中每一个元素的换行符
#         lines.append(line)
# c = con.cursor()
# id = 0
# for line in lines:
#     try:
#         if line.isalnum() and line.isalpha():
#             line = line.lower()
#             print(line)
#             c.execute("insert into vocab values (%d, '%s', '', '', '', '', '', '', '', '', '', '', '', '', '', 0, '');" % (id, line))
#             id += 1
#     except Exception as e:
#         print(e)
#         print(line)
# con.commit()
"""
