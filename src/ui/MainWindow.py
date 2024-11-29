from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsView, QGraphicsScene, QTextEdit
from PyQt5.QtCore import QTimer
from src.simulation.simulation_manager import SimulationManager
from src.simulation.thoughts_manager import ThoughtsManager
from src.ui.CreatureStatusWidget import CreatureStatusWidget

from PyQt5.QtWidgets import QHBoxLayout, QFrame
from PyQt5.QtCore import QTimer, QTime
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Terrarium Simulation")

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Graphics view setup
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(800, 600)
        main_layout.addWidget(self.view)

        # Control panel setup (start/stop buttons and status bar)
        control_panel = QVBoxLayout()
        # Start button with updated visuals
        self.start_button = QPushButton("Start Simulation")
        self.start_button.setStyleSheet(
            """
            QPushButton {
                background-color: #6C63FF;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                border: 2px solid #4B49FF;
                box-shadow: 0px 5px 15px rgba(108, 99, 255, 0.4);
            }
            QPushButton:hover {
                background-color: #4B49FF;
                box-shadow: 0px 8px 20px rgba(75, 73, 255, 0.6);
            }
            QPushButton:pressed {
                background-color: #403CCF;
                box-shadow: none;
            }
            """
        )

        # Stop button with updated visuals
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff9999ff;
                color: black;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 8px;
                box-shadow: 0px 5px 15px rgba(255, 99, 99, 0.4);
            }
            QPushButton:hover {
                background-color: #FF4B4B;
                box-shadow: 0px 8px 20px rgba(255, 75, 75, 0.6);
            }
            QPushButton:pressed {
                background-color: #D43D3D;
                box-shadow: none;
            }
            """
        )


        # Status label with updated visuals
        self.status_label = QLabel("Status: Waiting to start...")
        self.status_label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #555;
            }
            """
        )

        control_panel.addWidget(self.start_button)
        control_panel.addWidget(self.stop_button)
        control_panel.addWidget(self.status_label)

        main_layout.addLayout(control_panel)

        # Thoughts display panel
        self.thoughts_display = QTextEdit()
        self.thoughts_display.setReadOnly(True)
        self.thoughts_display.setFixedWidth(200)
        self.thoughts_display.setStyleSheet(
            """
            QTextEdit {
                background-color: #f1f1f1;
                font-size: 14px;
                border: 1px solid #ccc;
                padding: 5px;
                color: #333;
            }
            """
        )
        main_layout.addWidget(self.thoughts_display)

        # Initialize the ThoughtsManager with the thoughts_display
        self.thoughts_manager = ThoughtsManager(self.thoughts_display)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button.clicked.connect(self.stop_simulation)

        # Timer for updating visuals and status
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visuals)

        # Simulation manager
        self.simulation_manager = SimulationManager(
            self.scene,
            [],  # Status widgets not required
            self.thoughts_manager
        )

    def start_simulation(self):
        self.simulation_manager.start_simulation()
        self.timer.start(100)  # Update visuals every 100 ms
        self.status_label.setText("Status: Simulation running...")

    def stop_simulation(self):
        self.simulation_manager.stop_simulation()
        self.timer.stop()
        self.status_label.setText("Status: Simulation stopped.")

    def update_visuals(self):
        self.simulation_manager.update_scene()
