import numpy as np
from modules.objects import Ray, Plano
from modules.light import LuzAmbiente

def calcular_iluminacao(ponto, normal, view_dir, luzes, obj_atual, objetos):
    """
    ponto: np.array (3,)
    normal: np.array (3,)
    view_dir: np.array (3,)
    luzes: lista de luzes (LuzAmbiente, LuzPontual, LuzDirecional, LuzSpot)
    obj_atual: objeto intersectado
    objetos: lista de objetos da cena
    """

    normal = normal / np.linalg.norm(normal)
    view_dir = view_dir / np.linalg.norm(view_dir)

    Kd = obj_atual.Kd
    Ks = obj_atual.Ks
    Ka = obj_atual.Ka
    m  = obj_atual.m

    I_total = np.zeros(3)

    for luz in luzes:

        if isinstance(luz, LuzAmbiente):
            I_total += Ka * luz.intensidade
            continue

        l, I_F = luz.dir_intensi(ponto)

        # se a luz nao ilumina o ponto no caso da luzSpot
        if np.allclose(I_F, 0):
            continue

        l = l / np.linalg.norm(l)

        # checagem de sombra
        epsilon = 1e-4
        origem_shadow = ponto + epsilon * normal
        shadow_ray = Ray(origem_shadow, l)

        intersec_sombra = cenario_intersect(
            objetos,
            shadow_ray,
            ignore=obj_atual
        )

        em_sombra = False
        if intersec_sombra is not None:
            # Luz pontual
            if hasattr(luz, "posicao"):
                t_luz = np.linalg.norm(luz.posicao - ponto)
                if intersec_sombra["t"] < t_luz:
                    em_sombra = True
            # Luz spot
            elif hasattr(luz, "pontoFonte"):
                t_luz = np.linalg.norm(luz.pontoFonte - ponto)
                if intersec_sombra["t"] < t_luz:
                    em_sombra = True
            # Luz direcional
            else:
                em_sombra = True

        if em_sombra:
            continue

        diff = max(np.dot(normal, l), 0.0)

        r = 2 * np.dot(normal, l) * normal - l
        r = r / np.linalg.norm(r)
        spec = max(np.dot(r, view_dir), 0.0) ** m
        I_total += I_F * (Kd * diff + Ks * spec)

    return np.clip(I_total, 0, 1)


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

def normalize(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)

def render_linhas(args):
    (
        i_start, i_end,
        nx, ny,
        camera,
        projecao,
        cenario,
        luzes,
        bg_color
    ) = args

    bloco = np.zeros((i_end - i_start, nx, 3), dtype=float)

    for ii, i in enumerate(range(i_start, i_end)):
        for j in range(nx):

            # gera o raio pela projeção
            raio = projecao.generate_ray(camera, j, i, nx, ny)

            intersec = cenario_intersect(cenario, raio)

            if intersec is None:
                bloco[ii, j] = bg_color
                continue

            P = intersec["ponto"]
            normal = intersec["normal"]
            normal = normal / np.linalg.norm(normal)

            view_dir = -raio.direcao
            view_dir = view_dir / np.linalg.norm(view_dir)

            obj = intersec["obj"]

            I = calcular_iluminacao(
                ponto=P,
                normal=normal,
                view_dir=view_dir,
                luzes=luzes,
                obj_atual=obj,
                objetos=cenario
            )

            if isinstance(obj, Plano):
                color = intersec["cor"]
            else:
                color = obj.cor

            bloco[ii, j] = np.clip(color * I, 0, 1)

    return i_start, bloco


