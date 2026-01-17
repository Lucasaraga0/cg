import numpy as np
from modules.objects import Ray


def calcular_iluminacao(ponto, normal, view_dir, luz, Kd, Ks, Ka, LuzAmb, m, objetos, obj_atual):
    """
    ponto: np.array -> posição do ponto
    normal: vetor normal no ponto
    view_dir: vetor da câmera
    luz: instância de Luz
    Kd, Ks, Ka: coeficientes de iluminação
    LuzAmb: intensidade da luz ambiente
    m: expoente especular (brilho)
    objetos: lista de objetos na cena
    obj_atual: o objeto que já foi intersectado
    """

    # direção da luz e intensidade
    l, I_F = luz.dir_intensi(ponto)
    l /= np.linalg.norm(l)
    normal /= np.linalg.norm(normal)
    view_dir /= np.linalg.norm(view_dir)

    # raio de sombra
    epsilon = 1e-4
    origem_shadow = ponto + epsilon * normal
    shadow_ray = Ray(origem_shadow, l)

    # checa se algum outro objeto bloqueia a luz
    intersec_sombra = cenario_intersect(objetos, shadow_ray, ignore=obj_atual)

    if intersec_sombra is not None:
        # distância até a luz
        t_luz = np.linalg.norm(luz.posicao - ponto)
        if intersec_sombra["t"] < t_luz:
            # ponto está na sombra -> só luz ambiente
            return Ka * LuzAmb

    # cálculo do modelo de Phong
    diff = max(np.dot(normal, l), 0.0)
    r = 2 * np.dot(normal, l) * normal - l
    r /= np.linalg.norm(r)
    spec = max(np.dot(r, view_dir), 0.0) ** m

    return I_F * (Kd * diff + Ks * spec) + Ka * LuzAmb


def cenario_intersect(listaObjetos, ray, ignore=None):
    intersec = None
    for element in listaObjetos:
        if element is ignore:
            continue  # evita testar o mesmo objeto
        hit = element.intersect(ray)
        if hit is None:
            continue
        if intersec is None or hit["t"] < intersec["t"]:
            intersec = hit
    return intersec

def apply_transformation(object, matrix):
    """aplica a matriz de transformacao a um objeto"""
    #TODO

def normalize(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


