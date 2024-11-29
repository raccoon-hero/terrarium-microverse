from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtCore import Qt

class BoundaryModule:
    def __init__(self, scene):
        self.scene = scene
        self.boundary_box = None

    def initialize_boundary(self):
        """Create the main terrarium boundary with thematic enhancements."""
        self.boundary_box = QGraphicsRectItem(50, 50, 400, 400)
        self.boundary_box.setPen(QPen(QColor(50, 50, 50), 4))
        self.boundary_box.setBrush(QBrush(QColor(240, 240, 240)))
        self.scene.addItem(self.boundary_box)

        corner_radius = 15
        for dx, dy in [
            (0, 0),
            (400 - corner_radius * 2, 0),
            (0, 400 - corner_radius * 2),
            (400 - corner_radius * 2, 400 - corner_radius * 2),
        ]:
            corner_circle = QGraphicsEllipseItem(dx + 50, dy + 50, corner_radius * 2, corner_radius * 2)
            corner_circle.setBrush(QColor(100, 100, 100, 180))
            corner_circle.setPen(QPen(Qt.NoPen))
            self.scene.addItem(corner_circle)

        for i in range(75, 425, 50):
            line_h = QGraphicsLineItem(50, i, 450, i)
            line_h.setPen(QPen(QColor(200, 200, 200, 120), 1, Qt.DashLine))
            line_v = QGraphicsLineItem(i, 50, i, 450)
            line_v.setPen(QPen(QColor(200, 200, 200, 120), 1, Qt.DashLine))
            self.scene.addItem(line_h)
            self.scene.addItem(line_v)

    def get_boundaries(self):
        """Return the usable boundaries of the terrarium."""
        return (
            self.boundary_box.rect().left(),
            self.boundary_box.rect().top(),
            self.boundary_box.rect().right() - 20,
            self.boundary_box.rect().bottom() - 20,
        )
