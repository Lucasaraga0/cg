import numpy as np

def calcular_iluminacao(ponto, normal, view_dir, luz, Kd, Ks, Ka, LuzAmb ,m):
    """
    - ponto: np.array, posicao do ponto 
    - normal: vetor normal no ponto
    - view_dir: vetor da camera 
    - luz: instância de Luz 
    - Kd: coeficiente difuso
    - Ks: coeficiente especular
    - Ka: Coeficiente do ambiente
    - LuzAmb: Iluminacao
    - m: expoente especular (brilho)
    """
    
    l, I_F = luz.dir_intensi(ponto)
    l /= np.linalg.norm(l)
    normal /= np.linalg.norm(normal)
    view_dir /= np.linalg.norm(view_dir)

    diff = max(np.dot(normal, l), 0.0)

    r = 2 * np.dot(normal, l) * normal - l
    r /= np.linalg.norm(r)
    spec = max(np.dot(r, view_dir), 0.0) ** m

    return I_F * (Kd * diff + Ks * spec + Ka * LuzAmb)

def cenario_intersect(lista, ray):
    intersec = None
    for element in lista:
        Element_intersec = element.intersect(ray)
        if Element_intersec is None:
            continue
        else:
            if intersec is None:
                intersec = Element_intersec
            elif intersec["t"] > Element_intersec["t"]:
                intersec = Element_intersec
    return intersec

def normalize(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)