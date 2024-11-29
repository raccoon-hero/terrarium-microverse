from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtCore import Qt


class FoodModule:
    def __init__(self, scene, boundary):
        """
        Initialize the food source module.
        :param scene: The QGraphicsScene instance where the food source will be added.
        :param boundary: The boundary box within which the food source will be positioned.
        """
        self.scene = scene
        self.boundary = boundary
        self.food_source = None

    def initialize_food_source(self, food_image_path="src/environment/images/plant03.png"):
        """
        Initialize the food source with the given image path.
        :param food_image_path: Path to the PNG image used for the food source.
        """
        # Load and scale the food source image
        food_pixmap = QPixmap(food_image_path).scaled(
            35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.food_source = QGraphicsPixmapItem(food_pixmap)

        # Center the food source within the boundary box
        food_x = self.boundary.rect().center().x() - food_pixmap.width() / 2
        food_y = self.boundary.rect().center().y() - food_pixmap.height() / 2
        self.food_source.setPos(food_x, food_y)

        # Add a shadow effect to the food source
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.food_source.setGraphicsEffect(shadow)

        # Add the food source to the scene
        self.scene.addItem(self.food_source)

    def move_food_source(self, x, y):
        """
        Move the food source to a new position within the boundary box.
        :param x: The new x-coordinate.
        :param y: The new y-coordinate.
        """
        if self.boundary.contains(x, y):
            self.food_source.setPos(x, y)
        else:
            print("Food source position is outside the boundary!")

    def highlight_food_source(self):
        """
        Apply a glowing effect to the food source (e.g., when creatures interact with it).
        """
        highlight_brush = QBrush(QColor(0, 255, 0, 100))
        self.food_source.setBrush(highlight_brush)

    def reset_food_source_highlight(self):
        """
        Remove the highlight effect from the food source.
        """
        self.food_source.setBrush(QBrush(Qt.NoBrush))

    def get_position(self):
        """
        Return the position of the food source as a QPointF.
        """
        return self.food_source.pos()
