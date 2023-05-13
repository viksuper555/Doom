from shader_program import ShaderProgram
from vbo import VBO


class VAO:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        self.vaos['cube'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['cube']
        )

        self.vaos['wall'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['wall']
        )
        
        self.vaos['skybox'] = self.get_vao(
            program = self.program.programs['skybox'],
            vbo = self.vbo.vbos['skybox']
        )

        self.vaos['monkey'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['monkey']
        )


    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
