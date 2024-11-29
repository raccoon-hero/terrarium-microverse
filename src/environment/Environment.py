from src.environment.BoundaryModule import BoundaryModule
from src.environment.LightingModule import LightingModule
from src.environment.DecorationModule import DecorationModule
from src.environment.FoodModule import FoodModule 

class Environment:
    def __init__(self, scene):
        self.scene = scene
        self.boundary = BoundaryModule(scene)
        self.decorations = DecorationModule(scene)
        
        self.lighting = None
        self.food_source = None

    def initialize(self):
        self.boundary.initialize_boundary()
        self.decorations.add_decorations()

        # self.lighting = LightingModule(self.scene, self.boundary.boundary_box)
        # self.lighting.add_dynamic_lighting()

        self.food_source = FoodModule(self.scene, self.boundary.boundary_box)
        self.food_source.initialize_food_source()
