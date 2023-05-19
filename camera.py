import math
import glm
import pygame as pg
from map import WALL_IDs

from settings import FAR, FOV, MOUSE_SENSITIVITY, NEAR, PLAYER_POS, PLAYER_SIZE_SCALE, PLAYER_SPEED



class Camera:
    def __init__(self, app, position=(20, 1, -6), yaw=-90, pitch=0) -> None:
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)

        self.x, self.y = PLAYER_POS
        self.angle = 0

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()
    
    def rotate(self):
        rel_x, _ = pg.mouse.get_rel()
        self.yaw += rel_x * MOUSE_SENSITIVITY

    def update_camera_vectors(self):
        yaw= glm.radians(self.yaw)

        self.forward.x = glm.cos(yaw)
        self.forward.z = glm.sin(yaw)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        # self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = PLAYER_SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        vector = glm.vec3(0, 0, 0)
        if keys[pg.K_w]:
            vector = self.forward
        if keys[pg.K_a]:
            vector = -self.right
        if keys[pg.K_s]:
            vector = -self.forward
        if keys[pg.K_d]:
            vector = self.right
        if vector != glm.vec3(0, 0, 0):
            move = glm.floor((self.position + vector * velocity) / 6)
            if self.check_wall(-move[2], move[0]):
                self.position += vector * velocity


    def check_wall(self, x, y):
        return (x, y) not in self.app.map.world_map
    
    def can_move(self, dpos):
        velocity = PLAYER_SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.try_move(self.forward * velocity)
            # self.position += self.forward * velocity
        if keys[pg.K_a]:
            self.try_move(-self.right * velocity)
            # self.position -= self.right * velocity
        if keys[pg.K_s]:
            self.try_move(-self.forward * velocity)
            # self.position -= self.forward * velocity
        if keys[pg.K_d]:
            self.try_move(self.right * velocity)
            # self.position += self.right * velocity
    
    def try_move(self, vec: glm.vec3):
        scale = PLAYER_SIZE_SCALE / self.app.delta_time
        move = (self.position + vec * scale) / 6
        if move.x < 0 or -move.z < 0 or move.x >= len(self.app.map.mini_map[0]) or move.z >= len(self.app.map.mini_map):
            return  
        if not self.is_wall(int(move.x), int(-move.z)):
            self.position += vec
            print("Can move")
    
    def is_wall(self, x, y):
        return self.app.map.mini_map[x][y] in WALL_IDs

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

