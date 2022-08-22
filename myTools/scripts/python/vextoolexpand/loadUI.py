try:
    from vextoolexpand import initUI
    from vextoolexpand.initUI import Ui_Form
except:
    import initUI
    from initUI import Ui_Form

from imp import reload
from operator import truediv
from shelve import Shelf
from PySide2 import QtCore, QtGui, QtWidgets

import sys
import hou
import os
import vexpressionmenu

reload(initUI)

class loadUI(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self._path = 'E:/Github/customTools-master/myTools/vex/'
        self._file = ''
        self._text1 = ''
        self._text2 = ''
        self._text3 = ''
        self._text4 = ''
        self._text5 = ''
        self._text6 = ''

        #Ui_Form.__init__(self)
        
        self.setupUi(self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        self.setLayout(self.gridLayout)

        
        ###set item1#######
        self.setComboBox(self.comboBox_1)
        self.comboBox_1.setLineEdit(self.lineEdit_1)
        self.lineEdit_1.setText(self.comboBox_1.itemText(0))
        self.comboBox_1.activated.connect(lambda:self.updateCode(self.lineEdit_1, self.textEdit_1, self._text1))
        self.btn_to_1.clicked.connect(lambda:self.data(self.textEdit_1))
        self.btn_save_1.clicked.connect(lambda:self.saveCode(self.lineEdit_1.text(), self.lineEdit_1, self.textEdit_1))
        self.btn_update_1.clicked.connect(self.updateCode(self.lineEdit_1, self.textEdit_1, self._text1))
        self.btn_from_1.clicked.connect(lambda:self.fromWrangle(self.textEdit_1))

        ###set item2#######
        self.setComboBox(self.comboBox_2)
        self.comboBox_2.setLineEdit(self.lineEdit_2)
        self.lineEdit_2.setText(self.comboBox_2.itemText(1))
        self.comboBox_2.activated.connect(lambda:self.updateCode(self.lineEdit_2, self.textEdit_2, self._text2))
        self.btn_to_2.clicked.connect(lambda:self.data(self.textEdit_2))
        self.btn_save_2.clicked.connect(lambda:self.saveCode(self.lineEdit_2.text(), self.lineEdit_2, self.textEdit_2))
        self.btn_update_2.clicked.connect(self.updateCode(self.lineEdit_2, self.textEdit_2, self._text2))
        self.btn_from_2.clicked.connect(lambda:self.fromWrangle(self.textEdit_2))

        ###set item3#######
        self.setComboBox(self.comboBox_3)
        self.comboBox_3.setLineEdit(self.lineEdit_3)
        self.lineEdit_3.setText(self.comboBox_2.itemText(2))
        self.comboBox_3.activated.connect(lambda:self.updateCode(self.lineEdit_3, self.textEdit_3, self._text3))
        self.btn_to_3.clicked.connect(lambda:self.data(self.textEdit_3))
        self.btn_save_3.clicked.connect(lambda:self.saveCode(self.lineEdit_3.text(), self.lineEdit_3, self.textEdit_3))
        self.btn_update_3.clicked.connect(self.updateCode(self.lineEdit_3, self.textEdit_3, self._text3))
        self.btn_from_3.clicked.connect(lambda:self.fromWrangle(self.textEdit_3))

        ###set item4#######
        self.setComboBox(self.comboBox_4)
        self.comboBox_4.setLineEdit(self.lineEdit_4)
        self.lineEdit_4.setText(self.comboBox_4.itemText(3))
        self.comboBox_4.activated.connect(lambda:self.updateCode(self.lineEdit_4, self.textEdit_4, self._text4))
        self.btn_to_4.clicked.connect(lambda:self.data(self.textEdit_4))
        self.btn_save_4.clicked.connect(lambda:self.saveCode(self.lineEdit_4.text(), self.lineEdit_4, self.textEdit_4))
        self.btn_update_4.clicked.connect(self.updateCode(self.lineEdit_4, self.textEdit_4, self._text4))
        self.btn_from_4.clicked.connect(lambda:self.fromWrangle(self.textEdit_4))

        ###set item5#######
        self.setComboBox(self.comboBox_5)
        self.comboBox_5.setLineEdit(self.lineEdit_5)
        self.lineEdit_5.setText(self.comboBox_5.itemText(4))
        self.comboBox_5.activated.connect(lambda:self.updateCode(self.lineEdit_5, self.textEdit_5, self._text5))
        self.btn_to_5.clicked.connect(lambda:self.data(self.textEdit_5))
        self.btn_save_5.clicked.connect(lambda:self.saveCode(self.lineEdit_5.text(), self.lineEdit_5, self.textEdit_5))
        self.btn_update_5.clicked.connect(self.updateCode(self.lineEdit_5, self.textEdit_5, self._text5))
        self.btn_from_5.clicked.connect(lambda:self.fromWrangle(self.textEdit_5))

        ###set item6#######
        self.setComboBox(self.comboBox_6)
        self.comboBox_6.setLineEdit(self.lineEdit_6)
        self.lineEdit_6.setText(self.comboBox_6.itemText(5))
        self.comboBox_6.activated.connect(lambda:self.updateCode(self.lineEdit_6, self.textEdit_6, self._text6))
        self.btn_to_6.clicked.connect(lambda:self.data(self.textEdit_6))
        self.btn_save_6.clicked.connect(lambda:self.saveCode(self.lineEdit_6.text(), self.lineEdit_6, self.textEdit_6))
        self.btn_update_6.clicked.connect(self.updateCode(self.lineEdit_6, self.textEdit_6, self._text6))
        self.btn_from_6.clicked.connect(lambda:self.fromWrangle(self.textEdit_6))
        
        
        ##################
        self.show()

    def showInfo(self):
        print('hello houdini')

    def data(self, textEdit : QtWidgets.QTextEdit):
        self.vexnode(textEdit.toPlainText())

    def vexnode(self, text : str):
        node = hou.selectedNodes()[0]
        if node is None:
            print('please select wrangle node')
        else:
            node.parm('snippet').set(text)

        vexpressionmenu.createSpareParmsFromChCalls(node, 'snippet')

    def fromWrangle(self, textEdit):
        node = hou.selectedNodes()[0]
        code = node.parm('snippet').eval()
        textEdit.setText(code)

    def saveCode(self, file, lineEdit, textEdit):
        path = self._path + file + '.vfl'
        title = lineEdit.text()
        text = textEdit.toPlainText()

        with open(path, 'w') as f:
            f.write(text)

        print('Save code successful')

    def updateCode(self, lineEdit, textEdit, text):
        path = self._path + lineEdit.text() + '.vfl'
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = f.read()
                f.seek(0, 0)
                head = lineEdit.text()
                lineEdit.setText(head)
                textEdit.setText(data)
        else:
            pass


    def setComboBox(self, comboBox:QtWidgets.QComboBox):
        path = self._path
        for root, folders, files in os.walk(path):
            for file in files:
                ext = os.path.splitext(file)
                if ext[1] == '.vfl':
                    comboBox.addItem(ext[0])

    


    @property
    def text1(self):
        return self._text1
    @text1.setter
    def text1(self, text):
        self._text1 = text



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = loadUI.load()
    sys.exit(app.exec_())
