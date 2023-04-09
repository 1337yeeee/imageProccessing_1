from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
	QLineEdit, QMainWindow, QPushButton)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from binar_process import BinarIMG
from PIL.ImageQt import ImageQt
from time import time


class BinarImage(QWidget):
	def __init__(self, img, name, parent=None):
		super().__init__(parent)

		self.main_layout = QVBoxLayout()
		
		# Convert PIL Image to QImage
		qimage = ImageQt(img)

		# Create QLabel and set QPixmap from QImage
		self.pic = QLabel()
		self.pic.setPixmap(QPixmap.fromImage(qimage).scaled(QSize(250, 250), aspectRatioMode=Qt.KeepAspectRatio))

		# Create name label
		self.name = QLabel()
		self.name.setText(name)

		# Add image and name to the layout
		self.main_layout.addWidget(self.pic)
		self.main_layout.addWidget(self.name)

		self.setLayout(self.main_layout)


class BinarWindow(QMainWindow):
	def __init__(self, image_path, parent=None):
		super().__init__(parent)
		self.image_path = image_path
		self.binar_images = None

		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)
		self.param_layout = QHBoxLayout()

		# Label and input for window size param
		self.window_size_label = QLabel()
		self.window_size_label.setText('Window Size')
		self.window_size_field = QLineEdit()
		self.window_size_field.setInputMask("99")
		self.window_size_field.setText("21")
		self.window_size_field.setFixedWidth(50)

		# Label and input for k param
		self.k_label = QLabel()
		self.k_label.setText('k')
		self.k_field = QLineEdit()
		self.k_field.setInputMask(".99")
		self.k_field.setText("-.2")
		self.k_field.setFixedWidth(50)

		# Label and input for k param
		self.r_label = QLabel()
		self.r_label.setText('r')
		self.r_field = QLineEdit()
		self.r_field.setInputMask("999")
		self.r_field.setText("128")
		self.r_field.setFixedWidth(50)

		# Add all together
		self.param_layout.addWidget(self.window_size_label)
		self.param_layout.addWidget(self.window_size_field)
		self.param_layout.addWidget(self.k_label)
		self.param_layout.addWidget(self.k_field)
		self.param_layout.addWidget(self.r_label)
		self.param_layout.addWidget(self.r_field)

		self.main_layout.addLayout(self.param_layout)

		# Create and add layouts for images
		self.first_row = QHBoxLayout()
		self.second_row = QHBoxLayout()
		self.main_layout.addLayout(self.first_row)
		self.main_layout.addLayout(self.second_row)

		# Create apply button
		self.apply_button = QPushButton("Apply")
		self.apply_button.clicked.connect(self.make_binar_images)
		self.main_layout.addWidget(self.apply_button)

		# Create bottom layout
		self.bottom_layout = QHBoxLayout()
		self.bottom_layout.setAlignment(Qt.AlignBottom)

		# Create label for timing and connect to the bottom layout
		self.time_label = QLabel(self)
		self.bottom_layout.addWidget(self.time_label)

		# Create save ladel
		self.save_ladel = QLabel()
		self.bottom_layout.addWidget(self.save_ladel)

		# Create save button
		self.save_button = QPushButton("Save")
		self.save_button.clicked.connect(self.save_binar_images)
		self.save_button.setEnabled(False)
		self.bottom_layout.addWidget(self.save_button)

		self.main_layout.addLayout(self.bottom_layout)

		self.setCentralWidget(self.main_widget)
		self.setWindowTitle("Binarization")
		self.setGeometry(300, 0, 400, 400)

	def make_binar_images(self):
		window_size = self.window_size_field.text()
		try:
			window_size = int(window_size)
		except:
			print(f'binar_window.py in make_binar_images: error int(window_size): window_size = {window_size}')
			window_size = 21

		k = self.k_field.text()
		try:
			k = float(k)
		except:
			print(f'binar_window.py in make_binar_images: error float(k): k = {k}')
			k = -0.2

		r = self.r_field.text()
		try:
			r = int(r)
		except:
			print(f'binar_window.py in make_binar_images: error int(r): r = {r}')
			r = 128

		t1 = time()
		bin_img = BinarIMG(img_name=self.image_path, window_size=window_size, k=k, r=r)
		self.time_label.setText("%.6f seconds"%(time()-t1))
		self.append_image(bin_img)

	def append_image(self, bin_img):
		self.free_images()
		i = 0
		self.binar_images = bin_img.getimages()
		for name, img in self.binar_images.items():
			bin_img_widget = BinarImage(img=img, name=name)
			if i < 3:
				self.first_row.addWidget(bin_img_widget)
			else:
				self.second_row.addWidget(bin_img_widget)
			i += 1

		self.save_ladel.setText('')
		self.save_button.setEnabled(True)

	def save_binar_images(self):
		if self.binar_images is not None:
			t1 = int(time()*10)%1000
			for name, img in self.binar_images.items():
				img_name = f'img/binar_img_{name}_{t1}.jpg'
				print('saving image into ' + img_name)
				img.save(img_name)
			self.save_ladel.setText('Saved')

	def free_images(self):
		index = self.first_row.count()
		while(index > 0):
			myWidget = self.first_row.itemAt(index-1).widget()
			myWidget.setParent(None)
			index -= 1
		index = self.second_row.count()
		while(index > 0):
			myWidget = self.second_row.itemAt(index-1).widget()
			myWidget.setParent(None)
			index -= 1
