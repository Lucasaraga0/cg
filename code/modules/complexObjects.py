import numpy as np
from modules.objects import Ray
from modules.transformations import translate

class Triangulo:
    def __init__(self, cubo, i0, i1, i2, cor, Kd, Ks, Ka, m):
        """
        Triângulo definido por índices de vértices do cubo
        """
        self.cubo = cubo          # referência ao cubo dono
        self.i0 = i0
        self.i1 = i1
        self.i2 = i2

        self.cor = cor
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m  = m


    def intersect(self, ray: Ray):
        v0 = self.cubo.vertices[self.i0]
        v1 = self.cubo.vertices[self.i1]
        v2 = self.cubo.vertices[self.i2]

        r1 = v1 - v0
        r2 = v2 - v0

        # calculo da normal
        N  = np.cross(r1,r2)
        n = N/ np.linalg.norm(N)
        # calculo do ponto de intersecao
        w = ray.origem - v0
        d = ray.direcao
        tI = - np.dot(w, n) / np.dot(d, n)
        pI = ray.origem + tI * d
        # verificacao da posicao do ponto tI 
        s1 = v0 - pI
        s2 = v1 - pI
        s3 = v2 - pI
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
                "obj": self.cubo
        }

class Face:
    def __init__(self, cubo, i0, i1, i2, i3, cor, Kd, Ks, Ka, m):
        """
        Face quadrada definida por 4 índices de vértices do cubo
        """
        self.cubo = cubo
        self.i0 = i0
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3

        # dois triângulos da face
        self.tri1 = Triangulo(cubo, i0, i1, i2, cor, Kd, Ks, Ka, m)
        self.tri2 = Triangulo(cubo, i0, i2, i3, cor, Kd, Ks, Ka, m)
     
    
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
        self.cor = np.array(cor, dtype=float) / 255.0
        self.Kd = Kd
        self.Ks = Ks
        self.Ka = Ka
        self.m  = m

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
        centro_cubo = centro_base + (tamAresta / 2.0) * uy
        self.centro = centro_cubo

        # meia aresta
        h = tamAresta / 2.0

        # gerar os 8 vértices
        offsets = [
            -ux*h - uy*h - uz*h,  # 0
            +ux*h - uy*h - uz*h,  # 1
            -ux*h + uy*h - uz*h,  # 2
            +ux*h + uy*h - uz*h,  # 3
            -ux*h - uy*h + uz*h,  # 4
            +ux*h - uy*h + uz*h,  # 5
            -ux*h + uy*h + uz*h,  # 6
            +ux*h + uy*h + uz*h,  # 7
        ]

        self.vertices = [centro_cubo + off for off in offsets]

        # faces do cubo (cada uma com 4 índices de vértices)
        faces_idx = [
            (0, 1, 3, 2),  # face inferior
            (4, 5, 7, 6),  # face superior
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 2, 6, 4),
            (1, 3, 7, 5),
        ]

        self.faces = []
        for i0, i1, i2, i3 in faces_idx:
            face = Face(
                cubo=self,
                i0=i0, i1=i1, i2=i2, i3=i3,
                cor=cor, Kd=Kd, Ks=Ks, Ka=Ka, m=m
            )
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

    def translateObject(self, matrix):
        
        # aplica em todos os vértices
        novos_vertices = []
        for v in self.vertices:
            v_h = np.insert(v, 3, 1)
            v_t = matrix @ v_h
            novos_vertices.append(v_t[:3])

        self.vertices = novos_vertices

        # atualiza centro
        c_h = np.insert(self.centro, 3, 1)
        self.centro = (matrix @ c_h)[:3]


    def scaleObject(self, matrix):

        origem = np.zeros(3)

        # matrizes de ida e volta
        matriz_ida   = translate(self.centro, origem)
        matriz_volta = translate(origem, self.centro)

        novos_vertices = []
        for v in self.vertices:
            v_h = np.insert(v, 3, 1)
            v_t = matriz_volta @ matrix @ matriz_ida @ v_h
            novos_vertices.append(v_t[:3])

        self.vertices = novos_vertices

        # atualiza centro (não muda na escala em torno dele, mas mantemos coerente)
        c_h = np.insert(self.centro, 3, 1)
        self.centro = (matriz_volta @ matrix @ matriz_ida @ c_h)[:3]


    def rotateObject(self, matrix):
        origem = np.zeros(3)

        # matrizes de ida e volta
        matriz_ida   = translate(self.centro, origem)
        matriz_volta = translate(origem, self.centro)

        novos_vertices = []
        for v in self.vertices:
            v_h = np.insert(v, 3, 1)
            v_r = matriz_volta @ matrix @ matriz_ida @ v_h
            novos_vertices.append(v_r[:3])

        self.vertices = novos_vertices

        # atualiza centro
        c_h = np.insert(self.centro, 3, 1)
        self.centro = (matriz_volta @ matrix @ matriz_ida @ c_h)[:3]
