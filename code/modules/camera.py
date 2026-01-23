import numpy as np
from modules.objects import Ray

class Camera:
    def __init__(self, posicao, AtPoint, UpPoint):
        self.posicao = np.array(posicao, dtype=float)
        self.AtPoint = np.array(AtPoint, dtype=float)
        self.UpPoint = np.array(UpPoint, dtype=float)

        # Base da camera
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

class ProjecaoPerspectiva:
    def __init__(self, fov, aspect_ratio):
        self.fov = fov              # em radianos
        self.aspect = aspect_ratio

        self.h = np.tan(fov / 2)
        self.w = self.h * aspect_ratio

    def generate_ray(self, camera: Camera, i, j, nx, ny):
        """
        Gera raio passando pelo pixel (i,j)
        """

        # coordenadas normalizadas do pixel [-1,1]
        px = (2 * (i + 0.5) / nx - 1) * self.w
        py = (1 - 2 * (j + 0.5) / ny) * self.h

        # ponto no plano de imagem em coords de câmera
        p_cam = px * camera.u + py * camera.v - camera.w

        origem = camera.posicao
        direcao = p_cam / np.linalg.norm(p_cam)

        return Ray(origem, direcao)

class ProjecaoOrtografica:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    def generate_ray(self, camera: Camera, i, j, nx, ny):

        px = (2 * (i + 0.5) / nx - 1) * self.largura
        py = (1 - 2 * (j + 0.5) / ny) * self.altura

        origem = (
            camera.posicao
            + px * camera.u
            + py * camera.v
        )

        direcao = -camera.w   # todos paralelos

        return Ray(origem, direcao)
