import numpy as np
import glm


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # Translate pos
        m_model = glm.translate(m_model, self.pos)
        # Rotate
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        # Scale
        m_model = glm.scale(m_model, self.scale)
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()
        
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(3, 3, 3)) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class SkyBox(ExtendedBaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))
    
    def on_init(self): 
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)


class Wall(ExtendedBaseModel):
    def __init__(self, app, vao_name='wall', tex_id=4, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Monkey(ExtendedBaseModel):
    def __init__(self, app, vao_name='monkey', tex_id='monkey', pos=(0, 0, 0), rot=(-90, 0, 0), scale=(0.05, 0.05, 0.05)) -> None:
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

    def update(self):
        self.m_model = self.get_model_matrix()
        super().update()

    def update_npc_orientation(self, camera):
        npc_pos = self.pos  # Assuming `get_position()` returns a vec3 object
        player_pos = camera.position

        direction_vector = player_pos - npc_pos
        direction_vector = glm.vec3(direction_vector.x, 0.0, -direction_vector.z)  # Ignore the vertical component (y-axis) for 2D rotation

        if np.linalg.norm(direction_vector) < 0.01:
            return 0.0
        
        # Normalize the direction vector
        direction_vector /= np.linalg.norm(direction_vector)

        # Calculate the angle between the direction vector and the NPC's forward vector
        forward_vector = glm.vec3(0, 0, -1)
        dot_product = np.dot(direction_vector, forward_vector)
        angle = np.arccos(dot_product)

        # Determine the sign of the angle based on the direction vector
        if direction_vector[0] > 0:
            angle = -angle

        return angle
    
    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        angle = self.update_npc_orientation(self.app.camera)
        m_model = glm.rotate(m_model, glm.radians(-90), glm.vec3(1, 0, 0))
        if angle != 0.0:
            m_model = glm.rotate(m_model, angle, glm.vec3(0, 0, -1))
        # scale
        m_model = glm.scale(m_model, self.scale)
        return m_model