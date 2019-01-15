# coding: utf-8

import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QAbstractButton
from PyQt5.QtCore import QDateTime, QDate,QTime, Qt, QCoreApplication,QSize
import musicInfo as musInf
import matplotlib.pyplot as plt
class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

def create_QPixmap(image):
	#qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 4, QtGui.QImage.Format_ARGB32_Premultiplied)
	pixmap = QtGui.QPixmap.fromImage(image)
	return pixmap

class Window(QMainWindow):
	#コンストラクタ
	def __init__(self,path1,path2):
		#親クラス初期化
		super().__init__()

		self.title = "musicTree"
		self.top = 0
		self.left = 2000
		self.width = 400
		self.height = 600

		#反映されない？
		self.setWindowIcon(QtGui.QIcon("./icon.png"))
		#button
		#self.JacietButton1 = PicButton(QPixmap("./icon.png"),self)
		self.JacketButton1 = QPushButton("",self)
		self.JacketButton1.move(30,120)
		self.JacketButton1.resize(150,150)
		self.JacketButton1.setToolTip("<h3>ポイント時に表示される文字</h3>")
		self.JacketButton1.setIcon(QtGui.QIcon("./icon.png"))
		self.JacketButton1.setIconSize(QSize(130,130))
		#self.JacketButton1.setFlat(True)
		#self.JacketButton1.setPixmap(QPixmap("./icon.png"))
		self.JacketButton1.clicked.connect(self.Close)

		self.backButton1 = QPushButton("B",self)
		self.backButton1.move(35,280)
		self.backButton1.resize(40,40)
		self.backButton1.setToolTip("<h3>戻る</h3>")
		self.backButton1.clicked.connect(self.printMessage)
		self.playButton1 = QPushButton("P",self)
		self.playButton1.move(85,280)
		self.playButton1.resize(40,40)
		self.playButton1.setToolTip("<h3>再生</h3>")
		self.playButton1.clicked.connect(self.printMessage)
		self.nextButton1 = QPushButton("N",self)
		self.nextButton1.move(135,280)
		self.nextButton1.resize(40,40)
		self.nextButton1.setToolTip("<h3>次へ</h3>")
		self.nextButton1.clicked.connect(self.printMessage)

		self.JacketButton2 = QPushButton("JacketButton2",self)
		self.JacketButton2.move(220,120)
		self.JacketButton2.resize(150,150)
		self.JacketButton2.setToolTip("<h3>とじる</h3>")
		self.JacketButton2.clicked.connect(self.Close)

		self.backButton2 = QPushButton("B",self)
		self.backButton2.move(35+190,280)
		self.backButton2.resize(40,40)
		self.backButton2.setToolTip("<h3>戻る</h3>")
		self.backButton2.clicked.connect(self.printMessage)
		self.playButton2 = QPushButton("P",self)
		self.playButton2.move(85+190,280)
		self.playButton2.resize(40,40)
		self.playButton2.setToolTip("<h3>再生</h3>")
		self.playButton2.clicked.connect(self.printMessage)
		self.nextButton2 = QPushButton("N",self)
		self.nextButton2.move(135+190,280)
		self.nextButton2.resize(40,40)
		self.nextButton2.setToolTip("<h3>次へ</h3>")
		self.nextButton2.clicked.connect(self.printMessage)
		
		"""
		self.button3 = QPushButton("シエルさん",self)
		self.button3.move(300,300)
		self.button3.setToolTip("<h3>シラントくん</h3>")
		self.button3.clicked.connect(self.printMessage)

		self.button4 = QPushButton("パンくん",self)
		self.button4.move(300,400)
		self.button4.setToolTip("<h3>パンくん</h3>")
		self.button4.clicked.connect(self.printMessage)
		"""
		self.InitWindow()
		self.music = ["",""]
		self.setMusic(n = 0,path = path1)
		self.setMusic(n = 1,path = path2)
	def setMusic(self,n,path):
		self.music[n] = musInf.musInfo(path)
		print(self.music[n].title)
		#plt.imshow(self.music[n].img_numpy)
		#plt.show()
		pic = QtGui.QIcon(variant = self.music[n].img_numpy)
		#pic = create_QPixmap(self.music[n].img_pil.convert("RGBA"))
		#if n == 0:
		#	self.JacketButton1.setIcon(QtGui.QIcon(pic))
		#else:
		#	self.JacketButton2.setIcon(QtGui.QIcon(pic))


	def InitWindow(self):
		#多分構造体内で設定された内容から設定を作ってる？
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		#window拡縮禁止処理
		self.setMinimumHeight(self.height)
		self.setMinimumWidth(self.width)
		self.setMaximumHeight(self.height)
		self.setMaximumWidth(self.width)
		
		self.statusBar()
		self.statusBar().showMessage("test")
		
		self.show()

	def printMessage(self):
		if self.sender()  == self.backButton2 or self.sender()  == self.backButton1:
			print("back")
		elif self.sender()  == self.playButton2 or self.sender()  == self.playButton1:
			print("play")
		elif self.sender()  == self.nextButton2 or self.sender()  == self.nextButton1:
			print("next")
		#print(message)

	def Close(self):
		print("close")
		QCoreApplication.instance().quit()

def main():
	App = QApplication(sys.argv)
	path1 = r"/Users/arc/Music/iTunes/iTunes Media/Music/Toby Fox/DELTARUNE Chapter 1 OST/33 THE WORLD REVOLVING.mp3"
	path2 = r"/Users/arc/Music/iTunes/iTunes Media/Music/Toby Fox/DELTARUNE Chapter 1 OST/33 THE WORLD REVOLVING.mp3"
	window = Window(path1,path2)
	sys.exit(App.exec())

def differenceOfTime():
	#時刻まで
	datetime = QDateTime.currentDateTime()
	print(datetime.toString())
	print(datetime.toString(Qt.ISODate))
	print(datetime.toString(Qt.DefaultLocaleLongDate))

	#日まで
	date = QDate.currentDate()
	print(date.toString())
	print(date.toString(Qt.ISODate))
	print(date.toString(Qt.DefaultLocaleLongDate))

	#時刻のみ
	time = QTime.currentTime()
	print(time.toString())
	print(time.toString(Qt.ISODate))
	print(time.toString(Qt.DefaultLocaleLongDate))

	#月が何日かとかも取得できる

if __name__ == '__main__':
	#differenceOfTime()
	main()