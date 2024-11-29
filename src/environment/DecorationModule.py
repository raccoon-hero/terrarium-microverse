from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsDropShadowEffect, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor, QPen, QLinearGradient, QPixmap, QPolygonF
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel, QGraphicsProxyWidget
import random
import os

class DecorationModule:
    def __init__(self, scene):
        self.scene = scene
        self.decorations = []
        self.images_folder = "src/environment/images/background/main"
        self.additional_folder = "src/environment/images/background/additional"
        self.rocks_folder = "src/environment/images/background/rocks"
        self.gifs_folder = "src/environment/images/gifs"

    def add_decorations(self):
        """Add enhanced decorations to create a rich terrarium atmosphere."""
        self.add_pebbles()
        self.add_moss()
        self.add_leaves()
        self.add_water_droplets()
        self.add_branches()
        self.add_ambient_light()
        # Add general image decorations
        self.add_image_decorations(self.images_folder, 140)
        # Add additional decorations
        self.add_image_decorations(self.additional_folder, 20)
        # Add rock decorations
        self.add_image_decorations(self.rocks_folder, 20)
        # self.add_gif_decorations()

    def add_image_decorations(self, folder, count):
        """Add image-based decorations from a specified folder with random rotations."""
        if not os.path.exists(folder):
            print(f"Images folder '{folder}' not found.")
            return

        # List all image files in the folder
        image_files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            print(f"No image files found in the folder '{folder}'.")
            return

        for _ in range(count):  # Add specified number of decorations
            # Randomly select an image file
            image_file = random.choice(image_files)
            image_path = os.path.join(folder, image_file)

            # Load the image as a pixmap
            pixmap = QPixmap(image_path).scaled(35, 35, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if pixmap.isNull():
                print(f"Failed to load image: {image_path}")
                continue

            # Apply random rotation
            rotation_angle = random.randint(0, 360)
            transform = QTransform().rotate(rotation_angle)
            rotated_pixmap = pixmap.transformed(transform, mode=Qt.SmoothTransformation)

            # Create a QGraphicsPixmapItem for the image
            x, y = random.randint(60, 430), random.randint(60, 430)
            image_item = QGraphicsPixmapItem(rotated_pixmap)
            image_item.setPos(x, y)
            image_item.setZValue(random.randint(0, 3))  # Ensure it's above other decorations

            # Apply shadow effect
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(30)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor(0, 0, 0, 150))
            image_item.setGraphicsEffect(shadow)

            # Add the image to the scene and keep track of it
            self.scene.addItem(image_item)
            self.decorations.append(image_item)


    def add_gif_decorations(self):
        """Add GIF decorations to the scene."""
        if not os.path.exists(self.gifs_folder):
            print(f"GIFs folder '{self.gifs_folder}' not found.")
            return

        # List all GIF files in the folder
        gif_files = [f for f in os.listdir(self.gifs_folder) if f.endswith('.gif')]

        for _ in range(5):  # Add 5 randomly placed GIFs
            if not gif_files:
                print("No GIF files found in the folder.")
                return

            # Randomly select a GIF file
            gif_file = random.choice(gif_files)
            gif_path = os.path.join(self.gifs_folder, gif_file)

            # Create a QLabel to hold the GIF
            label = QLabel()
            label.setAttribute(Qt.WA_TranslucentBackground)  # Make background transparent
            label.setFixedSize(35, 35)
            label.setScaledContents(True)

            # Load and start the GIF
            movie = QMovie(gif_path)

            label.setMovie(movie)
            movie.start()

            # Wrap the QLabel in a QGraphicsProxyWidget to place it on the scene
            x, y = random.randint(60, 430), random.randint(60, 430)
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(label)
            proxy.setPos(x, y)

            # Random rotation
            rotation_angle = random.randint(0, 360)
            proxy.setRotation(rotation_angle)

            proxy.setZValue(3)  # Ensure it's above other decorations

            # Add the proxy to the scene and track it
            self.scene.addItem(proxy)
            self.decorations.append(proxy)

    def add_pebbles(self):
        """Add realistic pebbles with gradient shading."""
        for _ in range(12):  # Slightly more pebbles
            x, y = random.randint(60, 430), random.randint(60, 430)
            size = random.randint(8, 14)
            pebble = QGraphicsEllipseItem(x, y, size, size)
            gradient = QLinearGradient(0, 0, size, size)
            gradient.setColorAt(0, QColor(160, 160, 160))
            gradient.setColorAt(1, QColor(100, 100, 100))
            pebble.setBrush(QBrush(gradient))
            pebble.setPen(QPen(Qt.NoPen))
            self.scene.addItem(pebble)
            self.decorations.append(pebble)

    def add_moss(self):
        """Add textured moss patches."""
        for _ in range(8):  # More moss for a lush effect
            x, y = random.randint(60, 430), random.randint(60, 430)
            size_x, size_y = random.randint(15, 25), random.randint(10, 20)
            moss = QGraphicsEllipseItem(x, y, size_x, size_y)
            gradient = QLinearGradient(0, 0, size_x, size_y)
            gradient.setColorAt(0, QColor(46, 139, 87))
            gradient.setColorAt(1, QColor(34, 139, 34))
            moss.setBrush(QBrush(gradient))
            moss.setPen(QPen(Qt.NoPen))
            self.scene.addItem(moss)
            self.decorations.append(moss)

    def add_leaves(self):
        """Add varied and layered leaves."""
        for _ in range(10):  # Increase leaf count
            x, y = random.randint(60, 430), random.randint(60, 430)
            leaf_type = random.choice(["broad", "pointed"])
            if leaf_type == "broad":
                # Broad leaf
                leaf_points = [
                    QPointF(x, y),
                    QPointF(x + random.randint(15, 25), y + random.randint(10, 20)),
                    QPointF(x + random.randint(30, 40), y + random.randint(-10, 10)),
                ]
            else:
                # Pointed leaf
                leaf_points = [
                    QPointF(x, y),
                    QPointF(x + random.randint(10, 20), y + random.randint(-5, 5)),
                    QPointF(x + random.randint(25, 30), y),
                ]
            leaf = QGraphicsPolygonItem(QPolygonF(leaf_points))
            gradient = QLinearGradient(0, 0, 30, 30)
            gradient.setColorAt(0, QColor(60, 180, 60))
            gradient.setColorAt(1, QColor(30, 120, 30))
            leaf.setBrush(QBrush(gradient))
            leaf.setPen(QPen(Qt.NoPen))
            self.scene.addItem(leaf)
            self.decorations.append(leaf)

    def add_water_droplets(self):
        """Add sparkling water droplets with gradient transparency."""
        for _ in range(10):
            x, y = random.randint(60, 430), random.randint(60, 430)
            size = random.randint(5, 9)
            droplet = QGraphicsEllipseItem(x, y, size, size)
            gradient = QLinearGradient(0, 0, size, size)
            gradient.setColorAt(0, QColor(173, 216, 230, 180))
            gradient.setColorAt(1, QColor(135, 206, 235, 100))
            droplet.setBrush(QBrush(gradient))
            droplet.setPen(QPen(Qt.NoPen))
            self.scene.addItem(droplet)
            self.decorations.append(droplet)

    def add_branches(self):
        """Add realistic small branches with enhanced visual complexity and proper alignment."""
        for _ in range(8):  # Increase number for more diversity
            # Anchor point for the branch
            anchor_x = random.randint(60, 430)
            anchor_y = random.randint(60, 430)

            # Main branch dimensions
            length = random.randint(30, 60)  # Branch length
            thickness = random.randint(3, 7)  # Branch thickness
            
            # Main branch
            branch = QGraphicsRectItem(0, 0, length, thickness)  # Start at (0, 0)
            gradient = QLinearGradient(0, 0, length, 0)  # Gradient for texture
            gradient.setColorAt(0, QColor(101, 67, 33))  # Dark brown at one end
            gradient.setColorAt(1, QColor(139, 69, 19))  # Lighter brown at the other end
            branch.setBrush(QBrush(gradient))
            branch.setPen(QPen(Qt.NoPen))
            branch.setRotation(random.randint(-45, 45))  # Random angle
            branch.setPos(anchor_x, anchor_y)  # Position relative to the anchor
            branch.setZValue(1)  # Ensure visibility
            self.scene.addItem(branch)
            self.decorations.append(branch)

            # Add smaller twigs, positioned relative to the main branch
            for _ in range(random.randint(2, 4)):
                twig_length = random.randint(10, 20)
                twig_thickness = random.randint(1, 2)

                # Random offset along the main branch
                offset_x = random.uniform(0, length)
                offset_y = random.uniform(-thickness / 2, thickness / 2)

                twig = QGraphicsRectItem(offset_x, offset_y, twig_length, twig_thickness)
                twig.setBrush(QColor(101, 67, 33))  # Match branch color
                twig.setPen(QPen(Qt.NoPen))
                twig.setRotation(random.randint(-30, 30))  # Random twig angle
                twig.setPos(anchor_x, anchor_y)  # Position relative to the anchor
                twig.setZValue(2)  # Slightly above the main branch
                self.scene.addItem(twig)
                self.decorations.append(twig)

            # Add shadow beneath the branch
            shadow = QGraphicsEllipseItem(-length / 2, -thickness / 2, length, thickness)
            shadow.setBrush(QColor(0, 0, 0, 50))  # Transparent black
            shadow.setPen(QPen(Qt.NoPen))
            shadow.setPos(anchor_x, anchor_y)  # Align with the main branch
            shadow.setZValue(0)  # Shadow below the branch
            self.scene.addItem(shadow)
            self.decorations.append(shadow)


    def add_ambient_light(self):
        """Simulate ambient lighting for atmosphere."""
        ambient_light = QGraphicsEllipseItem(0, 0, 500, 500)
        ambient_light.setBrush(QColor(205, 205, 250, 50))  # Warm light
        ambient_light.setPen(QPen(Qt.NoPen))
        ambient_light.setZValue(-1)  # Ensure it is below other elements
        self.scene.addItem(ambient_light)
        self.decorations.append(ambient_light)
