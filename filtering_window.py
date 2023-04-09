from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
	QLineEdit, QMainWindow, QPushButton, QPlainTextEdit, QFrame, QDesktopWidget)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from functools import partial
from PIL.ImageQt import ImageQt
import filtering_process as imgfp
import re
import numpy as np
from fractions import Fraction
from time import time


class FilterWindow(QMainWindow):
	def __init__(self, img, parent=None):
		super().__init__(parent)
		self.img_raw = img
		self.img_out = None
		self.sub_window = None

		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)

		self.top_layout = QHBoxLayout()

		self.linear_button = QPushButton('Linear')
		self.linear_button.clicked.connect(self.sub_window_open_lin)
		self.top_layout.addWidget(self.linear_button)

		self.mid_button = QPushButton('Median')
		self.mid_button.clicked.connect(self.sub_window_open_med)
		self.top_layout.addWidget(self.mid_button)

		self.gaus_button = QPushButton('Gaus')
		self.gaus_button.clicked.connect(self.sub_window_open_gaus)
		self.top_layout.addWidget(self.gaus_button)

		self.image_layout = QHBoxLayout()

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

		# Create a frame widget and set its properties as a divider
		frame = QFrame()
		frame.setFrameShape(QFrame.VLine)
		frame.setFrameShadow(QFrame.Sunken)

		# output image
		self.image_processed_layout = QVBoxLayout()
		self.image_processed = QLabel()
		self.image_processed.mousePressEvent = self.on_image_out_clicked
		self.image_processed_label = QLabel()
		self.image_processed_label.setText('Processed image')
		self.image_processed_layout.addWidget(self.image_processed)
		self.image_processed_layout.addWidget(self.image_processed_label)

		# Connect to the image layout
		self.image_layout.addLayout(self.image_raw_layout)
		self.image_layout.addWidget(frame)
		self.image_layout.addLayout(self.image_processed_layout)

		self.time_label = QLabel(self)
		self.time_label.setAlignment(Qt.AlignBottom)

		# Connect to the main layout
		self.main_layout.addLayout(self.top_layout)
		self.main_layout.addLayout(self.image_layout)
		self.main_layout.addWidget(self.time_label)

		self.setCentralWidget(self.main_widget)
		self.setWindowTitle("Filtering")
		self.setGeometry(300, 0, 400, 400)

	def on_image_raw_clicked(self, event):
		if self.img_raw is not None:
			self.img_raw.show()

	def on_image_out_clicked(self, event):
		if self.img_out is not None:
			self.img_out.show()

	def sub_window_open_lin(self):
		self.sub_window_open(self._linear_filter, 'Linear Filter')

	def sub_window_open_med(self):
		self.sub_window_open(self._median_filter, 'Median Filter')

	def sub_window_open_gaus(self):
		self.sub_window_open(self._gaussian_filter, 'Gaus Filter')

	def sub_window_open(self, func, window_title):
		if self.sub_window is None:
			self.sub_window = _SubWindow(func, window_title, self)
			self.sub_window.show()
			self.sub_window.closeEvent = lambda event: self.on_sub_window_closed(event)
			
	def on_sub_window_closed(self, event):
		self.sub_window = None
		event.accept()

	def process_callback(self, callback):
		callback()
		
	def some(self, text_field):
		print(text_field)

	# TODO handle the parse_matrix exception
	def _linear_filter(self, text_field):
		t1 = time()
		self.img_out = imgfp.linear_filter(self.img_raw, parse_matrix(text_field, self))
		self.time_label.setText("%.6f seconds"%(time()-t1))
		qimage_out = ImageQt(self.img_out)
		self.image_processed.setPixmap(QPixmap.fromImage(qimage_out).scaled(QSize(250, 250), aspectRatioMode=Qt.KeepAspectRatio))

	def _median_filter(self, text_field):
		t1 = time()
		kernel = parse_matrix(text_field, self)
		if kernel.shape[0]==1 and kernel.shape[1]==1:
			shape = (int(kernel[0,0]),int(kernel[0,0]))
		else:
			shape = kernel.shape
		self.img_out = imgfp.median_filter(self.img_raw, shape)
		self.time_label.setText("%.6f seconds"%(time()-t1))
		qimage_out = ImageQt(self.img_out)
		self.image_processed.setPixmap(QPixmap.fromImage(qimage_out).scaled(QSize(250, 250), aspectRatioMode=Qt.KeepAspectRatio))

	def _gaussian_filter(self, text_field):
		t1 = time()
		text_field = text_field.split(' ')
		width = int(text_field[0])
		sigma = int(text_field[1]) if len(text_field)>1 else 3
		self.img_out = imgfp.gaussian_filter(self.img_raw, width, sigma)
		self.time_label.setText("%.6f seconds"%(time()-t1))
		qimage_out = ImageQt(self.img_out)
		self.image_processed.setPixmap(QPixmap.fromImage(qimage_out).scaled(QSize(250, 250), aspectRatioMode=Qt.KeepAspectRatio))

class _SubWindow(QMainWindow):
	def __init__(self, make_func, window_title, parent=None):
		super().__init__(parent)

		self.make_func = make_func
		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)

		self.text_area = QPlainTextEdit()

		self.apply_button = QPushButton('Make')
		self.apply_button.clicked.connect(self.return_text_field)

		self.main_layout.addWidget(self.text_area)
		self.main_layout.addWidget(self.apply_button)

		self.setCentralWidget(self.main_widget)
		self.setWindowTitle(window_title)
		self.setGeometry(100, 100, 300, 200)

	def return_text_field(self):
		text_field_value = self.text_area.toPlainText()
		callback = partial(self.make_func, text_field=text_field_value)
		self.parent().process_callback(callback)
		self.close()


class _ErrorWindow(QMainWindow):
	def __init__(self, message, parent=None):
		super().__init__(parent)
		main_widget = QWidget()
		main_layout = QVBoxLayout(main_widget)
		label = QLabel()
		label.setText(message)
		font = QFont()
		font.setPointSize(16)
		label.setFont(font)
		main_layout.addWidget(label)

		self.setCentralWidget(main_widget)
		self.setWindowTitle('Error!')
		desktop = QDesktopWidget().availableGeometry()
		self.setGeometry(desktop.width()//2-50, desktop.height()//2-50, 100, 100)


def parse_matrix(matrix_string, parent_window=None):
	rows = matrix_string.strip().split("\n")
	matrix = []
	num_cols = None
	for row in rows:
		# Match all numbers (integers or fractions) in the row
		nums = re.findall(r"[-]?\d+[/]?\d*", row)
		# Convert each number to a fraction and then to a float
		nums = [float(Fraction(num)) for num in nums]
		# Check that the row has the same number of columns as the previous rows
		if num_cols is not None and len(nums) != num_cols:
			error_window = _ErrorWindow('Matrix is not rectangular', parent=parent_window)
			error_window.show()
			return np.array([[1]])
		num_cols = len(nums)
		matrix.append(nums)
	# Convert the list of lists to a NumPy array
	matrix = np.array(matrix)
	# Check if the matrix has even width or height
	if matrix.shape[0] % 2 == 0 or matrix.shape[1] % 2 == 0:
		rows_to_add = int(matrix.shape[0] % 2 == 0)
		cols_to_add = int(matrix.shape[1] % 2 == 0)
		matrix = np.pad(matrix, ((0, rows_to_add), (0, cols_to_add)), mode='constant')

	return matrix
