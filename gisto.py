from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
	QVBoxLayout, QGraphicsView, QStackedWidget, QGraphicsScene)
from PIL import Image
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class GistoWidget(QWidget):
	def __init__(self, parent=None, image_path=None):
		super().__init__(parent)

		self.image_path = image_path
		self.plot_widget = QWidget()
		self.layout = QVBoxLayout(self.plot_widget)
		self.setLayout(self.layout)

	def gistogram(self):
		if self.image_path:
			img = Image.open(self.image_path)
			img_arr = np.asarray(img)
			return img_arr.flatten()

	def showGistogram(self):
		count = self.gistogram()
		if count.any():
			fig, ax = plt.subplots()
			ax.hist(count, bins=256, range=(0, 256), color='gray')
			ax.set_xticklabels([])
			ax.set_yticklabels([])

			canvas = FigureCanvas(fig)
			canvas.setParent(self.plot_widget)

			self.layout.addWidget(canvas)



class GistoWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)

		self.graphics_view = QGraphicsView()
		self.scene = QGraphicsScene()
		self.scene.setBackgroundBrush(QBrush(QColor(255, 255, 255, 255)))
		self.graphics_view.setScene(self.scene)
		self.scene.addLine(0, 0, 100, 100, Qt.black)
		self.graphics_view.setStyleSheet("background-color: rgba(0,0,0,0);")

		scene_rect = self.scene.sceneRect()
		scene_x = scene_rect.x()
		scene_y = scene_rect.y()
		scene_width = scene_rect.width()
		scene_height = scene_rect.height()

		pen = QPen(Qt.SolidLine)
		pen.setWidth(2)
		pen.setColor(Qt.black)

		# Add the line to the scene
		self.scene.addLine(0, scene_height, scene_width, 0, pen)

		# Set the main widget and layout
		self.setCentralWidget(self.main_widget)

		self.main_layout.addWidget(self.graphics_view)

		# Set the window properties
		self.setWindowTitle("Gistogram Window")
		self.setGeometry(300, 300, 400, 400)
