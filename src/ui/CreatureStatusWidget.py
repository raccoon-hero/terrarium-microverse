from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QColor, QPixmap

class CreatureStatusWidget(QWidget):
    def __init__(self, name, color):
        super().__init__()
        
        self.name = name
        self.color = color
        self.current_thought = ""

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Indicator
        self.creature_visual = QLabel()
        pixmap = QPixmap(20,20)
        pixmap.fill(QColor(color))
        self.creature_visual.setPixmap(pixmap)
        
        # Creature name label
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet(f"font-weight: bold; color: {color};")
        
        # Hunger progress bar
        self.hunger_bar = QProgressBar()
        self.hunger_bar.setMaximum(100)
        self.hunger_bar.setValue(30)
        
        # Thought label for displaying the current thought
        self.thought_label = QLabel("Thought: None")

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.creature_visual)
        top_layout.addWidget(self.name_label)
        layout.addLayout(top_layout)
        layout.addWidget(self.thought_label)
        layout.addWidget(QLabel("Hunger"))
        layout.addWidget(self.hunger_bar)

        

    def update_status(self, hunger, thought=""):
        """Update the creature's hunge, and thought."""
        self.hunger_bar.setValue(hunger)
        
        if thought and thought != self.current_thought:
            self.current_thought = thought
            self.thought_label.setText(f"Thought: {thought}")