from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout,
							QLabel, QMainWindow, QSizePolicy, QSlider,
							QVBoxLayout, QWidget, QPushButton, QFrame)
import img_process as imgp
from image_panel import ImagePanel
from gisto import GistoWindow, GistoWidget
from functools import partial
from time import time


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.image_out_path = None
		self.gisto_window = None
		self.gistogram = None

		# Create the main widget and layout
		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)

		# Create the out image label and connect to its layout
		self.out_layout = QVBoxLayout()
		self.out_label = QLabel(self)
		self.out_label.setFixedSize(400, 400)
		self.out_label.setAlignment(Qt.AlignCenter)
		self.out_layout.addWidget(self.out_label)

		# Create widget to display a histogram
		self.gistogram_widget = QWidget()
		self.gistogram_widget.setFixedSize(400, 150)
		self.out_layout.addWidget(self.gistogram_widget)

		# Create label for timing and connect to out layout
		self.time_label = QLabel(self)
		self.time_label.setAlignment(Qt.AlignBottom)
		self.out_layout.addWidget(self.time_label)


		# Create working layout and connecting out_label
		self.working_layout = QHBoxLayout()
		self.working_layout.addLayout(self.out_layout)

		# Create image_panel
		self.image_panel = ImagePanel()

		# Create input_layout
		self.input_layout = QVBoxLayout()
		self.input_layout.addWidget(self.image_panel)

		# Create apply button
		self.apply_button = QPushButton("Apply")
		self.apply_button.clicked.connect(self.apply_filters)
		self.input_layout.addWidget(self.apply_button)

		# Create a frame widget and set its properties as a divider
		frame = QFrame()
		frame.setFrameShape(QFrame.VLine)
		frame.setFrameShadow(QFrame.Sunken)

		# Connect layouts
		self.working_layout.addWidget(frame)
		self.working_layout.addLayout(self.input_layout)
		self.main_layout.addLayout(self.working_layout)

		# Create menu-option and connect it to add image
		magic_menu = self.menuBar().addMenu("&Magic")
		magic_add_img_action = magic_menu.addAction("Add image")
		magic_add_img_action.setShortcut("Ctrl+O")
		magic_add_img_action.triggered.connect(self.add_image_from_file)
		magic_out_action = magic_menu.addAction("Out image")
		magic_out_action.triggered.connect(lambda: self.open_image_out("img/in2.jpg"))

		gisto_menu = self.menuBar().addMenu("&Gisto")
		gisto_action = gisto_menu.addAction("Open gisto window")
		gisto_action.triggered.connect(self.new_gisto_window)
		gisto_make_action = gisto_menu.addAction("Make")
		gisto_make_action.triggered.connect(self.make_gisto_)

		# Set the main widget and layout
		self.setCentralWidget(self.main_widget)

		# Set the window properties
		self.setWindowTitle("Image Processing")
		self.setGeometry(100, 100, 800, 800)

	def add_image_from_file(self):
		# Open a file dialog to select an image file
		options = QFileDialog.Options()
		# options |= QFileDialog.DontUseNativeDialog
		file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Image File", "", "Image Files (*.jpg *.jpeg)", options=options)

		# If a file was selected, add it to the ImagePanel widget
		if file_paths:
			for file_path in file_paths:
				if file_path:
					self.image_panel.add_image(file_path)


	def open_image_out(self, file_name):
		if file_name:
			self.image_out_path = file_name

			if self.gistogram:
				self.gistogram.deleteLater()

			self.gistogram = GistoWidget(self.gistogram_widget, file_name)
			self.gistogram.showGistogram()
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

	def apply_filters(self):
		images = self.image_panel.get_image_widgets()
		out = None

		t1 = time()
		# if any image added
		if len(images):
			opt = images[0].comboBox.currentText()
			img_path = images[0].image_path
			channels = images[0].channel
			out = imgp.apply_filters(opt=opt, img1_name=img_path, img2=None, channels=channels)
		
		# for rest of the images
		# option - the value of the comboBox
		# out - the PIL.Image object - result of image processing
		# channels - value of the slider under the image
		for i in range(1, len(images)):
			opt = images[i].comboBox.currentText()
			img_path = images[i].image_path
			channels = images[i].channel
			out = imgp.apply_filters(opt=opt, img1_name=img_path, img2=out, channels=channels)

		self.time_label.setText("%.6f seconds"%(time()-t1))

		# if out image is gotten, creating a name for the image, saving it
		# then opening it to display on the window
		if out:
			output_name = 'img/out_' + str(int(time())) + '.jpg'
			print('saving output image into ' + output_name)
			out.save(output_name)
			self.open_image_out(output_name)

	def new_gisto_window(self):
		if self.gisto_window is None and self.image_out_path:
			self.gisto_window = GistoWindow(self, self.image_out_path)
			self.gisto_window.show()
			self.gisto_window.closeEvent = lambda event: self.on_gisto_window_closed(event)

	def on_gisto_window_closed(self, event):
		self.gisto_window = None
		event.accept()

	def make_gisto_(self):
		if isinstance(self.gisto_window, GistoWindow):
			self.gisto_window.showGistogram()
