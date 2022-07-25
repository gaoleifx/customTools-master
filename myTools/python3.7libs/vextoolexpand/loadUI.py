try:
    from vextoolexpand import initUI
    from vextoolexpand.initUI import Ui_Form
except:
    import initUI
    from initUI import Ui_Form

from imp import reload
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
        self._path = 'D:/Github/customTools-master/myTools/script/vex/'
        self._file = ''
        self._text1 = ''
        self._text2 = ''
        self._text3 = ''
        self._text4 = ''
        self._text5 = ''

        #Ui_Form.__init__(self)
        
        self.setupUi(self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        self.setLayout(self.gridLayout)
        
        ###set slot
        self.lineEdit_1.setText('AddOrientForPoints')
        self.textEdit_1.setText(self._text1)
        self.btn_to_1.clicked.connect(lambda:self.data(self.textEdit_1))
        self.btn_save_1.clicked.connect(lambda:self.saveCode(self.lineEdit_1.text(), self.lineEdit_1, self.textEdit_1))
        self.btn_update_1.clicked.connect(self.updateCode(self.lineEdit_1.text(), self.textEdit_1, self._text1))
        self.btn_from_1.clicked.connect(lambda:self.fromWrangle(self.textEdit_1))

        self.lineEdit_2.setText('AddPscaleAttribForPar')
        self.textEdit_2.setText(self._text2)
        self.btn_to_2.clicked.connect(lambda:self.data(self.textEdit_2))
        self.btn_save_2.clicked.connect(lambda:self.saveCode(self.lineEdit_2.text(), self.lineEdit_2, self.textEdit_2))
        self.btn_update_2.clicked.connect(self.updateCode(self.lineEdit_2.text(), self.textEdit_2, self._text2))
        self.btn_from_2.clicked.connect(lambda:self.fromWrangle(self.textEdit_2))
        
        
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
            f.write('/////{0}\n\n'.format(title))
            f.write(text)

        print('Save code successful')

    def updateCode(self, file, textEdit, text):
        path = self._path + file + '.vfl'
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = f.read()
                text = data
                textEdit.setText(text)
                print('Update code successful')
        else:
            pass




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
