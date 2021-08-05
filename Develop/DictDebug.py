# # # -*- coding = utf-8 -*-
# # # encoding: utf-8
# # # @Time : 2021.7.28 00:51
# # # @Author : Synthesis 杜品赫
# # # @File : DatabaseDebug.py
# # # @Software : PyCharm
# # # https://github.com/SynthesisDu/SE_Trandict
# #
# # from PySide2.QtWidgets import QApplication, QMessageBox
# # from PySide2.QtUiTools import QUiLoader
# # from PySide2.QtCore import QFile
# #
# # class Stats:
# #
# #     def __init__(self):
# #         # 从文件中加载UI定义
# #         qfileStats = QFile('cn_Main.ui')
# #         qfileStats.open(QFile.ReadOnly)
# #         qfileStats.close()
# #
# #         # 从 UI 定义中动态 创建一个相应的窗口对象
# #         # 注意：里面的控件对象也成为窗口对象的属性了
# #         # 比如 self.qMainWindow.button , self.qMainWindow.textEdit
# #
# #         self.qMainWindow = QUiLoader().load(qfileStats)
# #
# #         self.qMainWindow.buttonHis.clicked.connect(self.ButtonHis)
# #         self.qMainWindow.buttonGra.clicked.connect(self.ButtonHis)
# #         self.qMainWindow.vocIn.textChanged.connect(self.VocabInp)
# #
# #
# #     def ButtonHis(self):
# #         info = self.qMainWindow.vocIn.text()
# #         print(info)
# #
# #     def VocabInp(self):
# #         info = self.qMainWindow.vocIn.text()
# #         print(info)
# #
# # if __name__ == '__main__':
# #     app = QApplication([])
# #     stats = Stats()
# #     stats.qMainWindow.show()
# #     app.exec_()
#

