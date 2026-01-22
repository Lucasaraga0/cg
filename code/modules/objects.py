from PIL import Image
import numpy as np
from abc import ABC, abstractmethod
from modules.transformations import translate

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

    @abstractmethod
    def translateObject(self, matrix):
        pass
    
    @abstractmethod 
    def rotateObject(self, matrix):
        pass

    @abstractmethod
    def scaleObject(self, matrix):
        pass
    
    #@abstractmethod
    #def shearObject(self, matrix):
    #    pass

    #@abstractmethod
    #def reflectObject(self, matrix):
    #    pass
    
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
        return {"t": t, 
                "ponto": ponto, 
                "normal": normal, 
                "obj":self}

    def translateObject(self, matrix):
        pontoInicial = self.centro
        pontoAplicavel = np.insert(pontoInicial, 3, 1)
        self.centro = (matrix @ pontoAplicavel)[:3]

    def scaleObject(self, matrix):
        # so aumenta o raio da esfera
        self.raio *= matrix[0][0]

    def rotateObject(self, matrix):
        # rotacionar esfera nao faz nada
        pass


def load_texture(path):
    img = Image.open(path).convert("RGB")
    img = np.array(img, dtype=np.float32) / 255.0

    # sRGB → linear
    img = np.power(img, 2.2)
    return img


def criar_base_plano(normal):
    if abs(normal[1]) > 0.9:  # chão ou teto
        eixo_u = np.array([1, 0, 0])
        eixo_v = np.array([0, 0, 1])
    else:  # parede
        eixo_u = np.array([1, 0, 0])
        eixo_v = np.array([0, 1, 0])

    return eixo_u, eixo_v



class Plano(SimpleObject):
    def __init__(self, pontoPi, normalPlano, cor, Kd, Ks, Ka, m=1, texture = None, tex_scale = 1.0):
        self.pontoPi = np.array(pontoPi, dtype= float)
        self.normalPlano = np.array(normalPlano)
        self.cor = np.array(cor, dtype=float) / 255.0
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m = m
        self.texture = texture

        if texture is not None:
            self.tex_scale = tex_scale  # controla repetição da textura
            # base local do plano
            self.eixo_u, self.eixo_v = criar_base_plano(self.normalPlano)

    def get_uv(self, ponto):
        rel = ponto - self.pontoPi

        u = np.dot(rel, self.eixo_u) * self.tex_scale
        v = np.dot(rel, self.eixo_v) * self.tex_scale

        # repete textura
        u = u % 1.0
        v = v % 1.0

        return u, v

    def sample_texture(self, ponto):
        if self.texture is None:
            return self.cor

        h, w, _ = self.texture.shape
        u, v = self.get_uv(ponto)

        x = int(u * (w - 1))
        y = int((1 - v) * (h - 1))

        tex_color = self.texture[y, x]

        return tex_color

    def intersect(self, ray:Ray):
        w = ray.origem - self.pontoPi
        den = (np.dot(ray.direcao, self.normalPlano))

        if abs(den) < 1e-6:
                    return None  

        ti = - (np.dot(w,self.normalPlano))/den
        if ti < 0:
            return None
        
        pontoI = ray.origem + ti * ray.direcao
            
        return {"t":ti, 
                "ponto": pontoI, 
                "normal": self.normalPlano, 
                "cor": self.sample_texture(pontoI),
                "obj": self}

    def translateObject(self, matrix):
        pontoAplicavel = np.insert(self.pontoPi, 3, 1)
        self.pontoPi = (matrix @ pontoAplicavel)[:3]

    def scaleObject(self, matrix):
        # faz nada pq nn tem sentido escalar um plano
        pass

    def rotateObject(self, matrix):
        pontoAplicavel = np.insert(self.pontoPi, 3 , 1)
        origem = np.zeros(3)

        matriz_ida = translate(PInicial= pontoAplicavel, PFinal= origem)
        matriz_volta = translate(PInicial = origem, PFinal= pontoAplicavel)
        # translada pra origem, rotaciona e volta pro ponto original
        self.pontoPi = (matriz_volta @ matrix @ matriz_ida @ pontoAplicavel)[:3]

        # rotaciona a normal    
        self.normalPlano = matrix[:3,:3] @ self.normalPlano
        self.normalPlano /= np.linalg.norm(self.normalPlano)

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
            "obj": self
        }
    
    def translateObject(self, matrix):
        pontoAplicavel = np.insert(self.centroBase, 3, 1)
        self.centroBase = (matrix @ pontoAplicavel)[:3]
    
    def scaleObject(self, matrix):
        # por questoes de simplicidade deixei a escala uniforme em relacao a todos os eixos
        escala = matrix[0][0]
        self.altura *= escala
        self.raioBase *= escala 

    def rotateObject(self, matrix):
        pontoAplicavel = np.insert(self.centroBase, 3, 1)
        origem = np.zeros(3)

        matriz_ida = translate(PInicial= pontoAplicavel, PFinal= origem)
        matriz_volta = translate(PInicial = origem, PFinal= pontoAplicavel)
        self.centroBase = (matriz_volta @ matrix @ matriz_ida @ pontoAplicavel)[:3]

        # rotaciona a direcao 

        self.vetorDir = matrix[:3,:3] @ self.vetorDir
        self.vetorDir /= np.linalg.norm(self.vetorDir)

    
class Cone(SimpleObject):
    def __init__(self, centroBase, raioBase, altura, vetorDir, cor, Kd, Ks, Ka, m):
        self.centroBase = np.array(centroBase, dtype = float)
        self.raioBase = raioBase
        self.altura = altura
        self.vetorDir = np.array(vetorDir, dtype= float)
        self.vetorDir /= np.linalg.norm(self.vetorDir)
        self.cor = np.array(cor, dtype= float)/ 255.0
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m = m
    
    def intersect(self, ray: Ray):
        dc = self.vetorDir 
        H = self.altura
        dr = ray.direcao 
        w = ray.origem - self.centroBase

        M = np.eye(3) - np.outer(dc, dc)
        M_bar = np.outer(dc,dc)
        M_ast = M_bar - ((H/self.raioBase)**2) * M
        
        a = dr.T @ M_ast @ dr
        b = 2 * w.T @ M_ast @ dr - 2 * H * dr.T @ dc
        c = w.T @ M_ast @ w - 2 * H * w.T @ dc + H**2

        delta =  b**2 - 4*a*c
        
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
            "obj": self
        }
    
    def translateObject(self, matrix):
        pontoAplicavel = np.insert(self.centroBase, 3, 1)
        self.centroBase = (matrix @ pontoAplicavel)[:3]
    
    def scaleObject(self, matrix):
        # por questoes de simplicidade deixei a escala uniforme em relacao a todos os eixos
        escala = matrix[0][0]
        self.altura *= escala
        self.raioBase *= escala 

    def rotateObject(self, matrix):
        pontoAplicavel = np.insert(self.centroBase, 3, 1)
        origem = np.zeros(3)

        matriz_ida = translate(PInicial= pontoAplicavel, PFinal= origem)
        matriz_volta = translate(PInicial = origem, PFinal= pontoAplicavel)
        self.centroBase = (matriz_volta @ matrix @ matriz_ida @ pontoAplicavel)[:3]

        # rotaciona a direcao 
        self.vetorDir = (matrix)[:3,:3] @ self.vetorDir
        self.vetorDir /= np.linalg.norm(self.vetorDir)