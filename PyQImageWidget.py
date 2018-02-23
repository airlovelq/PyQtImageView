import sys
import copy
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class QImagePreviewWidget(QWidget):
    def __init__(self,parent=None):
        super(QImagePreviewWidget,self).__init__(parent)
        self.m_xs = 0.0
        self.m_ys = 0.0
        self.m_xp = 0.0
        self.m_yp = 0.0
        self.m_xsf = 0.0
        self.m_ysf = 0.0
        self.m_rect = self.rect()
        #bmpMove = QPixmap('pan.bmp')
        #bmpMove = bmpMove.scaled(32, 32, Qt.KeepAspectRatio)
        #self.CursorMove = QCursor(bmpMove)
        bmpZoom = QPixmap('fangdajing.png')
        bmpZoom = bmpZoom.scaled(32, 32, Qt.KeepAspectRatio)
        self.CursorZoom = QCursor(bmpZoom)
        self.setMouseTracking(True)
        self.bBack = False
        self.color = Qt.black
        self.m_filename = ''

    def loadpic(self, filename):
        self.m_filename = filename

    def paintEvent(self, QPaintEvent):
        p = QPainter(self)
        pic = QPixmap()
        pic.load(self.m_filename)
        if self.bBack:
            p.setBrush(QBrush(self.color,Qt.SolidPattern))
            p.drawRect(self.rect())
        p.drawPixmap(self.m_rect, pic)

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
            rc = copy.deepcopy(self.m_rect)
            self.m_rect.setLeft(rc.left() + e.pos().x() - self.m_xp)
            self.m_rect.setTop(rc.top() + e.pos().y() - self.m_yp)
            self.m_rect.setWidth(rc.width())
            self.m_rect.setHeight(rc.height())
            self.m_xp = e.pos().x()
            self.m_yp = e.pos().y()
        else:
            self.setCursor(Qt.ArrowCursor)
        self.update()

    def wheelEvent(self, e):
        self.setCursor(self.CursorZoom)
        self.m_xsf = e.pos().x()
        self.m_ysf = e.pos().y()
        if e.angleDelta().y() > 0:
            self.m_xs = 0.1
            self.m_ys = 0.1
        else:
            self.m_xs = -0.1
            self.m_ys = -0.1
        rc = copy.deepcopy(self.m_rect)
        self.m_rect.setLeft(int(float(rc.left()) - float((self.m_xsf - rc.left()) * (self.m_xs))))
        self.m_rect.setRight(int(float(rc.right()) + float((rc.right() - self.m_xsf) * (self.m_xs))))
        self.m_rect.setTop(int(float(rc.top()) - float((self.m_ysf - rc.top()) * (self.m_ys))))
        self.m_rect.setBottom(int(float(rc.bottom()) + float((rc.bottom() - self.m_ysf) * (self.m_ys))))
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.m_xp = e.pos().x()
            self.m_yp = e.pos().y()
        if e.button() == Qt.RightButton:
            self.fitWindow()

    def mouseReleaseEvent(self, QMouseEvent):
        self.setCursor(Qt.ArrowCursor)

    def fitWindow(self):
        self.m_rect = self.rect()
        self.update()

    def zoomIn(self):
        rc = self.rect()
        self.m_xsf = (rc.left() + rc.right())/2
        self.m_ysf = (rc.top() + rc.bottom())/2
        self.m_xs = 0.1
        self.m_ys = 0.1
        rc = copy.deepcopy(self.m_rect)
        self.m_rect.setLeft(int(float(rc.left()) - float((self.m_xsf - rc.left()) * (self.m_xs))))
        self.m_rect.setRight(int(float(rc.right()) + float((rc.right() - self.m_xsf) * (self.m_xs))))
        self.m_rect.setTop(int(float(rc.top()) - float((self.m_ysf - rc.top()) * (self.m_ys))))
        self.m_rect.setBottom(int(float(rc.bottom()) + float((rc.bottom() - self.m_ysf) * (self.m_ys))))
        self.update()

    def zoomOut(self):
        rc = self.rect()
        self.m_xsf = (rc.left() + rc.right()) / 2
        self.m_ysf = (rc.top() + rc.bottom()) / 2
        self.m_xs = -0.1
        self.m_ys = -0.1
        rc = copy.deepcopy(self.m_rect)
        self.m_rect.setLeft(int(float(rc.left()) - float((self.m_xsf - rc.left()) * (self.m_xs))))
        self.m_rect.setRight(int(float(rc.right()) + float((rc.right() - self.m_xsf) * (self.m_xs))))
        self.m_rect.setTop(int(float(rc.top()) - float((self.m_ysf - rc.top()) * (self.m_ys))))
        self.m_rect.setBottom(int(float(rc.bottom()) + float((rc.bottom() - self.m_ysf) * (self.m_ys))))
        self.update()

    def resizeEvent(self, QResizeEvent):
        self.fitWindow()

    def setUseBackColor(self, b):
        self.bBack = b

    def setBackColor(self, Color):
        self.color = Color


class QImageWidget(QWidget):
    def __init__(self,parent=None):
        super(QImageWidget,self).__init__(parent)
        self.view = QImagePreviewWidget(self)
        self.fitbtn = QPushButton()
        self.fitbtn.setText('Fit')
        self.inbtn = QPushButton()
        self.inbtn.setText('Zoom In')
        self.outbtn = QPushButton()
        self.outbtn.setText('Zoom Out')
        self.lay = QGridLayout()
        self.lay.addWidget(self.fitbtn, 0, 0)
        self.lay.addWidget(self.inbtn, 0 ,1)
        self.lay.addWidget(self.outbtn, 0, 2)
        self.lay.addWidget(self.view, 1, 0, 1, 3)
        self.lay.setRowStretch(0, 1)
        self.lay.setRowStretch(0, 6)
        self.setLayout(self.lay)
        self.fitbtn.clicked.connect(self.view.fitWindow)
        self.inbtn.clicked.connect(self.view.zoomIn)
        self.outbtn.clicked.connect(self.view.zoomOut)

    def loadpic(self, filename):
        self.view.loadpic(filename)

    def setUseBackColor(self, b):
        self.view.setUseBackColor(b)

    def setBackColor(self, Color):
        self.view.setBackColor(Color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QImageWidget()
    dialog.loadpic('f:/132432.bmp')
    dialog.setMinimumSize(200,300)
    dialog.setUseBackColor(True)
    dialog.setBackColor(Qt.red)
    dialog.show()

    app.exec()



