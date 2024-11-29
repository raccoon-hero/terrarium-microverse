from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import QColor, QBrush, QRadialGradient, QPen
from PyQt5.QtCore import Qt, QPointF, QTimer, QTime, QCoreApplication
import random

# from PyQt5.QtWidgets import (
#     QGraphicsRectItem,
#     QGraphicsPixmapItem,
#     QGraphicsDropShadowEffect,
#     QGraphicsEllipseItem,
#     QGraphicsLineItem,
#     QGraphicsTextItem,
#     QGraphicsPolygonItem,
# )
# from PyQt5.QtGui import QColor, QPen, QPixmap, QFont, QBrush, QRadialGradient, QPolygonF

class LightingModule:
    def __init__(self, scene, boundary):
        self.scene = scene
        self.boundary = boundary
        self.dynamic_lights = []
        self.current_light_opacity = 100
        self.time_of_day = 2  # 0 = Day, 1 = Transition to Night, etc.
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lighting)
        self.timer.start(100)

    def add_dynamic_lighting(self):
        """Initialize dynamic lighting effects."""
        for light, _ in self.dynamic_lights:
            self.scene.removeItem(light)
        self.dynamic_lights.clear()

        for _ in range(3):
            x, y = random.randint(60, 420), random.randint(60, 420)
            size = random.randint(100, 150)
            light = QGraphicsEllipseItem(x, y, size, size)

            gradient = QRadialGradient(x + size / 2, y + size / 2, size / 2)
            gradient.setColorAt(0, QColor(255, 255, 200, self.current_light_opacity))
            gradient.setColorAt(1, QColor(255, 255, 200, 0))

            light.setBrush(QBrush(gradient))
            light.setPen(QPen(Qt.NoPen))
            light.setZValue(-2)
            self.scene.addItem(light)
            self.dynamic_lights.append((light, gradient))

    def update_lighting(self):
        """Update lighting based on the time of day."""
        self.time_of_day = (self.time_of_day + 1) % 100

        if 0 <= self.time_of_day <= 50:
            self.current_light_opacity = int(100 + (50 - self.time_of_day) * 3)
        else:
            self.current_light_opacity = int((self.time_of_day - 50) * 3)

        # Update background color
        bg_color = QColor(
            int(240 - self.current_light_opacity * 0.5),
            int(240 - self.current_light_opacity * 0.5),
            int(240 - self.current_light_opacity * 0.5),
        )
        self.boundary.setBrush(QBrush(bg_color))

        for light, gradient in self.dynamic_lights:
            gradient.setColorAt(0, QColor(255, 255, 200, self.current_light_opacity))
