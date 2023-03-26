from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
	QCheckBox, QLineEdit)



class MaskMenu(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.layout = QHBoxLayout()

		self.square_label = QLabel()
		self.square_label.setText("Square")
		self.square_checkbox = QCheckBox()
		self.square_field = QLineEdit()
		self.square_field.setInputMask(".99")
		self.square_field.setText(".50")
		self.square_field.setContentsMargins(5,0,5,0)

		self.circle_label = QLabel()
		self.circle_label.setText("Circle")
		self.circle_checkbox = QCheckBox()
		self.circle_field = QLineEdit()
		self.circle_field.setInputMask(".99")
		self.circle_field.setText(".50")
		self.circle_field.setContentsMargins(5,0,5,0)

		self.layout.addWidget(self.square_label)
		self.layout.addWidget(self.square_checkbox)
		self.layout.addWidget(self.square_field)
		self.layout.addWidget(self.circle_label)
		self.layout.addWidget(self.circle_checkbox)
		self.layout.addWidget(self.circle_field)
		self.setLayout(self.layout)

	def get_mask_settings(self):
		isSquare = self.square_checkbox.isChecked()
		valSquare = float(self.square_field.text())
		isCircle = self.circle_checkbox.isChecked()
		valCircle = float(self.square_field.text())

		mask_settings = {
			"S": valSquare if isSquare else None,
			"C": valCircle if isCircle else None,
		}

		return mask_settings


