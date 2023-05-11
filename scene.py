from map import Map
from model import Cat, Cube, Wall


class Scene:
    def __init__(self, app) -> None:
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        n, s = 80, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -3, z)))
        
        add(Cat(app, pos=(0, -2, -10)))
        walls = app.map.get_walls(app)
        for wall in walls:
            add(wall)
        
    def render(self):
        for obj in self.objects:
            obj.render()