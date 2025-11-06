import numpy as np
from objects import Ray

class Triangulo:
    def __init__(self, v0, v1, v2):
        """
        define um obj da classe triangulo a partir de seus 3 vertices
        """
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.vertices = np.array([v0,v1,v2])

    def intersect(self, ray: Ray):
        r1 = self.v1 - self.v0
        r2 = self.v2 - self.v0
        # calculo da normal
        N  = np.cross(r1,r2)
        n = N/ np.linalg.norm(N)
        # calculo do ponto de intersecao 
        tI = - np.dot((ray.origem - self.v0), n) / np.dot(ray.direcao, n)
        pI = ray.origem + tI * ray.direcao
        # verificacao da posicao do ponto tI 
        denom = np.dot(N,n) # r1 x r2 . n
        c1 = (np.dot(np.cross((self.v2 - pI), (self.v0 - pI)), n))/ denom
        c2 = (np.dot(np.cross((self.v0 - pI), (self.v1 - pI)), n))/ denom
        c3 = (np.dot(np.cross((self.v1 - pI), (self.v2 - pI)), n))/ denom
        
        if c1 <= 0 or c2<= 0 or c3<=0:
            return None
        return { "t": tI,
                "ponto": pI,
                "normal" : n,
                "obj": self
        }

class Face:
    def __init__(self, tri1: Triangulo, tri2: Triangulo, cor):
        """
        define um obj da classe face a partir dos triangulos que o compoem 
        """
        # o quadrado eh p ser formado pela juncao de 2 triangulos que possuem 2 vertices iguais
        verticesQuad = []
        for vertice in tri1.vertices:
            if vertice not in verticesQuad:
                verticesQuad.append(vertice)
        for vertice in tri2.vertices:
            if vertice not in verticesQuad:
                verticesQuad.append(vertice)
        
        self.tri1 = tri1
        self.tri2 = tri2
        self.vertices = verticesQuad        
        self.cor = np.array(cor, dtype = float) / 255.0
    
    def intersect(self, ray: Ray):
        intersec = None
        for element in [self.tri1, self.tri2]:
            hit = element.intersect(ray)
            if hit is None:
                continue
            if intersec is None or hit["t"] < intersec["t"]:
                intersec = hit
        return intersec

class Cubo:
    def __init__(self, faces, Kd, Ks, Ke): 
        """
        define um obj da classe Cubo a partir das suas faces
        """
        # o cubo eh p´ser formado pela 6 faces quadradas
        # as faces compartilham vertices, mapear os 8 vertices
        for face in faces:
            pass 

        pass

    def intersect(self, ray):
        pass