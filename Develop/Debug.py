# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.7.28 00:51
# @Author : Synthesis 杜品赫
# @File : Debug.py
# @Software : PyCharm
# https://github.com/SynthesisDu/SE_Trandict

import urllib.request
import urllib.error
from bs4 import BeautifulSoup

import sqlite3

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

def DropTable(connect, table='', tables=[]):
    """
    @ ShowTable()
    """
    if not table == '' or not tables == []:
        if tables == []:
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
            tabs = ShowTable(connect, re=True)
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

def YouDao(wordlist):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    for word in wordlist:
        request = urllib.request.Request("https://www.youdao.com/w/" + word, headers = head)
        try:
            response = urllib.request.urlopen(request)
            htmlChar = response.read().decode("utf-8")
            bs = BeautifulSoup(htmlChar, 'html.parser')
            print(word)
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print("===Url error: " + e.reason)
            else:
                print("===Url error: " + e)
        except Exception as e:
            print("===Error: " + e)



if __name__ == '__main__':
    con = sqlite3.connect('Database.db')

    YouDao(SelectTableField(con, "vocab", "vocab"))

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
