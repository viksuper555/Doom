from map import Map
from model import Cube, Monkey, SkyBox


class Scene:
    def __init__(self, app) -> None:
        self.app = app
        self.objects = []
        self.load()
        self.skybox = SkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        tiles = app.map.get_floor(app)
        for tile in tiles:
            add(tile)        
        
        add(Monkey(app, pos=(20, -2, -25)))
        walls = app.map.get_walls(app)
        for wall in walls:
            add(wall)

    def render(self):
        for obj in self.objects:
            obj.render()
        self.skybox.render()