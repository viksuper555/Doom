import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/container.jpg')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        
        # Mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AntiAlias Filter
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]