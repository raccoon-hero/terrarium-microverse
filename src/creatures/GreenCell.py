import numpy as np
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import Qt
import random
from threading import Semaphore
from fmpy import simulate_fmu
import threading

from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItemGroup
from PyQt5.QtGui import QColor, QRadialGradient
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QGraphicsRectItem

class GreenCell:
    def __init__(self, idx, scene, environment):
        self.idx = idx
        self.environment = environment
        self.hunger_level = random.randint(22, 25)
        self.direction = random.uniform(0, 2 * np.pi)
        self.speed = random.uniform(1.5, 3.0)
        self.idle_ticks = 0
        self.cooldown = 0
        self.edge_wander_ticks = 0
        self.detection_radius = 100

        self.trail_markers = []
        self.scene = scene

        self.is_at_target = False

        self.food_semaphore = Semaphore(1)

        # CELL LOOK
        # Main body of the "molecular cell"
        self.creature_item = QGraphicsEllipseItem(0, 0, 20, 20)  # Main body
        self.creature_item.setBrush(QColor(144, 238, 144, 80))  # Light, semi-transparent green
        self.creature_item.setPen(QPen(QColor(34, 139, 34), 2))  # Darker green border for "cell membrane"

        # Add shadow effect to the creature
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)  # Adjust blur for softness of shadow
        shadow.setOffset(1, 1)    # Offset to create a slight drop shadow effect
        shadow.setColor(QColor(0, 100, 0, 170))  # Semi-transparent dark green shadow
        self.creature_item.setGraphicsEffect(shadow)

        # Center nucleus effect
        nucleus = QGraphicsEllipseItem(5, 5, 10, 10, self.creature_item)
        nucleus.setBrush(QColor(107, 142, 35, 200))  # Lightly colored, opaque green center
        nucleus.setPen(QPen(QColor(34, 139, 34, 150), 1))

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(10)  # Adjust blur for softness of shadow
        shadow2.setOffset(3, 3)    # Offset to create a slight drop shadow effect
        shadow2.setColor(QColor(46, 139, 87, 150))  # Semi-transparent dark green shadow
        nucleus.setGraphicsEffect(shadow2)


        # Initialize organelles within the cell with random initial positions
        self.organelles = []
        for _ in range(3):
            x, y = random.randint(2, 15), random.randint(2, 15)
            organelle = QGraphicsEllipseItem(x, y, 5, 5, self.creature_item)
            organelle.setBrush(QColor(random.randint(40, 120), random.randint(60, 200), random.randint(70, 240), random.randint(120, 180)))
            
            shadow3 = QGraphicsDropShadowEffect()
            shadow3.setBlurRadius(25)  # Adjust blur for softness of shadow
            shadow3.setOffset(1, 1)    # Offset to create a slight drop shadow effect
            shadow3.setColor(QColor(0, 120, 130, 170))  # Semi-transparent dark shadow
            organelle.setGraphicsEffect(shadow3)
            organelle.setPen(QPen(QColor(15, 18, 180, 150), 1))
            self.organelles.append((organelle, x, y))  # Store initial positions
            
        # Target attributes (initialized randomly within boundaries)
        boundaries = environment.boundary.get_boundaries()
        self.target_x = random.uniform(boundaries[0], boundaries[2])
        self.target_y = random.uniform(boundaries[1], boundaries[3])

        # Position the creature
        self.creature_item.setPos(self.target_x, self.target_y)
        self.creature_item.setZValue(1) 
        self.scene.addItem(self.creature_item)

        # Scanner projection (cone) effect
        self.scanner_beam = QGraphicsPolygonItem()
        self.scanner_beam.setBrush(QColor(150, 200, 255, 40))  # Semi-transparent light blue
        self.scanner_beam.setPen(QPen(Qt.NoPen))  # No border for smooth look
        self.scene.addItem(self.scanner_beam)

        # Add to scene
        scene.addItem(self.creature_item)

    def update_needs(self, thoughts_manager, status_widget=None):
        self.hunger_level -= 0.1

        if self.hunger_level < 20:
            if thoughts_manager.creature_thoughts.get(self.idx) != "feels hungry":
                thoughts_manager.add_thought(self.idx, "feels hungry")
        else:
            thoughts_manager.resolve_thought(self.idx, "feels hungry")

    def handle_food_interaction(self, thoughts_manager):
        if self.hunger_level <= 20:
            food_position = self.environment.food_source.get_position()
            food_x, food_y = food_position.x() + 7.5, food_position.y() + 7.5
            x, y = self.creature_item.pos().x(), self.creature_item.pos().y()
            
            distance_to_food = np.hypot(food_x - x, food_y - y)
            
            if self.move_towards(food_x, food_y):
                if distance_to_food < 10:
                    if self.food_semaphore.acquire(blocking=False):
                        self.hunger_level = 100
                        self.idle_ticks = random.randint(20, 40)
                        thoughts_manager.add_thought(self.idx, "is eating to refuel")
                        self.food_semaphore.release()
                    else:
                        # Add idle behavior if unable to access food
                        self.idle_ticks = random.randint(10, 30)
                        thoughts_manager.add_thought(self.idx, "is waiting to eat")
                else:
                    # Adjust direction slightly to simulate searching near the food
                    self.direction += random.uniform(-np.pi / 16, np.pi / 16)
                    thoughts_manager.add_thought(self.idx, "is moving toward food")
        elif random.random() < 0.02:
            # Occasional idle behavior if not actively seeking food
            self.idle_ticks = random.randint(20, 60)


    def handle_nearby_creature_interaction(self, creatures, thoughts_manager):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        nearby_creatures = [creature for creature in creatures if creature != self and self.distance(creature) < self.detection_radius]

        if nearby_creatures:
            thoughts_manager.add_thought(self.idx, "notices other creatures nearby")

            target_creature = random.choice(nearby_creatures)
            target_x, target_y = target_creature.creature_item.pos().x(), target_creature.creature_item.pos().y()
            angle_to_target = np.arctan2(target_y - self.creature_item.pos().y(), target_x - self.creature_item.pos().x())

            if random.random() < 0.5:  # Sprinting follow behavior
                self.direction = angle_to_target
                self.speed = 4.0  # Sprinting speed for following
                thoughts_manager.add_thought(self.idx, f"is sprinting to follow Creature {target_creature.idx}")

                # Keep cooldown longer to prolong the following behavior
                self.cooldown = random.randint(80, 120)
                target_creature.cooldown = random.randint(60, 90)  # Allow target to respond sooner
                thoughts_manager.add_thought(target_creature.idx, "notices it’s being closely followed and feels tense")

                # Check distance periodically to maintain close following
                distance_to_target = self.distance(target_creature)
                if distance_to_target > 10:
                    # Adjust direction if target moves; maintain the sprint until cooldown ends
                    self.direction += (angle_to_target - self.direction) * 0.2
                else:
                    # Slow down slightly when very close to the target
                    self.speed = 2.5

            elif random.random() < 0.2:  # Explore together in a loose formation
                offset_distance = 30  # Distance to maintain between each other
                target_x += random.randint(-offset_distance, offset_distance)
                target_y += random.randint(-offset_distance, offset_distance)
                joint_angle = np.arctan2(target_y - self.creature_item.pos().y(), target_x - self.creature_item.pos().x())
                self.direction += (joint_angle - self.direction) * 0.1  # Smoothly align directions
                target_creature.direction += (joint_angle - target_creature.direction) * 0.1
                thoughts_manager.add_thought(self.idx, f"is exploring alongside Creature {target_creature.idx}")
                thoughts_manager.add_thought(target_creature.idx, f"is wandering alongside Creature {self.idx}")
                self.cooldown = random.randint(60, 80)
                target_creature.cooldown = self.cooldown

            elif random.random() < 0.2:  # Keep distance
                thoughts_manager.add_thought(self.idx, "is keeping a safe distance")
                distance_angle = angle_to_target + np.pi  # Move in the opposite direction
                self.direction += (distance_angle - self.direction) * 0.1  # Smooth transition away
                self.speed = max(self.speed - 0.1, 1.0)  # Slight deceleration while keeping distance
                self.cooldown = random.randint(40, 60)

            else:  # Casual observation with slight variation in direction
                self.direction += random.uniform(-np.pi / 16, np.pi / 16)
                self.speed = max(self.speed - 0.05, 1.5)  # Slow down slightly
                thoughts_manager.add_thought(self.idx, "is observing nearby creatures")
                self.cooldown = random.randint(20, 40)

            # Reaction to crowded surroundings
            if len(nearby_creatures) > 3:
                thoughts_manager.add_thought(self.idx, "feels surrounded and slightly uneasy")
                self.cooldown += 30
                self.speed = max(self.speed - 0.1, 1.0)  # Slow down slightly when feeling surrounded


    def leave_trail(self):
        """Leave a trail marker behind the creature, centered below it."""
        # Get the creature's current position (centered)
        x = self.creature_item.pos().x() + self.creature_item.rect().width() / 2
        y = self.creature_item.pos().y() + self.creature_item.rect().height() / 2

        # Calculate the offset for the trail position directly behind the creature based on its direction
        offset_distance = 12  # Distance behind the creature
        trail_x = x - offset_distance * np.cos(self.direction)
        trail_y = y - offset_distance * np.sin(self.direction)

        # Create a small, semi-transparent ellipse for the "trail in water" effect
        trail_marker = QGraphicsEllipseItem(trail_x - 3, trail_y - 3, 6, 6)  # Slightly larger for a fluid look
        color_variation = random.randint(180, 220)  # Light color variation for a "water diffusion" effect
        trail_marker.setBrush(QColor(150, color_variation, 255, 130))  # Light, watery blue with transparency
        trail_marker.setPen(QPen(Qt.NoPen))  # No border for a soft look

        # Set a low z-value to ensure the trail is behind other items
        trail_marker.setZValue(0)  # Lower z-value for rendering below other elements

        # Add the trail marker to the scene and initialize it with full opacity
        self.scene.addItem(trail_marker)
        self.trail_markers.append((trail_marker, 40))  # Add as (marker, opacity) for fading

    def update_trail(self):
        """Update the opacity of the trail markers, and remove them if fully faded out."""
        markers_to_remove = []  # Temporary list to track indices of markers that need removal

        if self.idle_ticks > 0:  # Creature is idling
            fade_amount = 10  # Faster fade while idle
        else:
            fade_amount = 4  # Standard fade when moving

        # Update opacity and gather markers to remove
        for i, (marker, opacity) in enumerate(self.trail_markers):
            opacity -= fade_amount
            if opacity <= 0:
                self.scene.removeItem(marker)  # Remove marker from the scene if fully faded
                markers_to_remove.append(i)  # Add index to remove from trail_markers list
            else:
                # Increase marker size slightly as it fades for a "diffusion" effect
                rect = marker.rect()
                marker.setRect(rect.x() - 0.2, rect.y() - 0.2, rect.width() + 0.4, rect.height() + 0.4)
                marker.setBrush(QColor(120, 140, 120, opacity))
                self.trail_markers[i] = (marker, opacity)  # Update the list with new opacity value

        # Remove all fully faded markers from the main trail_markers list by index
        for index in sorted(markers_to_remove, reverse=True):
            del self.trail_markers[index]


    def update_position(self, left, top, right, bottom):
        if self.idle_ticks > 0:  # Skip movement while idle (e.g., eating)
            self.idle_ticks -= 1
            return

        # Usual position update code
        x, y = self.creature_item.pos().x(), self.creature_item.pos().y()
        dx = self.speed * np.cos(self.direction)
        dy = self.speed * np.sin(self.direction)
        new_x = max(left, min(x + dx, right))
        new_y = max(top, min(y + dy, bottom))
        
        self.creature_item.setPos(new_x, new_y)

        # Leave a trail at each step
        self.leave_trail()
        self.update_trail()
        # Update scanner beam position and orientation
        self.update_scanner_beam()

    def update_scanner_beam(self):
        """Update the position and direction of the scanner beam, using beam_width for the angular spread."""
        # Center of the creature
        x, y = self.creature_item.pos().x() + 10, self.creature_item.pos().y() + 10

        # Set beam parameters
        beam_length = 100  # Length of the scanner projection
        beam_width = 50   # Width of the scanner projection (controls spread angle)

        # Calculate the spread angle based on beam_width and beam_length
        spread_angle = np.arctan(beam_width / beam_length)

        # Define the angles for the wide end of the scanner beam
        left_angle = self.direction - spread_angle
        right_angle = self.direction + spread_angle

        # Calculate points for the triangular beam shape
        left_point = QPointF(x + beam_length * np.cos(left_angle), y + beam_length * np.sin(left_angle))
        right_point = QPointF(x + beam_length * np.cos(right_angle), y + beam_length * np.sin(right_angle))

        # Set the sharp point (origin of the fan) near the creature
        sharp_point = QPointF(x, y)

        # Create the scanner beam shape as a polygon
        scanner_path = QPolygonF([sharp_point, left_point, right_point])

        # Set the polygon path for the scanner beam
        self.scanner_beam.setPolygon(scanner_path)

    def handle_edge_behavior(self, left, top, right, bottom, thoughts_manager):
        """Simulate a battering ram motion against the boundary, with alignment, retreat, and charge."""
        x, y = self.creature_item.pos().x(), self.creature_item.pos().y()
        edge_proximity = 5  # Distance to consider the creature at the edge

        # Check if creature is near the boundary
        if x <= left + edge_proximity or x >= right - edge_proximity or y <= top + edge_proximity or y >= bottom - edge_proximity:
            # Enter boundary interaction mode if not already initialized
            if not hasattr(self, "boundary_phase"):
                # Determine the perpendicular direction to the wall based on proximity
                if x <= left + edge_proximity:
                    self.direction = 0  # Facing right
                elif x >= right - edge_proximity:
                    self.direction = np.pi  # Facing left
                elif y <= top + edge_proximity:
                    self.direction = np.pi / 2  # Facing down
                elif y >= bottom - edge_proximity:
                    self.direction = 3 * np.pi / 2  # Facing up

                # Initialize interaction phases
                self.boundary_phase = "retreat_from_wall"
                self.phase_ticks = 0
                thoughts_manager.add_thought(self.idx, "aligns with the boundary to attempt a breakthrough")

            # Phased boundary interaction
            if self.boundary_phase == "retreat_from_wall":
                # Retreat 10 steps back from the wall, while keeping the direction towards it
                self.speed = 3.0  # Set a slower backward speed for visible retreat
                self.direction = (self.direction + np.pi) % (2 * np.pi)  # Turn to retreat
                thoughts_manager.add_thought(self.idx, "steps back for a running start")
                self.phase_ticks += 1

                # After a set number of ticks, prepare to charge forward
                if self.phase_ticks >= 10:
                    self.boundary_phase = "charge_toward_wall"
                    self.phase_ticks = 0
                    # Re-align direction towards the wall
                    self.direction = (self.direction + np.pi) % (2 * np.pi)  # Turn to face the wall

            elif self.boundary_phase == "charge_toward_wall":
                # Sprint toward the wall with increased speed
                self.speed = 5.0  # Sprint speed
                thoughts_manager.add_thought(self.idx, "charges forward with full force!")
                self.phase_ticks += 1

                # Once close enough to the wall, go back to retreat phase
                if self.phase_ticks >= 10:
                    self.boundary_phase = "retreat_from_wall"
                    self.phase_ticks = 0

        else:
            # Reset if the creature is no longer near the edge
            if hasattr(self, "boundary_phase"):
                del self.boundary_phase  # Clear boundary interaction mode

            # Regular wandering behavior if not near boundary
            self.direction += random.uniform(-np.pi / 16, np.pi / 16)
            self.speed = max(1.0, min(self.speed + random.uniform(-0.05, 0.05), 3.0))


    def move_towards(self, target_x, target_y):
        distance = np.hypot(self.creature_item.pos().x() - target_x, self.creature_item.pos().y() - target_y)
        if distance < 10:
            return True
        angle_to_target = np.arctan2(target_y - self.creature_item.pos().y(), target_x - self.creature_item.pos().x())
        self.direction = angle_to_target
        return False

    def distance(self, other_creature):
        return np.hypot(self.creature_item.pos().x() - other_creature.creature_item.pos().x(),
                        self.creature_item.pos().y() - other_creature.creature_item.pos().y())


    def calculate_average_position(self, creatures):
        avg_x = np.mean([c.creature_item.pos().x() for c in creatures])
        avg_y = np.mean([c.creature_item.pos().y() for c in creatures])
        return avg_x, avg_y
