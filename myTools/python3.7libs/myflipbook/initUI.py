from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from myflipbook import StartFlipbook as sf
from imp import reload
import sys

reload(sf)

class flipbookWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QPushButton控件演示')
        self.resize(300, 400)

        mainLayout = QVBoxLayout()

        self.btn2 = QPushButton('图标按钮')
        self.btn2.setIcon(QIcon(QPixmap('E:/0.ART_houdini/HDAS/icons/pilot.png')))
        mainLayout.addWidget(self.btn2)

        self.btn3 = QPushButton('不可用按钮')
        self.btn3.setEnabled(False)
        mainLayout.addWidget(self.btn3)

        self.btn4 = QPushButton('&MyButton')
        self.btn4.setDefault(False)
        self.btn4.clicked.connect(lambda:self.btnInfo(self.btn4))
        mainLayout.addWidget(self.btn4)

        layout1 = QHBoxLayout()
        self.selBtn1 = QPushButton()
        self.selBtn1.setText('...')
        self.selBtn1.setObjectName('browse_button')

        self.label = QLabel()
        self.label.setText(sf.StartFlipbook().directory)
        self.label2 = QLabel()
        self.label2.setText(sf.StartFlipbook().outputPath)

        self.selBtn1.clicked.connect(self.select_file)

        layout1.addWidget(self.selBtn1)
        layout1.addWidget(self.label)
        mainLayout.addLayout(layout1)
        mainLayout.addWidget(self.label2)

        self.setLayout(mainLayout)


    def btnInfo(self, btn):
        sw = sf.StartFlipbook()
        sw.begin()

    def select_file(self):
        # fileName,_ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpentFileName()', '', '(*)')
        # if fileName:
        #     print(fileName, _)
        #     self.label.setText(fileName)

        folder = QFileDialog.getExistingDirectory(self, 'Select Directory')
        sw = sf.StartFlipbook()
        sw.directory = folder
        self.label.setText(folder)
        self.label2.setText(sw.outputPath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = flipbookWin()
    main.show()
    sys.exit(app.exec_())

