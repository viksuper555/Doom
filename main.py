import pygame as pg
import moderngl as mgl
import sys
from map import Map
from mesh import Mesh
from model import *
from camera import Camera
from light import Light
from scene import Scene

class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)) -> None:
        pg.init()
        self.WIN_SIZE = win_size

        # Init OpenGL attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # Create the OpenGL context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # Mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # Detect and use existing OpenGL context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pg.time.Clock()
        self.time = 1
        self.delta_time = 1
        # Light, camera, scene
        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.map = Map(self)
        self.scene = Scene(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.destroy()
    
    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() / 1000
        return self.time
    
    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

    def destroy(self):
        self.mesh.destroy()
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
