import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

# 定义整个程序窗口的类别Winform
class Winform(QWidget):

    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)

        # 设置标题
        self.setWindowTitle("FACE_COVER")
        # self.setObjectName("MainWindow")
        # self.setStyleSheet("#MainWindow{background-color:black}")

        # 实例化QPixmap类，分别为rgb图像，ir图像和黑图的像素子窗口类别
        self.pix = QPixmap()
        self.pix_1 = QPixmap()
        self.pix_2 = QPixmap()

        # 定义每一笔画的起点，终点（未改动的图像上不需要有任何笔记，因此坐标全部初始化为负值）
        self.lastPoint = QPoint(-100, -100)
        self.endPoint = QPoint(-100, -100)

        # 初始化交互界面
        self.initUi()

        # 定义画笔颜色的rgb值（默认为灰色）
        self.r = 96
        self.g = 96
        self.b = 96

        # 定义画笔笔尖的粗细
        self.capSize = 100

        # 创建键盘监听事件
        self.grabKeyboard()

    # 程序窗口的初始化函数
    def initUi(self):
        # 窗口大小设置为1400*700，这样可以鼠标拖动缩放
        self.resize(1400, 700)
        # 固定窗口大小，不可缩放
        # self.setFixedSize(1400, 700)

        # 设置三块画布大小为400*550，背景为黑色
        self.pix = QPixmap(400, 550)  # rgb图像画布
        self.pix.fill(Qt.black)

        self.pix_1 = QPixmap(400, 550)  # ir图像画布
        self.pix_1.fill(Qt.black)

        self.pix_2 = QPixmap(400, 550)  # 黑图画布
        self.pix_2.fill(Qt.black)

        # 初始化rgb图像，ir图像的读取路径变量，以及黑图的保存路径变量
        self.imageName = "C:\\pyqt\\DATA\\1\\RGB\\CQ1\\120_RGB_CQ1_1_"  # rgb读取路径
        self.imgNum = 8535
        self.imageName_1 = "C:\\pyqt\\DATA\\1\\IR\\CQ1\\120_IR_CQ1_1_"  # ir读取路径
        self.imgNum_1 = 8535
        self.savePath = "C:\\pyqt\\DATA\\1\\face_cover\\"  # 黑图保存路径

        # 设置偏移量，保证鼠标的位置和rgb图像画的线点是重合的
        # self.offset = QPoint(self.width() - self.pix.width(), self.height() - self.pix.height())
        self.offset = QPoint(50, 50)  # rgb图像的偏移量
        self.offset_1 = QPoint(500, 50)  # ir图像的偏移量
        self.offset_2 = QPoint(950, 50)  # 黑图的偏移量

        # 可视化rgb图像，ir图像的读取路径变量，以及黑图的保存路径变量
        self.rgbImgNameStr = QTextBrowser(self)
        self.rgbImgNameStr.setText("no image")  # rgb图像初始文字
        self.rgbImgNameStr.resize(360, 30)
        self.rgbImgNameStr.move(50, 10)

        self.irImgNameStr = QTextBrowser(self)
        self.irImgNameStr.setText("no image")  # ir图像初始文字
        self.irImgNameStr.resize(360, 30)
        self.irImgNameStr.move(500, 10)

        self.blackImgSavePath = QTextBrowser(self)
        self.blackImgSavePath.setText("no image to save")  # 保存的黑色图像初始文字
        self.blackImgSavePath.resize(360, 30)
        self.blackImgSavePath.move(950, 10)

        # 各个按钮的初始化与链接
        btn_open = QPushButton(self)
        btn_open.setText("上一张")
        btn_open.resize(80, 30)
        btn_open.move(70, 630)
        btn_open.clicked.connect(self.previousImg)

        btn_open = QPushButton(self)
        btn_open.setText("打开RGB")
        btn_open.resize(80, 30)
        btn_open.move(210, 630)
        btn_open.clicked.connect(self.open)

        btn_clear = QPushButton(self)
        btn_clear.setText("下一张")
        btn_clear.resize(80, 30)
        btn_clear.move(350, 630)
        btn_clear.clicked.connect(self.nextImg)

        btn_save = QPushButton(self)
        btn_save.setText("保存")
        btn_save.resize(80, 30)
        btn_save.move(1200, 630)
        btn_save.clicked.connect(self.save)

        btn_save = QPushButton(self)
        btn_save.setText("删除")
        btn_save.resize(80, 30)
        btn_save.move(1000, 630)
        btn_save.clicked.connect(self.deleteImg)

        btn_save_1 = QPushButton(self)
        btn_save_1.setText("打开IR")
        btn_save_1.resize(80, 30)
        btn_save_1.move(660, 630)
        btn_save_1.clicked.connect(self.open_1)

        # btn_open = QPushButton(self)  # 起初要将rgb和ir图像分别设置下一张的按钮，后来合并此功能
        # btn_open.setText("下一张IR")
        # btn_open.resize(80, 30)
        # btn_open.move(800, 630)
        # btn_open.clicked.connect(self.nextIR)
        #
        # btn_open = QPushButton(self)
        # btn_open.setText("上一张IR")
        # btn_open.resize(80, 30)
        # btn_open.move(520, 630)
        # btn_open.clicked.connect(self.previousIR)

    # 键盘事件响应函数
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.previousImg()  # 如果按A键，则显示上一张
        elif event.key() == Qt.Key_D:
            self.nextImg()  # 如果按D键， 则显示下一张
        elif event.key() == Qt.Key_S:
            self.save()  # 如果按B键， 则保存黑图
        elif event.key() == Qt.Key_C:
            self.clearPenMask()  # 如果按C键， 则清空所有笔迹

    # 黑图保存函数
    def save(self):
        # fileName = QFileDialog.getSaveFileName(self, "保存图片", "C:\\pyqt\\b.png", "*.png")
        # file = open(fileName, 'w')
        self.pix_2.save(self.savePath + str(self.imgNum) + "_fixed" + ".jpg", 'jpg')  # 保存黑色图像
        self.blackImgSavePath.append(self.savePath + str(self.imgNum) + "_fixed" + ".jpg")  # 打印保存路径到窗口

    # ir图像打开函数
    def open_1(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "C:\\pyqt\\DATA\\1\\IR\\CQ1", "*.jpg;;*.png;;All Files(*)")
        # jpg = QPixmap(imgName).scaled(self.pix.width(), self.pix.height())
        self.imageName_1 = imgName[:35]
        self.imgNum_1 = int(imgName[35:39])
        png = QPixmap(imgName)
        # self.label.setPixmap(png)
        self.pix_1.load(imgName)
        self.irImgNameStr.append(imgName)

    # rgb图像打开函数
    def open(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "C:\\pyqt\\DATA\\1\\rgb\\CQ1", "*.jpg;;*.png;;All Files(*)")
        # imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "C:\\pyqt\\DATA\\1\\RGB\\CQ1\\120_RGB_CQ1_1_8535.jpg", "*.jpg;;*.png;;All Files(*)")
        print(QPixmap(imgName).width())
        print(QPixmap(imgName).height())
        # jpg = QPixmap(imgName).scaled(self.pix.width(), self.pix.height())
        print(imgName)
        # print(float(imgName[37:41]))
        self.imageName = imgName[:37]
        self.imgNum = int(imgName[37:41])
        png = QPixmap(imgName)
        # self.label.setPixmap(png)
        self.capSize = QPixmap(imgName).width() * 0.25

        self.pix.load(imgName)
        self.pix_2.load(imgName)
        # self.pix_1.scaled(self.wiDth, self.heiGht)
        self.pix_2.fill(Qt.black)
        self.rgbImgNameStr.append(imgName)

    def clearPenMask(self):
        self.pix.load(self.imageName + str(self.imgNum) + ".jpg")
        self.pix_1.load(self.imageName_1 + str(self.imgNum_1) + ".jpg")
        self.pix_2.load(self.imageName + str(self.imgNum) + ".jpg")
        self.pix_2.fill(Qt.black)

    # 打开下一张图像
    def nextImg(self):
        # 打开rgb图像画布位置的rgb图像，并根据其尺寸重新初始化黑图的尺寸
        self.imgNum = self.imgNum + 1
        self.pix.load(self.imageName + str(self.imgNum) + ".jpg")
        self.pix_2.load(self.imageName + str(self.imgNum) + ".jpg")
        self.pix_2.fill(Qt.black)
        # self.pix.load("C:\\pyqt\\1244.png")
        self.rgbImgNameStr.append(self.imageName + str(self.imgNum) + ".jpg")
        print(self.imageName + str(self.imgNum) + ".jpg")

        # 打开ir图像画布位置的ir图像
        self.imgNum_1 = self.imgNum_1 + 1
        self.pix_1.load(self.imageName_1 + str(self.imgNum_1) + ".jpg")
        # self.pix.load("C:\\pyqt\\1244.png")
        # self.imgNameStr.setPlaceholderText(self.imageName + str(self.imgNum) + ".png")
        self.irImgNameStr.append(self.imageName_1 + str(self.imgNum_1) + ".jpg")
        print(self.imageName_1 + str(self.imgNum_1) + ".jpg")

        # 根据rgb图像的尺寸更新画笔笔尖粗细
        self.capSize = QPixmap(self.imageName + str(self.imgNum) + ".jpg").width() * 0.25

    # def nextIR(self):
    #     self.imgNum_1 = self.imgNum_1 + 1
    #     self.pix_1.load(self.imageName_1 + str(self.imgNum_1) + ".jpg")
    #     # self.pix.load("C:\\pyqt\\1244.png")
    #     # self.imgNameStr.setPlaceholderText(self.imageName + str(self.imgNum) + ".png")
    #     self.irImgNameStr.append(self.imageName_1 + str(self.imgNum_1) + ".jpg")
    #     print(self.imageName_1 + str(self.imgNum_1) + ".jpg")

    # 打开上一张图像
    def previousImg(self):
        # 打开rgb图像画布位置的rgb图像，并根据其尺寸重新初始化黑图的尺寸
        self.imgNum = self.imgNum - 1
        self.pix.load(self.imageName + str(self.imgNum) + ".jpg")
        self.pix_2.load(self.imageName + str(self.imgNum) + ".jpg")
        # self.imgNameStr.setPlaceholderText(self.imageName + str(self.imgNum) + ".png")
        self.rgbImgNameStr.append(self.imageName + str(self.imgNum) + ".jpg")
        self.pix_2.fill(Qt.black)
        print(self.imageName + str(self.imgNum) + ".jpg")

        # 打开ir图像画布位置的ir图像
        self.imgNum_1 = self.imgNum_1 - 1
        self.pix_1.load(self.imageName_1 + str(self.imgNum_1) + ".jpg")
        self.irImgNameStr.append(self.imageName_1 + str(self.imgNum_1) + ".jpg")
        # self.irImgNameStr.append(self.imageName_1 + str(self.imgNum_1) + ".jpg")
        # self.imgNameStr.setPlaceholderText(self.imageName + str(self.imgNum) + ".png")
        print(self.imageName_1 + str(self.imgNum_1) + ".jpg")

        # 根据rgb图像的尺寸更新画笔笔尖粗细
        self.capSize = QPixmap(self.imageName + str(self.imgNum) + ".jpg").width() * 0.25

    # def previousIR(self):
    #     self.imgNum_1 = self.imgNum_1 - 1
    #     self.pix_1.load(self.imageName_1 + str(self.imgNum_1) + ".jpg")
    #     self.irImgNameStr.append(self.imageName_1 + str(self.imgNum_1) + ".jpg")
    #     self.irImgNameStr.append(self.imageName_1 + str(self.imgNum_1) + ".jpg")
    #     # self.imgNameStr.setPlaceholderText(self.imageName + str(self.imgNum) + ".png")
    #     print(self.imageName_1 + str(self.imgNum_1) + ".jpg")

    # 永久删除数据集中的无效图像数据函数
    def deleteImg(self):
        os.remove(self.imageName + str(self.imgNum) + ".jpg")

    # 画图函数
    def paintEvent(self, event):
        # 定义画笔类，设置画笔类型，笔尖粗细，颜色等参数
        pen = QPen()
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setColor(QColor(self.r, self.g, self.b))
        pen.setWidth(self.capSize)

        # 分别定义三块画布上面的painter类，并初始化painter手中的pen
        pp = QPainter(self.pix)  # rgb画布
        pp.setPen(pen)

        pp_1 = QPainter(self.pix_1)  # ir画布
        # pp_1.setPen(QPen(QColor(self.r, self.g, self.b), 40))
        pp_1.setPen(pen)

        pp_2 = QPainter(self.pix_2)  # 黑图画布
        # pp_2.setPen(QPen(QColor(self.r, self.g, self.b), 40))
        pp_2.setPen(pen)

        # 根据鼠标指针前后两个位置绘制直线，只在rgb画布上作图，三幅画布同时在相同位置出现笔迹
        pp.drawLine(self.lastPoint, self.endPoint)
        pp_1.drawLine(self.lastPoint, self.endPoint)
        pp_2.drawLine(self.lastPoint, self.endPoint)

        # 让前一个坐标值等于后一个坐标值，这样能画出连续的线条
        self.lastPoint = self.endPoint

        # 定义绘制画布的painter类
        painter = QPainter(self)

        # 绘制画布到窗口指定位置处
        painter.drawPixmap(50, 50, self.pix)  # rgb图像画布
        painter.drawPixmap(500, 50, self.pix_1)  # ir图像画布
        painter.drawPixmap(950, 50, self.pix_2)  # 黑图画布

    # 鼠标按下事件检测函数
    def mousePressEvent(self, event):
        # 鼠标左键按下
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos() - self.offset
            # 上面这里减去一个偏移量，否则鼠标点的位置和线的位置不对齐
            self.endPoint = self.lastPoint

            print(self.endPoint)
            # print(self.endPoint_1)

    # 鼠标移动事件检测函数
    def mouseMoveEvent(self, event):
        # 鼠标左键按下的同时移动鼠标
        if event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos() - self.offset
            # 进行重新绘制
            self.update()

    # 鼠标释放事件检测函数
    def mouseReleaseEvent(self, event):
        # 鼠标左键释放
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos() - self.offset
            # 进行重新绘制
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Winform()
    form.show()
    sys.exit(app.exec_())
