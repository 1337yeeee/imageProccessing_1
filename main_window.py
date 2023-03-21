from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout,
							QLabel, QMainWindow, QSizePolicy, QSlider,
							QVBoxLayout, QWidget, QPushButton)
from PIL import Image, ImageOps
import img_process as imgp
from functools import partial
from time import time


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.channel = "RGB"

		# Create the main widget and layout
		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)

		# Create the image labels and sliders
		self.image1_label = QLabel()
		self.image2_label = QLabel()
		self.out_label = QLabel(self)
		self.out_label.setMaximumSize(250, 250)
		self.out_label.setAlignment(Qt.AlignCenter)
		# self.label_deleted = True
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMinimum(0)
		self.slider.setMaximum(6)
		self.slider.setValue(0)

		# Set up the in/out put images layout
		self.inout_layout = QHBoxLayout()

		# Set up the input layout
		self.input_layout = QVBoxLayout()
		self.input_layout.addWidget(self.image1_label)
		self.input_layout.addWidget(self.image2_label)

		# create a new QVBoxLayout for the output image
		self.out_layout = QVBoxLayout()
		self.out_layout.addWidget(self.out_label)

		# Add input and output layouts to inout
		self.inout_layout.addLayout(self.input_layout)
		self.inout_layout.addLayout(self.out_layout)

		# Add the image labels and sliders to the layout
		self.main_layout.addLayout(self.inout_layout)

		self.slider_layout = QHBoxLayout()
		self.channel_label = QLabel()
		self.channel_label.setText(self.channel)
		self.slider_layout.addWidget(self.slider)
		self.slider_layout.addWidget(self.channel_label)
		self.main_layout.addLayout(self.slider_layout)

		# Set the main widget and layout
		self.setCentralWidget(self.main_widget)

		# Connect the slider to the update_mask function
		self.slider.valueChanged.connect(self.update_channel)

		# Set the default image paths and mask
		self.image1_path = None
		self.image2_path = None
		self.image_out_path = None
		self.mask = Image.new("L", (0, 0))

		# Set the window properties
		self.setWindowTitle("Image Processing")
		self.setGeometry(100, 100, 800, 800)

		# Create the file menu and add the open image actions
		file_menu = self.menuBar().addMenu("&File")
		open_image1_action = file_menu.addAction("Open &Image 1")
		open_image1_action.triggered.connect(self.open_image1)
		open_image2_action = file_menu.addAction("Open &Image 2")
		open_image2_action.triggered.connect(self.open_image2)

		# Create the magic menu and add the processing image actions
		magic_menu = self.menuBar().addMenu("&Magic")
		magic_sum_action = magic_menu.addAction("Add images")
		magic_sum_action.triggered.connect(self.magic_sum)
		magic_avg_action = magic_menu.addAction("Average images")
		magic_avg_action.triggered.connect(self.magic_avg)
		magic_max_action = magic_menu.addAction("Maximum images")
		magic_max_action.triggered.connect(self.magic_max)
		magic_min_action = magic_menu.addAction("Minimum images")
		magic_min_action.triggered.connect(self.magic_min)
		magic_mult_action = magic_menu.addAction("Multiply images")
		magic_mult_action.triggered.connect(self.magic_mult)
		magic_mask_action = magic_menu.addAction("Square mask images")
		magic_mask_action.triggered.connect(partial(self.magic_mask, mask_mode="S"))
		magic_mask_action = magic_menu.addAction("Circle mask images")
		magic_mask_action.triggered.connect(partial(self.magic_mask, mask_mode="C"))

		# Buttons
		self.button1 = QPushButton("Button 1")
		self.button1.clicked.connect(self.button1_clicked)
		self.button2 = QPushButton("Button 2")
		self.button2.clicked.connect(self.button2_clicked)
		self.button3 = QPushButton("Button 3")
		self.button3.clicked.connect(self.button3_clicked)
		self.button4 = QPushButton("Hide Output")
		self.button4.clicked.connect(self.button4_clicked)

		button_layout = QHBoxLayout()
		button_layout.addWidget(self.button1)
		button_layout.addWidget(self.button2)
		button_layout.addWidget(self.button3)
		button_layout.addWidget(self.button4)

		self.main_layout.addLayout(button_layout)


	def open_image1(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getOpenFileName(self, "Open Image 1", "", "Image Files (*.png *.jpg *.bmp)", options=options)
		if file_name:
			self.image1_path = file_name
			image = QImage(file_name)
			image = self.scale_image(image, 250, 250)
			self.image1_label.setPixmap(QPixmap.fromImage(image))

	def open_image2(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		file_name, _ = QFileDialog.getOpenFileName(self, "Open Image 2", "", "Image Files (*.png *.jpg *.bmp)", options=options)
		if file_name:
			self.image2_path = file_name
			image = QImage(file_name)
			image = self.scale_image(image, 250, 250)
			self.image2_label.setPixmap(QPixmap.fromImage(image))

	def open_image_out(self, file_name):
		if file_name:
			self.image_out_path = file_name
			image = QImage(file_name)
			image = self.scale_image(image, 250, 250)
			self.out_label.setPixmap(QPixmap.fromImage(image))

	def scale_image(self, image, max_width, max_height):
		width, height = image.width(), image.height()
		aspect_ratio = width / height

		# Scale the image while maintaining aspect ratio
		if width > max_width:
			width = max_width
			height = int(width / aspect_ratio)

		if height > max_height:
			height = max_height
			width = int(height * aspect_ratio)

		return image.scaled(width, height, Qt.KeepAspectRatio)    

	def button1_clicked(self):
		print("Button 1 clicked")
		self.open_image_out(imgp.sumImage(self.image1_path, self.image2_path))

	def button2_clicked(self):
		print("Button 2 clicked")

	def button3_clicked(self):
		print("Button 3 clicked")

	def button4_clicked(self):
		print("Button 4 clicked")
		# self.image_out_path = None
		# if self.out_label and not self.label_deleted:
		# 	self.out_label.deleteLater()
		# 	self.label_deleted = True

	def magic_sum(self):
		self.open_image_out(imgp.sumImage(self.image1_path, self.image2_path))

	def magic_avg(self):
		self.open_image_out(imgp.avgImage(self.image1_path, self.image2_path))

	def magic_max(self):
		self.open_image_out(imgp.maxImage(self.image1_path, self.image2_path))

	def magic_min(self):
		self.open_image_out(imgp.minImage(self.image1_path, self.image2_path))

	def magic_mult(self):
		self.open_image_out(imgp.multImage(self.image1_path, self.image2_path))

	def magic_mask(self, mask_mode="C"):
		self.open_image_out(imgp.maskImage(self.image1_path, mask_mode, self.channel))

	def update_channel(self):
		# Update the chanel based on the slider value
		channels = ["RGB", "R", "G", "B", "RG", "GB", "RB"]
		self.channel = channels[self.slider.value()]
		self.channel_label.setText(self.channel)
