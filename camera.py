import math
import glm
import pygame as pg
from map import WALL_IDs

from settings import FAR, FOV, HALF_HEIGHT, HALF_WIDTH, MOUSE_BORDER_LEFT, MOUSE_BORDER_RIGHT, MOUSE_MAX_REL, MOUSE_SENSITIVITY, NEAR, PLAYER_POS, PLAYER_ROT_SPEED, PLAYER_SIZE_SCALE, PLAYER_SPEED, WIDTH



class Camera:
    def __init__(self, app, position=(20, 1, -6), yaw=-90) -> None:
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()
    
        self.speed = PLAYER_SPEED * self.app.delta_time
        self.x, self.y = PLAYER_POS
        self.diag_move_corr = 1 / math.sqrt(2)
    
    
    def rotate(self):
        rel_x, _ = pg.mouse.get_rel()
        self.yaw += rel_x * MOUSE_SENSITIVITY

    def update_camera_vectors(self):
        yaw= glm.radians(self.yaw)

        self.forward.x = glm.cos(yaw)
        self.forward.z = glm.sin(yaw)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))

    def update(self):
        self.move()
        self.mouse_control()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()
        print(self.position)
    def move(self):
        # velocity = PLAYER_SPEED * self.app.delta_time
        # keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.try_move(self.forward * velocity)
        #     # self.position += self.forward * velocity
        # if keys[pg.K_a]:
        #     self.try_move(-self.right * velocity)
        #     # self.position -= self.right * velocity
        # if keys[pg.K_s]:
        #     self.try_move(-self.forward * velocity)
        #     # self.position -= self.forward * velocity
        # if keys[pg.K_d]:
        #     self.try_move(self.right * velocity)
        #     # self.position += self.right * velocity
        sin_a = math.sin(self.yaw)
        cos_a = math.cos(self.yaw)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.app.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.yaw -= PLAYER_ROT_SPEED * self.app.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.yaw += PLAYER_ROT_SPEED * self.app.delta_time
        # self.yaw %= math.tau
        self.position.x = self.x * 6 + 3
        self.position.z = self.y * 6 - 3
        
    def is_wall(self, x, y):
        return self.app.map.mini_map[x][y] in WALL_IDs


    def try_move(self, vec: glm.vec3):
        scale = PLAYER_SIZE_SCALE / self.app.delta_time
        move = (self.position + vec * scale) / 6
        print(f"P {round(-self.position.z/6, 2)}, {round(self.position.x/6, 2)} + {-round(vec.z,2)}, {round(vec.x,2)} = {round(-move.z,2)}, {round(move.x,2)}  M {int(move.x)}, {int(-move.z)}")
        print(f'W {self.app.map.mini_map[int(move.x)][int(move.y)]}')
        if move.x < 0 or -move.z < 0 or move.x >= len(self.app.map.mini_map[0]) or move.z >= len(self.app.map.mini_map):
            return  
        if not self.is_wall(int(move.x), int(-move.z)):
            self.position += vec
            print("Can move")

    
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)



    def mouse_control(self):
        mx, _ = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.yaw += self.rel * MOUSE_SENSITIVITY * self.app.delta_time

    def draw(self):
        pg.draw.line(self.app.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.yaw),
                     self.y * 100 + WIDTH * math. sin(self.yaw)), 2)
        pg.draw.circle(self.app.screen, 'green', (self.x * 100, self.y * 100), 15)

        
    def check_wall(self, x, y):
        return (x, y) not in self.app.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.app.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy