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
        w = ray.origem - self.v0
        d = ray.direcao
        tI = - np.dot(w, n) / np.dot(d, n)
        pI = ray.origem + tI * d
        # verificacao da posicao do ponto tI 
        s1 = self.v0 - pI
        s2 = self.v1 - pI
        s3 = self.v2 - pI
        #s3 = vt_final - pI2
        denom = np.linalg.norm(N) 
        
        c1 = np.dot(n, np.cross(s3,s1)) / denom
        c2 = np.dot(n, np.cross(s1,s2)) / denom
        c3 = 1 - c1 - c2

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

class BlocoRetangular:
    def __init__(self, faces, Kd, Ks, Ke): 
        """
        define um obj da classe Cubo a partir das suas faces
        """
        self.faces = faces        
        self.Kd = Kd
        self.Ks = Ks
        self.Ke = Ke

        verts = []
        for face in faces:
            for v in face.vertices:
                if not any(np.allclose(v, x) for x in verts):
                    verts.append(v)
        self.vertices = verts

    def intersect(self, ray):
        intersec = None
        for face in self.faces:
            hit = face.intersect(ray)
            if hit is None:
                continue

            if hit["t"] > 0:  # garantir interseção válida
                if intersec is None or hit["t"] < intersec["t"]:
                    intersec = hit

        return intersec
