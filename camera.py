import math
import glm
import pygame as pg

from settings import FAR, FOV, MOUSE_SENSITIVITY, NEAR, PLAYER_POS, PLAYER_SIZE_SCALE, PLAYER_SPEED



class Camera:
    def __init__(self, app, position=(0, 1, 4), yaw=-90, pitch=0) -> None:
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
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity

        # if keys[pg.K_SPACE]:
        #     self.position += self.up * velocity
        # if keys[pg.K_LSHIFT]:
        #     self.position -= self.up * velocity

    def check_wall(self, x, y):
        return (x, y) not in self.app.map.world_map
    
    def try_move(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.app.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
            self.position.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
            self.position.z += dy
            
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)

