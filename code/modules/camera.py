import numpy as np
from modules.objects import Ray

class Camera:
    def __init__(self, posicao, AtPoint, UpPoint):
        self.posicao = np.array(posicao, dtype=float)
        self.AtPoint = np.array(AtPoint, dtype=float)
        self.UpPoint = np.array(UpPoint, dtype=float)

        self.update_basis()

    def update_basis(self):
        """
        Recalcula u,v,w sempre que Eye/At/Up mudar
        """
        self.w = self.posicao - self.AtPoint
        self.w = self.w / np.linalg.norm(self.w)

        self.u = np.cross(self.UpPoint, self.w)
        self.u = self.u / np.linalg.norm(self.u)

        self.v = np.cross(self.w, self.u)

    def world_to_camera(self, p):
        """
        Converte ponto do mundo para coordenadas de camera
        """
        d = p - self.posicao
        return np.array([
            np.dot(d, self.u),
            np.dot(d, self.v),
            np.dot(d, self.w)
        ])
    
class Projecao:
    def __init__(self, fov, aspect_ratio, focal=1.0):
        self.aspect = aspect_ratio
        self.focal = focal

        # perspectiva
        self.set_fov(fov)

        # ortográfica (default grande)
        self.ortho = False
        self.ortho_width  = 300.0
        self.ortho_height = 300.0

    def set_fov(self, fov):
        self.fov = fov
        self.persp_h = np.tan(fov / 2)
        self.persp_w = self.persp_h * self.aspect

    def set_ortho_size(self, width, height):
        self.ortho_width = width
        self.ortho_height = height

    def set_ortho(self, state=True):
        self.ortho = state

    def generate_ray(self, camera, i, j, nx, ny):

        if self.ortho:
            # escala ortográfica independente
            px = (2 * (i + 0.5) / nx - 1) * (self.ortho_width / 2)
            py = (1 - 2 * (j + 0.5) / ny) * (self.ortho_height / 2)

            origem = camera.posicao + px * camera.u + py * camera.v
            direcao = -camera.w
            return Ray(origem, direcao)

        else:
            # perspectiva normal
            px = (2 * (i + 0.5) / nx - 1) * self.persp_w
            py = (1 - 2 * (j + 0.5) / ny) * self.persp_h

            p_cam = px * camera.u + py * camera.v - self.focal * camera.w
            direcao = p_cam / np.linalg.norm(p_cam)

            return Ray(camera.posicao, direcao)
