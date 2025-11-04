import numpy as np
from modules.objects import Ray


def calcular_iluminacao(ponto, normal, view_dir, luz, Kd, Ks, Ka, LuzAmb, m, objetos):
    l, I_F = luz.dir_intensi(ponto)
    l /= np.linalg.norm(l)
    normal /= np.linalg.norm(normal)
    view_dir /= np.linalg.norm(view_dir)

    epsilon = 1e-4  # pequeno deslocamento pra evitar autointerseção
    origem_shadow = ponto + epsilon * normal
    shadow_ray = Ray(origem_shadow, l)

    intersec_sombra = cenario_intersect(objetos, shadow_ray)

    # checa se há objeto entre ponto e luz
    if intersec_sombra is not None:
        t_luz = np.linalg.norm(luz.posicao - ponto)
        if intersec_sombra["t"] < t_luz:
            # ponto está na sombra -> só luz ambiente
            return Ka * LuzAmb

    diff = max(np.dot(normal, l), 0.0)
    r = 2 * np.dot(normal, l) * normal - l
    r /= np.linalg.norm(r)
    spec = max(np.dot(r, view_dir), 0.0) ** m

    return I_F * (Kd * diff + Ks * spec) + Ka * LuzAmb


def cenario_intersect(listaObjetos, ray):
    intersec = None
    for element in listaObjetos:
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