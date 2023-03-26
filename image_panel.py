from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
	QComboBox, QScrollArea, QFrame, QPushButton, QSlider, QFrame, QLineEdit)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from mask_menu import MaskMenu


class ImageWidget(QWidget):
	def __init__(self, image_path, parent=None):
		super().__init__(parent)
		self.image_path = image_path
		self.channel = "RGB"

		# Creating Pixmap label for the image
		self.label = QLabel(self)
		self.label.setPixmap(QPixmap(image_path).scaled(QSize(250, 250), aspectRatioMode=Qt.KeepAspectRatio))

		# Creating ComboBox with options (the thing where you can select an option)
		self.comboBox = QComboBox(self)
		self.comboBox.addItems(["None", "Square mask image", "Circle mask image"])

		# Creating 'delete' button
		self.delete_button = QPushButton("Delete", self)
		self.delete_button.clicked.connect(self.delete)

		# Creating horizontal layout
		# and adding to it comboBox and delete_button
		h_layout = QHBoxLayout()
		h_layout.addWidget(self.comboBox)
		h_layout.addWidget(self.delete_button)

		# Create slider
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMinimum(0)
		self.slider.setMaximum(6)
		self.slider.setValue(0)

		# Create slider layout and connect it to the main layout
		self.slider_layout = QHBoxLayout()
		self.channel_label = QLabel()
		self.channel_label.setText(self.channel)
		self.slider_layout.addWidget(self.slider)
		self.slider_layout.addWidget(self.channel_label)

		# Create a frame widget and set its properties as a divider
		frame = QFrame()
		frame.setFrameShape(QFrame.HLine)
		frame.setFrameShadow(QFrame.Sunken)

		# Connect the slider to the update_mask function
		self.slider.valueChanged.connect(self.update_channel)

		# Creating the main layout and adding to it what needed
		# Then setting layout
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.label)
		self.layout.addLayout(h_layout)
		self.layout.addLayout(self.slider_layout)
		self.layout.addWidget(frame)
		self.setLayout(self.layout)

	def update_channel(self):
		# Update the chanel based on the slider value
		channels = ["RGB", "R", "G", "B", "RG", "GB", "RB"]
		self.channel = channels[self.slider.value()]
		self.channel_label.setText(self.channel)

	def set_combo_box_items(self, is_first=False):
		self.comboBox.clear()
		if is_first:
			self.comboBox.addItems(["None", "Square mask image", "Circle mask image"])
		else:
			self.comboBox.addItems(["Add", "Multiply", "Max", "Min", "Average"])

	def delete(self):
		# Get the parent widget
		parent_widget = self.parentWidget()

		# Get the layout of the parent widget
		layout = parent_widget.layout()

		# Remove the image widget from the layout
		layout.removeWidget(self)

		# Destroy the image widget
		self.deleteLater()

		index = layout.indexOf(self)
		next_widget_item = layout.itemAt(index+1)
		if next_widget_item:
			next_image_widget = next_widget_item.widget()
			if isinstance(next_image_widget, ImageWidget):
				next_image_widget.set_combo_box_items(True)

	def __str__(self):
		return self.image_path

	def __repr__(self):
		return f'<ImageWidget:{id(self)}> image_path = {self.image_path}'


class ImagePanel(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		# Create mask_layout
		self.mask_layout = QHBoxLayout()
		self.mask_label = QLabel()
		self.mask_label.setText("Mask transparency")
		self.mask_label.setContentsMargins(5,0,5,0)
		self.mask_field = QLineEdit()
		self.mask_field.setInputMask(".99")
		self.mask_field.setText(".50")
		self.mask_field.setFixedWidth(50)
		self.mask_layout.addStretch(1)
		self.mask_layout.addWidget(self.mask_label)
		self.mask_layout.addSpacing(5) 
		self.mask_layout.addWidget(self.mask_field)
		self.mask_layout.addStretch(1)

		# Create a QScrollArea and set its properties
		self.scroll_area = QScrollArea(self)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.scroll_area.setFrameStyle(QFrame.NoFrame)

		# Set the fixed height for the scroll area widget
		self.scroll_area.setFixedHeight(800-100)

		# Create a widget to hold the images
		self.image_widget = QWidget(self.scroll_area)
		self.image_layout = QVBoxLayout()
		self.image_widget.setLayout(self.image_layout)

		# Set the widget as the scroll area's main widget
		self.scroll_area.setWidget(self.image_widget)

		# Add the scroll area to the main layout
		self.layout = QVBoxLayout()
		self.layout.addLayout(self.mask_layout)
		self.layout.addWidget(self.scroll_area)
		self.setLayout(self.layout)

	def add_image(self, image_path):
		image_widget = ImageWidget(image_path)
		if self.image_layout.count():
			self.image_layout.itemAt(0).widget().set_combo_box_items(False)
		self.image_layout.insertWidget(0, image_widget)

	def get_image_widgets(self):
		# get all the image widgets added to the image layout
		image_widgets = []
		for i in range(self.image_layout.count()):
			widget_item = self.image_layout.itemAt(i)
			image_widget = widget_item.widget()
			if isinstance(image_widget, ImageWidget):
				image_widgets.append(image_widget)
		return image_widgets

	def get_mask_transparency(self):
		mask_field_val = self.mask_field.text()
		if mask_field_val == ".":
			mask_field_val = 0
		return float(mask_field_val)
