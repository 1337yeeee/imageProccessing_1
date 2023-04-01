from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout,
							QLabel, QMainWindow, QSizePolicy, QSlider,
							QVBoxLayout, QWidget, QPushButton, QFrame,
							QDesktopWidget)
# import img_process as imgp
import img_process_fast as imgp
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
		self.out_label.setFixedSize(400, 300)
		self.out_label.setAlignment(Qt.AlignCenter)
		self.out_layout.addWidget(self.out_label)

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

		binar_menu = self.menuBar().addMenu("&Binary")
		binar_action = binar_menu.addAction("Binary action")
		binar_action.triggered.connect(lambda x: print(x))

		# Set the main widget and layout
		self.setCentralWidget(self.main_widget)

		# Set the window properties
		self.setWindowTitle("Image Processing")
		self.setGeometry(100, 100, 800, 800)
		desktop = QDesktopWidget().availableGeometry()
		self.setFixedSize(800, desktop.height()-28)

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

			self.gistogram = GistoWidget(image_path=file_name)
			self.gistogram.showGistogram()
			self.gistogram.setFixedSize(350, 300)
			# self.out_layout.addWidget(self.gistogram)
			self.out_layout.insertWidget(1, self.gistogram)

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
		images = self.image_panel.get_image_widgets()[::-1]
		out = None

		if len(images) == 0:
			self.time_label.setText("0 seconds")
			return

		t1 = time()

		for i in range(len(images)):
			if i == 0:
				opt = "None"
			else:
				opt = images[i-1].comboBox.currentText()

			img_path = images[i].image_path
			channels = images[i].channel
			out = imgp.apply_filters(opt=opt, img1_name=img_path, img2=out, channels=channels)

		if images[-1].comboBox.currentText() != "None":
			opt = images[-1].comboBox.currentText()
			transparency = self.image_panel.get_mask_transparency()
			out = imgp.apply_filters(opt=opt, img2=out, transparency=transparency)

		self.time_label.setText("%.6f seconds"%(time()-t1))

		self.save_output(out)


	def new_gisto_window(self):
		if self.gisto_window is None and self.image_out_path:
			self.gisto_window = GistoWindow(self)
			self.gisto_window.show()
			self.gisto_window.closeEvent = lambda event: self.on_gisto_window_closed(event)

	def on_gisto_window_closed(self, event):
		self.gisto_window = None
		event.accept()

	def make_gisto_(self):
		if isinstance(self.gisto_window, GistoWindow):
			points = self.gisto_window.get_scene_points()
			t1 = time()
			out = imgp.grad_transform(self.image_out_path, points)
			self.time_label.setText("%.6f seconds"%(time()-t1))
			self.save_output(out)

	def save_output(self, out_img, name=None):
		if out_img is None:
			return

		if name is None:
			name = 'img/out_' + str(int(time())) + '.jpg'

		print('saving output image into ' + name)
		out_img.save(name)
		self.open_image_out(name)
