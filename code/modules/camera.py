import numpy as np

class Camera:
    def __init__(self, posicao, AtPoint, UpPoint, distanciaFocal, campoVisao):
        self.posicao = posicao
        self.AtPoint = AtPoint
        self.UpPoint = UpPoint
        self.distanciaFocal = distanciaFocal
        self.campoVisao = campoVisao
        

