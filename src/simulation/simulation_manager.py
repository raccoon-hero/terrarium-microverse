import numpy as np
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import Qt
import random
from threading import Semaphore
from fmpy import simulate_fmu, instantiate_fmu, read_model_description, extract
from fmpy.fmi2 import FMU2Slave
import threading

from src.creatures.BlueCell import BlueCell
from src.creatures.GreenCell import GreenCell
from src.environment.Environment import Environment
from src.simulation.thoughts_manager import ThoughtsManager

class SimulationManager:
    def __init__(self, scene, status_widgets, thoughts_manager):
        self.scene = scene
        self.status_widgets = status_widgets
        self.thoughts_manager = thoughts_manager
        self.environment = Environment(scene)
        self.creatures = []
        self.running = False
        self.fmu_instances = []
        self.variable_maps = []
        self.tick = 0

        self.model_descriptions = []

    def start_simulation(self):
        self.stop_simulation()
        self.running = True
        self.environment.initialize()

        self.creatures.clear()
        self.fmu_instances.clear()
        self.variable_maps.clear()

        # FMU configuration
        fmu_files = [
            {'file': 'fmus/BlueCell/BlueCell.fmu', 'class': BlueCell, 'type': 'BlueCell'},
            {'file': 'fmus/GreenCell/GreenCell.fmu', 'class': GreenCell, 'type': 'GreenCell'},
            {'file': 'fmus/GreenCell/GreenCell.fmu', 'class': GreenCell, 'type': 'GreenCell'},
            {'file': 'fmus/GreenCell/GreenCell.fmu', 'class': GreenCell, 'type': 'GreenCell'},
            {'file': 'fmus/GreenCell/GreenCell.fmu', 'class': GreenCell, 'type': 'GreenCell'},
        ]

        for idx, fmu_config in enumerate(fmu_files):
            fmu_file = fmu_config['file']
            creature_class = fmu_config['class']
            fmu_type = fmu_config['type']

            unzip_dir = extract(fmu_file)

            model_description = read_model_description(fmu_file)
            self.model_descriptions.append(model_description)

            variable_map = {var.name: var.valueReference for var in model_description.modelVariables}

            fmu = FMU2Slave(
                guid=model_description.guid,
                unzipDirectory=unzip_dir,
                modelIdentifier=model_description.modelExchange.modelIdentifier
            )
            fmu.instantiate()
            fmu.setupExperiment()
            fmu.enterInitializationMode()

            creature = creature_class(idx, self.scene, self.environment)
            left, top, right, bottom = self.environment.boundary.get_boundaries()

            if fmu_type == 'BlueCell':
                initial_x = random.uniform(left + 10, right - 10)
                initial_y = random.uniform(top + 10, bottom - 10)
                boundaries = self.environment.boundary.get_boundaries()
                fmu.setReal(
                    [
                        variable_map['initialPositionX'],
                        variable_map['initialPositionY'],
                    ],
                    [random.uniform(boundaries[0], boundaries[2]), random.uniform(boundaries[1], boundaries[3])]
                )
            elif fmu_type == 'GreenCell':
                fmu.setReal(
                    [variable_map['initialPosition']],
                    [random.uniform(60, 430)] 
                )

            fmu.exitInitializationMode()
            self.fmu_instances.append(fmu)
            self.variable_maps.append(variable_map)

            
            self.creatures.append(creature)

    def update_scene(self):
        if not self.running:
            return

        left, top, right, bottom = self.environment.boundary.get_boundaries()

        for idx, creature in enumerate(self.creatures):
            fmu = self.fmu_instances[idx]
            variable_map = self.variable_maps[idx]

            # FMU-specific updates
            if isinstance(creature, BlueCell):
                # FMU input values for BlueCell
                fmu.setReal(
                    [
                        variable_map['targetX'],
                        variable_map['targetY'],
                        variable_map['direction'],
                        variable_map['speed'],
                    ],
                    [creature.target_x, creature.target_y, creature.direction, creature.speed]
                )


                # Step the FMU
                fmu.doStep(currentCommunicationPoint=self.tick, communicationStepSize=0.1)

                # Get outputs from the FMU
                position_x = fmu.getReal([variable_map['positionX']])[0]
                position_y = fmu.getReal([variable_map['positionY']])[0]
                distance_to_target = np.hypot(creature.target_x - position_x, creature.target_y - position_y)
                is_at_target = distance_to_target < 10

                # Update creature position and state
                creature.update_from_fmu(position_x, position_y, distance_to_target, is_at_target)

            elif isinstance(creature, GreenCell):
                # Step the FMU
                fmu.doStep(currentCommunicationPoint=self.tick, communicationStepSize=0.1)

                # Get outputs from the FMU
                creature.update_position(left, top, right, bottom)

            # Continue with usual updates
            creature.leave_trail()
            creature.update_trail()
            creature.update_needs(self.thoughts_manager)
            creature.handle_food_interaction(self.thoughts_manager)
            creature.handle_nearby_creature_interaction(self.creatures, self.thoughts_manager)
            creature.handle_edge_behavior(left, top, right, bottom, self.thoughts_manager)

        self.tick += 1

    def stop_simulation(self):
        self.running = False
        for fmu in self.fmu_instances:
            fmu.terminate()
            fmu.freeInstance()
        self.fmu_instances.clear()
        self.tick = 0
        print("Simulation stopped successfully.")
