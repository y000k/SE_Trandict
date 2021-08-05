# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.7.28 00:51
# @Author : Synthesis 杜品赫
# @File : DatabaseDebug.py
# @Software : PyCharm
# https://github.com/SynthesisDu/SE_Trandict

# pip install pySide2
import PySide2
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtOpenGL import QGLWidget
from PySide2 import QtCore, QtWidgets, QtOpenGL

import sqlite3

# pyside2-rcc [.qrc] -o [.py]
import icon_Trandict

# https://blog.csdn.net/xufive/article/details/86565130
from OpenGL.GL import *
from OpenGL.GLUT import *

# Main window
class MainWindow:
    def __init__(self, connect):
        qfileStats = QFile('cn_Main.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.connect = connect
        self.cur = self.connect.cursor()
        self.qMainWindow = QUiLoader().load(qfileStats)
        # 控件
        self.qMainWindow.qqqE_A.triggered.connect(self.ActionEA)
        self.qMainWindow.qqqH_A.triggered.connect(self.ActionHA)
        self.qMainWindow.qqqF_Q.triggered.connect(self.ActionFQ)
        self.qMainWindow.qqqButtonHis.clicked.connect(self.ButtonHis)
        self.qMainWindow.qqqButtonGra.clicked.connect(self.ButtonHis)
        self.qMainWindow.qqqVocIn.textChanged.connect(self.VocIn)
        self.qMainWindow.qqqVocIn.textChanged.connect(self.VocInR)
        self.qMainWindow.qqqVocIn.returnPressed.connect(self.VocInR)
        self.qMainWindow.qqqCheckBoxStar.toggled.connect(lambda: self.Box(self.qMainWindow.qqqCheckBoxStar, value = 'star'))
        self.qMainWindow.qqqCheckBoxDone.toggled.connect(lambda: self.Box(self.qMainWindow.qqqCheckBoxDone, value = 'done'))

    def BoxCheck(self, vocab):
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT star, done FROM vocab WHERE vocab == '%s';" % vocab)
            inp = str(self.cur.fetchall()[0])
            star = inp[:inp.find(',')]
            done = inp[inp.find(','):]
            print('===MainWindow.BoxCheck()')
            if '0' in star or 'No' in star:
                self.qMainWindow.qqqCheckBoxStar.setChecked(False)
            elif '1' in star:
                self.qMainWindow.qqqCheckBoxStar.setChecked(True)
            if '0' in done or 'No' in done:
                self.qMainWindow.qqqCheckBoxDone.setChecked(False)
            elif '1' in done:
                self.qMainWindow.qqqCheckBoxDone.setChecked(True)
        except Exception as e:
            pass

    def Box(self, btn, value):
        checkBox = str(btn.checkState())
        if 'Checked' in checkBox:
            check = 1
        elif 'Unchecked' in checkBox:
            check = 0
        vocab = str(self.qMainWindow.qqqVocIn.text())
        vocab = vocab.lower()
        if vocab != '' and vocab is not None:
            try:
                self.cur.execute('UPDATE vocab SET %s = %d WHERE vocab = "%s";' % (value, check, vocab))
                con.commit()
            except Exception as e:
                pass


    def ActionFQ(self):
        self.qMainWindow.close()

    def ActionEA(self):
        statsEA.Load()
        statsEA.qMainWindow.show()

    def ActionHA(self):
        statsHA.qMainWindow.show()

    def ButtonHis(self):
        pass

    def VocIn(self):
        # 刷新
        self.qMainWindow.qqqVocList.clear()
        self.qMainWindow.qqqVocTitle.clear()
        self.qMainWindow.qqqVocCharacter.clear()
        self.qMainWindow.qqqVocWY.clear()
        # 新输入
        info = str(self.qMainWindow.qqqVocIn.text())
        info = info.lower()
        self.BoxCheck(info)
        if info != '':
            re = []
            self.cur.execute("SELECT vocab FROM vocab WHERE vocab LIKE '%s%%';" % info)
            re = re + self.cur.fetchall()
            reS = ''
            try:
                i = 0
                for reR in re:
                    reS += str(reR).replace('(', '').replace("'", '').replace(',', '').replace(')', '').replace(' ', '') + '\n'
                    if i > 20:
                        break
                    i += 1
            except Exception as e:
                reS = '<font color=red>没有匹配的单词</font>'
            self.qMainWindow.qqqVocList.append(reS)

    def VocInR(self):
        # 刷新
        self.qMainWindow.qqqVocTitle.clear()
        self.qMainWindow.qqqVocCharacter.clear()
        self.qMainWindow.qqqVocWY.clear()
        # 主体
        info = str(self.qMainWindow.qqqVocIn.text())
        self.qMainWindow.qqqVocTitle.append(info)
        info = info.lower()
        self.BoxCheck(info)
        # 备加载E_A编辑窗口
        statsEA.qMainWindow.qqqVocab.append(info)
        statsEA.word = info
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT noun, pronoun, adjective, adverb, verb, intransitive_verb, transitive_verb, "
                             "auxiliary_verb, numeral, article, preposition, conjunction, interjection, abbreviation FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0])
            noun = inp[:inp.find(',')].replace("'", '').replace('(', '', 1).replace(',', '')
            inp = inp[inp.find(',') + 1:]
            pronoun = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adjective = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adverb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            intransitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            transitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            auxiliary_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            numeral = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            article = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            preposition = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            conjunction = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            interjection = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            if inp.find(',') == -1:
                abbreviation = inp.replace("'", '').replace('(', '').replace(',', '').replace(')', '')
            else:
                abbreviation = inp[:inp.find(',')].replace("'", '').replace('(', '').replace(',', '').replace(')', '')
            re = ''
            if noun != '' and noun != 'None' and noun != ' ':
                re += 'n.' + noun + '\n'
            if pronoun != '' and pronoun != 'None' and pronoun != ' ':
                re += 'porn.' + pronoun + '\n'
            if adjective != '' and adjective != 'None' and adjective != ' ':
                re += 'adj.' + adjective + '\n'
            if adverb != '' and adverb != 'None' and adverb != ' ':
                re += 'adv.' + adverb + '\n'
            if verb != '' and verb != 'None' and verb != ' ':
                re += 'v.' + verb + '\n'
            if intransitive_verb != '' and intransitive_verb != 'None' and intransitive_verb != ' ':
                re += 'vi.' + intransitive_verb + '\n'
            if transitive_verb != '' and transitive_verb != 'None' and transitive_verb != ' ':
                re += 'vt.' + transitive_verb + '\n'
            if auxiliary_verb != '' and auxiliary_verb != 'None' and auxiliary_verb != ' ':
                re += 'aux.' + auxiliary_verb + '\n'
            if numeral != '' and numeral != 'None' and numeral != ' ':
                re += 'num.' + numeral + '\n'
            if article != '' and article != 'None' and article != ' ':
                re += 'art.' + article + '\n'
            if preposition != '' and preposition != 'None' and preposition != ' ':
                re += 'prep.' + preposition + '\n'
            if conjunction != '' and conjunction != 'None' and conjunction != ' ':
                re += 'conj.' + conjunction + '\n'
            if interjection != '' and interjection != 'None' and interjection != ' ':
                re += 'int.' + interjection + '\n'
            if abbreviation != '' and abbreviation != 'None' and abbreviation != ' ':
                re += 'abbr.' + abbreviation + '\n'
            self.qMainWindow.qqqVocCharacter.append(re)
            self.cur.execute("SELECT wyy_additional FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0]).replace('(', '', 1).replace(',)', '')[1:-1]
            if inp != '' and inp != 'on':
                self.qMainWindow.qqqVocWY.append(inp)
        except Exception as e:
            pass

# &E&A window
class EA:
    def __init__(self, connect):
        qfileStats = QFile('cn_EA.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.word = ''
        self.connect = connect
        self.cur = self.connect.cursor()
        self.qMainWindow = QUiLoader().load(qfileStats)
        self.qMainWindow.qqqButtonC.clicked.connect(self.ButtonEA_C)
        self.qMainWindow.qqqButtonOK.clicked.connect(self.ButtonEA_OK)

    def Load(self):
        self.cur.execute("SELECT noun FROM vocab WHERE vocab = '%s';" % self.word)
        noun = str(self.cur.fetchall())
        print(noun)
        # self.qMainWindow.qqqN.setText(noun)
        # self.qMainWindow.qqqPron.setText(pronoun)
        # self.qMainWindow.qqqAdj.setText(adjective)
        # self.qMainWindow.qqqAdv.setText(adverb)
        # self.qMainWindow.qqqV.setText(verb)
        # self.qMainWindow.qqqVi.setText(intransitive_verb)
        # self.qMainWindow.qqqVt.setText(transitive_verb)
        # self.qMainWindow.qqqAux.setText(auxiliary_verb)
        # self.qMainWindow.qqqNum.setText(numeral)
        # self.qMainWindow.qqqArt.setText(article)
        # self.qMainWindow.qqqPrep.setText(preposition)
        # self.qMainWindow.qqqConj.setText(conjunction)
        # self.qMainWindow.qqqInt.setText(interjection)
        # self.qMainWindow.qqqAbb.setText(abbreviation)

    def ButtonEA_C(self):
        self.qMainWindow.close()

    def ButtonEA_OK(self):
        try:
            n = self.qMainWindow.qqqN.text()
            self.cur.execute('UPDATE vocab SET noun = "%s" WHERE vocab = "%s";' % (n, self.word))
            pron = self.qMainWindow.qqqPron.text()
            self.cur.execute('UPDATE vocab SET pronoun = "%s" WHERE vocab = "%s";' % (pron, self.word))
            adj = self.qMainWindow.qqqAdj.text()
            self.cur.execute('UPDATE vocab SET adjective = "%s" WHERE vocab = "%s";' % (adj, self.word))
            adv = self.qMainWindow.qqqAdv.text()
            self.cur.execute('UPDATE vocab SET adverb = "%s" WHERE vocab = "%s";' % (adv, self.word))
            v = self.qMainWindow.qqqV.text()
            self.cur.execute('UPDATE vocab SET verb = "%s" WHERE vocab = "%s";' % (v, self.word))
            vi = self.qMainWindow.qqqVi.text()
            self.cur.execute('UPDATE vocab SET intransitive_verb = "%s" WHERE vocab = "%s";' % (vi, self.word))
            vt = self.qMainWindow.qqqVt.text()
            self.cur.execute('UPDATE vocab SET transitive_verb = "%s" WHERE vocab = "%s";' % (vt, self.word))
            aux = self.qMainWindow.qqqAux.text()
            self.cur.execute('UPDATE vocab SET auxiliary_verb = "%s" WHERE vocab = "%s";' % (aux, self.word))
            num = self.qMainWindow.qqqNum.text()
            self.cur.execute('UPDATE vocab SET numeral = "%s" WHERE vocab = "%s";' % (num, self.word))
            art = self.qMainWindow.qqqArt.text()
            self.cur.execute('UPDATE vocab SET article = "%s" WHERE vocab = "%s";' % (art, self.word))
            prep = self.qMainWindow.qqqPrep.text()
            self.cur.execute('UPDATE vocab SET preposition = "%s" WHERE vocab = "%s";' % (prep, self.word))
            conj = self.qMainWindow.qqqConj.text()
            self.cur.execute('UPDATE vocab SET conjunction = "%s" WHERE vocab = "%s";' % (conj, self.word))
            intv = self.qMainWindow.qqqInt.text()
            self.cur.execute('UPDATE vocab SET interjection = "%s" WHERE vocab = "%s";' % (intv, self.word))
            abb = self.qMainWindow.qqqAbb.text()
            self.cur.execute('UPDATE vocab SET abbreviation = "%s" WHERE vocab = "%s";' % (abb, self.word))
            con.commit()
        except Exception as e:
            pass
        stats.qMainWindow.qqqVocCharacter.clear()
        stats.qMainWindow.qqqVocTitle.clear()
        stats.VocInR()
        self.qMainWindow.close()
        self.qMainWindow.qqqVocab.clear()

# &H&A window
class HA:
    def __init__(self, connect):
        qfileStats = QFile('cn_About.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.connect = connect
        self.cur = self.connect.cursor()
        self.qMainWindow = QUiLoader().load(qfileStats)

if __name__ == '__main__':
    icon_Trandict.check()
    con = sqlite3.connect('Database.db')
    app = QApplication([])
    stats = MainWindow(connect = con)
    stats.qMainWindow.show()
    statsEA = EA(connect = con)
    statsHA = HA(connect = con)
    app.exec_()
    con.close()

