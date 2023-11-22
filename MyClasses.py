from PyQt5.QtWidgets import QWidget, QApplication, QMenu, QDesktopWidget, QLabel, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
import sys
import os
import time
import matplotlib.pyplot as plt


class MY桌宠(QWidget):
    def __init__(self, parent=None):
        super(MY桌宠, self).__init__(parent)

        ### 初始化
        self.__initdata()
        self.__initui()

    def __initdata(self):
        '''
        获取与定义（传入）初始数据
        :return:
        '''
        self.状态: tuple = ("静息", "静息")  # 0为上次更新时状态，1为当下状态
        self.time: dict = {"静息": 853, }  # 意思是静息状态有853张图片
        self.i = 1  # 计时器，固定时间后切换桌宠形态

        ### 获取屏幕大小
        screen = QDesktopWidget().screenGeometry()  # 获取屏幕的几何信息
        self.screenW = screen.width()  # 获取屏幕的宽度
        self.screenH = screen.height()  # 获取屏幕的高度

        ### 设置窗口大小
        self.windowW, self.windowH = 280, 170
    def __initui(self):
        """
        初始化窗口
        :return:
        """
        ### 会不间断的调用槽函数
        self.timer = QTimer()
        self.timer.setInterval(15)  # 设置每多少毫秒调用槽函数
        self.timer.timeout.connect(self.__timeChanged)
        self.timer.start()

        ### 初始化窗口内容
        self.label = QLabel(self)  # 定义一个控件，用于存放图片
        self.__显示窗口内容()

        ### 设置窗口状态
        W, H = self.size().width(), self.size().height()  # 获取窗口大小
        self.move(self.screenW-W, self.screenH-H-20)  # 设置窗口位置
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去除界面边框
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 将窗口始终置顶
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明
        self.setMouseTracking(False)  # 禁用鼠标追踪

        ### 显示窗口
        self.show()

    def __timeChanged(self):
        if self.状态[0] == self.状态[1]:
            self.i += 1
            if self.i > self.time[self.状态[1]]:
                self.i = 1
            ### 可以在这里设定一个时间（或随机数）来更换状态
        else:
            self.i = 1
        self.__显示窗口内容()

    def __显示窗口内容(self):
        self.update()
        图片路径 = f"./img/{self.状态[1]}/{self.i}.png"  # 需要自行修改图片路径，保存规则就是这样
        image = QImage(图片路径)  # 导入图片
        W, H = image.width(), image.height()
        缩放倍数 = 0.2
        image = image.scaled(int(W*缩放倍数), int(H*缩放倍数))  # 对图片进行缩放
        self.pix = QPixmap.fromImage(image)  # 绘制图片
        self.resize(self.pix.size())  # 调整窗口大小为图片的大小
        self.setMask(self.pix.mask())  # 设置窗口的遮罩，使窗口形状与图片轮廓相匹配
        # 在窗口上添加新的 QLabel 控件来显示图片
        self.label.setPixmap(self.pix)
        # 初始化拖动位置变量，用于记录鼠标拖动时的起始位置
        self.dragPosition = None

    def mouseMoveEvent(self, event) -> None:
        '''
        跟随鼠标移动
        :param event:
        :return:
        '''
        xy = event.pos()
        鼠标坐标 = self.mapToGlobal(xy)

        self.move(鼠标坐标.x()-self.__相对位置[0], 鼠标坐标.y()-self.__相对位置[1])
        self.update()

    def mousePressEvent(self, event) -> None:
        '''
        鼠标点击事件
        :param event:
        :return:
        '''
        buttons = event.button()
        if buttons == Qt.NoButton:
            print('没有按下鼠标键')
        elif buttons == Qt.LeftButton:
            print('按下鼠标左键')
            self.__鼠标相对窗口坐标(event)
        elif buttons == Qt.RightButton:
            print('按下鼠标右键')
        elif buttons == Qt.MiddleButton:
            print('按下鼠标中键')
    def mouseReleaseEvent(self, event) -> None:
        '''
        鼠标放开事件
        :param event:
        :return:
        '''
        print('鼠标键放开了')

    def contextMenuEvent(self, e):
        '''
        右键菜单
        :param e:
        :return:
        '''
        cmenu = QMenu(self)
        act1 = cmenu.addAction("退出")
        act2 = cmenu.addAction("最小化")
        action = cmenu.exec_(self.mapToGlobal(e.pos()))
        if action == act1:
            sys.exit(0)
        elif action == act2:
            self.showMinimized()

    def __鼠标相对窗口坐标(self, event):
        '''
        在鼠标点击时，保存鼠标相对于窗口的坐标
        :param event:
        :return:
        '''
        xy = event.pos()
        鼠标坐标 = self.mapToGlobal(xy)
        窗口坐标 = self.pos()
        self.__相对位置 = (鼠标坐标.x() - 窗口坐标.x(), 鼠标坐标.y() - 窗口坐标.y())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MY桌宠()
    sys.exit(app.exec_())