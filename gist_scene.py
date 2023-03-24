from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsLineItem,
	QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem)
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF
import math



class GistoScene(QGraphicsScene):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.radius = 10
		self.points = {}
		self.setBackgroundBrush(QBrush(QColor(255, 255, 255, 255)))
		self.setSceneRect(0, 0, 300, 300)

		self.points = {0.0: self.sceneRect().height(),
					   self.sceneRect().width(): 0.0}
		self.updateLine()

	def mousePressEvent(self, event):
		pos = event.scenePos()
		x, y = pos.x(), pos.y()
		radius = self.radius

		if self.sceneRect().contains(pos):
			point_x = int(math.ceil((x-radius)/(2*radius))) * (2*radius)

			if point_x in self.points:
				point_y = self.points[point_x]
				if point_y-10 <= y <= point_y+10:
					del self.points[point_x]
				else:
					self.points[point_x] = y
			else:
				self.points[point_x] = y

		self.updateLine()

	def updateLine(self):
		# Remove any existing line or points from the scene
		for item in self.items():
			if isinstance(item, (QGraphicsLineItem, QGraphicsPathItem, QGraphicsRectItem)):
				self.removeItem(item)

		# Sort the points by x coordinate
		points = sorted(self.points.items())

		# Create a path for the curve
		path = QPainterPath()
		if len(points) == 2:
			# Only two points, draw a straight line
			p1, p2 = points
			path.moveTo(p1[0], p1[1])
			path.lineTo(p2[0], p2[1])
		else:
			path.moveTo(points[0][0], points[0][1])

			# Create cubic Bézier curves between each pair of points
			for i in range(len(points) - 1):
				p1, p2 = points[i], points[i + 1]
				cp1 = QPointF((p1[0] + p2[0]) / 2, p1[1])
				cp2 = QPointF((p1[0] + p2[0]) / 2, p2[1])
				endPt = QPointF(p2[0], p2[1])
				path.cubicTo(cp1, cp2, endPt)

		# Add a rectangle item for each point in self.points
		pen = QPen(Qt.black, 2)
		brush = QBrush(QColor(255, 0, 0, 255))
		for point in points:
			x, y = point[0], point[1]
			radius = self.radius
			rect = QGraphicsRectItem(x-radius, y-radius, 2*radius, 2*radius)
			rect.setPen(pen)
			rect.setBrush(brush)
			self.addItem(rect)

		# Update the line
		line = QGraphicsPathItem(path)
		line.setPen(pen)
		self.addItem(line)

	def get_points(self):
		points = {}
		for x, y in sorted(self.points.items()):
			points[int(255*x/300)] = 255*(300-y)/300

		return points

