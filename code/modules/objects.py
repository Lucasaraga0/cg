import numpy as np

class Ray:
    def __init__(self, origem, direcao):
        self.origem = np.array(origem, dtype=float)
        self.direcao = np.array(direcao, dtype=float)
        self.direcao /= np.linalg.norm(self.direcao)

class Esfera:
    def __init__(self, centro, raio, cor, Kd=0.7, Ks=0.3, m=20):
        self.centro = np.array(centro, dtype=float)
        self.raio = raio
        self.cor = np.array(cor, dtype=float) / 255.0
        self.Kd = Kd
        self.Ks = Ks
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
                "Kd": self.Kd, "Ks": self.Ks, "m": self.m}


class Cilindro():
    def __init__(self):
        pass

class Cone():
    def __init__(self):
        pass