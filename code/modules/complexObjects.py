import numpy as np
from modules.objects import Ray

class Triangulo:
    def __init__(self, v0, v1, v2, cor, Kd, Ks, Ka, m):
        """
        define um obj da classe triangulo a partir de seus 3 vertices
        """
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.vertices = np.array([v0,v1,v2])
        self.cor = np.array(cor, dtype = float) / 255.0
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m = m

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
    def __init__(self, tri1: Triangulo, tri2: Triangulo):
        """
        define um obj da classe face a partir dos triangulos que o compoem 
        """
        # o quadrado eh p ser formado pela juncao de 2 triangulos que possuem 2 vertices iguais
        verticesQuad = []
        for vertice in tri1.vertices:
            if not any(np.allclose(vertice, v) for v in verticesQuad):
                verticesQuad.append(vertice)
        for vertice in tri2.vertices:
            if not any(np.allclose(vertice, v) for v in verticesQuad):
                verticesQuad.append(vertice)


        self.tri1 = tri1
        self.tri2 = tri2
        self.vertices = verticesQuad        
    
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
    def __init__(self, tamAresta, centro_base, ux, uy, uz, cor, Kd, Ks, Ka, m):
        """
        Constrói um cubo a partir do tamanho da aresta, do centro da BASE,
        e dos vetores de orientação locais (ux, uy, uz).
        """

        self.a = tamAresta
        self.cor = cor
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m = m
        # normalizar eixos locais
        ux = np.array(ux, dtype=float)
        uy = np.array(uy, dtype=float)
        uz = np.array(uz, dtype=float)

        ux = ux / np.linalg.norm(ux)
        uy = uy / np.linalg.norm(uy)
        uz = uz / np.linalg.norm(uz)

        self.ux = ux
        self.uy = uy
        self.uz = uz

        # converter centro da base → centro do cubo
        centro_base = np.array(centro_base, dtype=float)
        centro_cubo = centro_base + (tamAresta/2) * uy
        self.centro = centro_cubo

        # meia aresta
        h = tamAresta / 2.0

        # gerar os 8 vértices
        offsets = [
            -ux*h - uy*h - uz*h,
            +ux*h - uy*h - uz*h,
            -ux*h + uy*h - uz*h,
            +ux*h + uy*h - uz*h,
            -ux*h - uy*h + uz*h,
            +ux*h - uy*h + uz*h,
            -ux*h + uy*h + uz*h,
            +ux*h + uy*h + uz*h,
        ]
        self.vertices = [centro_cubo + off for off in offsets]

        # faces do cubo (cada uma com 4 vértices)
        faces_idx = [
            (0,1,3,2),  
            (4,5,7,6),  
            (0,1,5,4),  
            (2,3,7,6),  
            (0,2,6,4),  
            (1,3,7,5),  
        ]

        self.faces = []
        for i0, i1, i2, i3 in faces_idx:
            v0 = self.vertices[i0]
            v1 = self.vertices[i1]
            v2 = self.vertices[i2]
            v3 = self.vertices[i3]

            t1 = Triangulo(v0, v1, v2, cor, Kd, Ks, Ka, m)
            t2 = Triangulo(v0, v2, v3, cor, Kd, Ks, Ka, m)
            face = Face(t1, t2)

            self.faces.append(face)

    def intersect(self, ray):
        intersec = None
        for face in self.faces:
            hit = face.intersect(ray)
            if hit is None:
                continue

            if hit["t"] > 0:
                if intersec is None or hit["t"] < intersec["t"]:
                    intersec = hit

        return intersec
