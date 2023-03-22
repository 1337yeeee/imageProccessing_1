from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
	QVBoxLayout, QGraphicsView, QStackedWidget, QGraphicsScene)
from PIL import Image
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

			img = img.convert('L')

			count = [0] * 256

			for x in range(img.width):
				for y in range(img.height):
					pixel_value = img.getpixel((x, y))
					count[pixel_value] += 1

			return count

	def showGistogram(self):
		count = self.gistogram()
		if count:
			print("hello")
		
			fig, ax = plt.subplots()
			ax.hist(count, density=True, bins=range(256))

			canvas = FigureCanvas(fig)
			canvas.setParent(self.plot_widget)

			self.layout.addWidget(canvas)



class GistoWindow(QMainWindow):
	def __init__(self, parent=None, image_path=None):
		super().__init__(parent)

		self.image_path = image_path

		self.main_widget = QWidget()
		self.main_layout = QVBoxLayout(self.main_widget)

		# self.showGistogram()

		self.plot_widget = None

		self.stacked_widget = QStackedWidget()
		self.stacked_widget.setGeometry(0, 0, 400, 300)

		self.graphics_view = QGraphicsView()
		self.scene = QGraphicsScene()
		self.scene.setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
		self.graphics_view.setScene(self.scene)
		self.scene.addRect(0, 0, 100, 100, Qt.black)
		self.scene.addEllipse(50, 50, 100, 100, Qt.red)
		self.graphics_view.setStyleSheet("background-color: rgba(0,0,0,0);")
		# self.stacked_widget.addWidget(self.graphics_view)

		# Raise the graphics view to the front
		self.stacked_widget.setCurrentWidget(self.graphics_view)

		# Set the main widget and layout
		self.setCentralWidget(self.main_widget)

		self.main_layout.addWidget(self.stacked_widget)

		# Set the window properties
		self.setWindowTitle("Gistogram Window")
		self.setGeometry(300, 300, 400, 300)

	def gistogram(self):
		if self.image_path:
			img = Image.open(self.image_path)

			img = img.convert('L')

			count = [0] * 256

			for x in range(img.width):
				for y in range(img.height):
					pixel_value = img.getpixel((x, y))
					count[pixel_value] += 1

			return count

	def showGistogram(self):
		count = self.gistogram()
		if count:
			print(self.stacked_widget.count())
			# Create a new plot widget and add it to the stacked widget
			plot_widget = QWidget(self)
			# self.setCentralWidget(plot_widget)

			fig, ax = plt.subplots()
			ax.hist(count, density=True, bins=range(256))

			canvas = FigureCanvas(fig)
			canvas.setParent(plot_widget)

			self.stacked_widget.addWidget(canvas)
			
			# Remove the previous widget and set the new one as the current widget
			if self.plot_widget:
				self.stacked_widget.removeWidget(self.plot_widget)
				self.plot_widget.deleteLater()
			self.plot_widget = plot_widget

