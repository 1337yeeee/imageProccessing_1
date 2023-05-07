from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
	QPushButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont
from PIL.ImageQt import ImageQt
import freq_process as imgfqp
from time import time



class FreqWindow(QMainWindow):
	def __init__(self, img, parent=None):
		super().__init__(parent)

		self.img_raw = img
		self.img_out = None
		self.img_fourier = None

		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)

		self.button_layout = QHBoxLayout()
		self.top_layout = QHBoxLayout()
		self.bot_layout = QHBoxLayout()

		self._button = QPushButton('Make')
		self._button.clicked.connect(self._button_clicked)
		self.button_layout.addWidget(self._button)

		# input image
		self.image_raw_layout = QVBoxLayout()
		qimage_raw = ImageQt(self.img_raw)
		self.image_raw = QLabel()
		self.image_raw.setPixmap(QPixmap.fromImage(qimage_raw).scaled(QSize(250, 250), aspectRatioMode=Qt.KeepAspectRatio))
		self.image_raw.mousePressEvent = self.on_image_raw_clicked
		self.image_raw_label = QLabel()
		self.image_raw_label.setText('Input image')
		self.image_raw_layout.addWidget(self.image_raw)
		self.image_raw_layout.addWidget(self.image_raw_label)

		self.top_layout.addLayout(self.image_raw_layout)

		# output image
		self.image_out_layout = QVBoxLayout()
		self.image_out = QLabel()
		self.image_out.mousePressEvent = self.on_image_out_clicked
		self.image_out_label = QLabel()
		self.image_out_label.setText('Processed image')
		self.image_out_layout.addWidget(self.image_out)
		self.image_out_layout.addWidget(self.image_out_label)

		self.bot_layout.addLayout(self.image_out_layout)

		self.time_label = QLabel(self)
		self.time_label.setAlignment(Qt.AlignBottom)

		self.main_layout.addLayout(self.button_layout)
		self.main_layout.addLayout(self.top_layout)
		self.main_layout.addLayout(self.bot_layout)
		self.main_layout.addWidget(self.time_label)

		self.setCentralWidget(self.main_widget)
		self.setWindowTitle("Filtering")
		self.setGeometry(300, 0, 550, 550)

	def on_image_raw_clicked(self, event):
		if self.img_raw is not None:
			self.img_raw.show()

	def on_image_out_clicked(self, event):
		if self.img_out is not None:
			self.img_out.show()

	def _button_clicked(self):
		t1 = time()
		self.img_out = imgfqp.make(self.img_raw)
		if self.img_out:
			self.time_label.setText("%.6f seconds"%(time()-t1))
			qimage_out = ImageQt(self.img_out)
			self.image_out.setPixmap(QPixmap.fromImage(qimage_out).scaled(QSize(250, 250), aspectRatioMode=Qt.KeepAspectRatio))
		else:
			exit(0)
