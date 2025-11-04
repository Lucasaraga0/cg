import numpy as np
from abc import ABC, abstractmethod

class Ray:
    def __init__(self, origem, direcao):
        self.origem = np.array(origem, dtype=float)
        self.direcao = np.array(direcao, dtype=float)
        self.direcao /= np.linalg.norm(self.direcao)

class SimpleObject(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def intersect(self, ray):
        pass

class Esfera(SimpleObject):
    def __init__(self, centro, raio, cor, Kd=0.7, Ks=0.3, Ka =0.2 ,m=20):
        self.centro = np.array(centro, dtype=float)
        self.raio = raio
        self.cor = np.array(cor, dtype=float) / 255.0
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m = m

    def intersect(self, ray: Ray):
        OC = ray.origem - self.centro
        a = np.dot(ray.direcao, ray.direcao)
        b = 2.0 * np.dot(ray.direcao, OC)
        c = np.dot(OC, OC) - self.raio**2
        delta = b**2 - 4*a*c

        if delta < 0:
            return None

        t1 = (-b - np.sqrt(delta)) / (2*a)
        t2 = (-b + np.sqrt(delta)) / (2*a)

        if t1 > 0 and t2 > 0:
            t = min(t1, t2)
        elif t1 > 0:
            t = t1
        elif t2 > 0:
            t = t2
        else:
            return None

        ponto = ray.origem + t * ray.direcao
        normal = (ponto - self.centro) / self.raio
        return {"t": t, "ponto": ponto, "normal": normal, "cor": self.cor,
                "Kd": self.Kd, "Ks": self.Ks, "Ka": self.Ka, "m": self.m}


class Plano(SimpleObject):
    def __init__(self, pontoPi, normalPlano, cor, Kd, Ks, Ka, m=1):
        self.pontoPi = np.array(pontoPi)
        self.normalPlano = np.array(normalPlano)
        self.cor = np.array(cor, dtype=float) / 255.0
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m = m

    def intersect(self, ray:Ray):
        w = ray.origem - self.pontoPi
        ti = - (np.dot(w,self.normalPlano))/(np.dot(ray.direcao, self.normalPlano))
        if ti < 0:
            return None
        pontoI = ray.origem + ti * ray.direcao
        return {"t":ti, "ponto": pontoI, "normal": self.normalPlano, "cor": self.cor,
                "Kd": self.Kd, "Ks": self.Ks,"Ka": self.Ka ,"m": self.m}
        
class Cilindro(SimpleObject):
    def __init__(self, centroBase, raioBase, altura, vetorDir, cor, Kd, Ks, Ka, m):
        self.centroBase = np.array(centroBase)
        self.raioBase = raioBase
        self.altura = altura
        self.vetorDir = np.array(vetorDir)
        self.vetorDir /= np.linalg.norm(self.vetorDir) 
        self.cor = np.array(cor, dtype=float) / 255.0
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m = m
        
    def intersect(self, ray: Ray):
        dc = self.vetorDir 
        dr = ray.direcao 
        w = ray.origem - self.centroBase

        M = np.eye(3) - np.outer(dc, dc)

        a = dr @ M @ dr
        b = 2 * (w @ M @ dr)
        c = w @ M @ w - self.raioBase**2

        delta = b**2 - 4 * a * c
        if delta < 0:
            return None

        sqrt_delta = np.sqrt(delta)
        t_candidates = [(-b - sqrt_delta) / (2 * a), (-b + sqrt_delta) / (2 * a)]
        t = None

        for cand in t_candidates:
            if cand <= 0:
                continue

            # sI é o vetor do centro da base até o ponto de interseção
            sI = w + cand * dr
            res = np.dot(sI, dc)  # projeção ao longo do eixo do cilindro

            # Verifica se o ponto está entre as tampas
            if 0 <= res <= self.altura:
                t = cand
                break

        if t is None:
            return None

 
        ponto = ray.origem + t * dr

        # recomputa sI e rI
        sI = w + t * dr
        res = np.dot(sI, dc)
        rI = sI - res * dc  
        normal = rI / np.linalg.norm(rI)

        return {
            "t": t,
            "ponto": ponto,
            "normal": normal,
            "Kd": self.Kd,
            "Ks": self.Ks,
            "Ka": self.Ka,
            "m": self.m,
            "cor": self.cor
        }

    
class Cone(SimpleObject):
    def __init__(self):
        pass