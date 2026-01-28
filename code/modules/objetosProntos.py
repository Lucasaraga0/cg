import numpy as np
from modules.objects import Esfera, Cilindro, Cone
from modules.complexObjects import Cubo
import numpy as np

from modules.objects import Esfera, Plano, Cilindro, Cone
from modules.complexObjects import Cubo

# ============================================================
# QUARTO (6 PLANOS)
# ============================================================
def criar_quarto(W, H, D,
                 cor_paredes=(200, 200, 200),
                 cor_chao=(150, 150, 150),
                 cor_teto=(180, 180, 180),
                 Kd=0.7, Ks=0.1, Ka=0.2,
                 textura_paredes=None,
                 textura_chao=None,
                 textura_teto=None):

    planos = []

    # chão
    chao = Plano(
        pontoPi=[0, 0, 0],
        normalPlano=[0, 1, 0],
        cor=cor_chao,
        Kd=Kd, Ks=Ks, Ka=Ka,
        texture=textura_chao
    )
    planos.append(chao)

    # teto
    teto = Plano(
        pontoPi=[0, H, 0],
        normalPlano=[0, -1, 0],
        cor=cor_teto,
        Kd=Kd, Ks=Ks, Ka=Ka,
        texture=textura_teto
    )
    planos.append(teto)

    # parede de fundo (z = 0)
    parede_fundo = Plano(
        pontoPi=[0, 0, 0],
        normalPlano=[0, 0, 1],
        cor=cor_paredes,
        Kd=Kd, Ks=Ks, Ka=Ka,
        texture=textura_paredes
    )
    planos.append(parede_fundo)

    # parede da frente (z = D)
    parede_frente = Plano(
        pontoPi=[0, 0, D],
        normalPlano=[0, 0, -1],
        cor=cor_paredes,
        Kd=Kd, Ks=Ks, Ka=Ka,
        texture=textura_paredes
    )
    planos.append(parede_frente)

    # parede esquerda (x = 0)
    parede_esq = Plano(
        pontoPi=[0, 0, 0],
        normalPlano=[1, 0, 0],
        cor=cor_paredes,
        Kd=Kd, Ks=Ks, Ka=Ka,
        texture=textura_paredes
    )
    planos.append(parede_esq)

    # parede direita (x = W)
    parede_dir = Plano(
        pontoPi=[W, 0, 0],
        normalPlano=[-1, 0, 0],
        cor=cor_paredes,
        Kd=Kd, Ks=Ks, Ka=Ka,
        texture=textura_paredes
    )
    planos.append(parede_dir)

    return planos

# ============================================================
# ARVORE DE NATAL (CILINDRO + CONE)
# ============================================================

def criar_arvore_natal(pos_x=70, pos_z=30):
    objetos = []

    # tronco
    tronco = Cilindro(
        centroBase=[pos_x, 0, pos_z],
        raioBase=8,
        altura=30,
        vetorDir=[0, 1, 0],
        cor=[120, 50, 30],
        Kd=0.7, Ks=0.3, Ka=0.2, m=10
    )

    # copa
    copa = Cone(
        centroBase=[pos_x, 30, pos_z],
        raioBase=50,
        altura=120,
        vetorDir=[0, 1, 0],
        cor=[30, 180, 30],
        Kd=0.7, Ks=0.3, Ka=0.2, m=10
    )

    objetos.append(tronco)
    objetos.append(copa)

    return objetos

# PUFF (CUBO ROXO)
def criar_puff(base_pos = [], tam=30):

    puff = Cubo(
        tamAresta=tam,
        centro_base=base_pos,
        ux=[1, 0, 0],
        uy=[0, 1, 0],
        uz=[0, 0, 1],
        cor=[160, 80, 200],   # roxo
        Kd=0.7, Ks=0.3, Ka=0.2,
        m=20
    )

    return [puff]

# SNOWMAN (3 ESFERAS + 2 OLHOS + 1 CONE)

def criar_snowman(base_pos):

    objs = []
    base_pos = np.array(base_pos, float)

    # raios do corpo
    r1 = 25   # base
    r2 = 18   # meio
    r3 = 12   # cabeça

    # centros das esferas do corpo
    c1 = base_pos + np.array([0, r1, 0])
    c2 = c1 + np.array([0, r1 + r2, 0])
    c3 = c2 + np.array([0, r2 + r3, 0])

    corpo1 = Esfera(c1, r1, cor=[255, 255, 255], Kd=0.7, Ks=0.3, Ka=0.2, m=20)
    corpo2 = Esfera(c2, r2, cor=[255, 255, 255], Kd=0.7, Ks=0.3, Ka=0.2, m=20)
    corpo3 = Esfera(c3, r3, cor=[255, 255, 255], Kd=0.7, Ks=0.3, Ka=0.2, m=20)

    objs.append(corpo1)
    objs.append(corpo2)
    objs.append(corpo3)
    
    # olhos
    olho_offset_y = 2
    olho_offset_z = 10
    olho_offset_x = 4

    olho1 = Esfera(
        c3 + np.array([-olho_offset_x, olho_offset_y, olho_offset_z]),
        2,
        cor=[0, 0, 0],
        Kd=0.7, Ks=0.3, Ka=0.2, m=5
    )

    olho2 = Esfera(
        c3 + np.array([olho_offset_x, olho_offset_y, olho_offset_z]),
        2,
        cor=[0, 0, 0],
        Kd=0.7, Ks=0.3, Ka=0.2, m=5
    )

    objs.append(olho1)
    objs.append(olho2)

    # nariz (cone laranja)
    nariz_base = c3 + np.array([0, 0, olho_offset_z])

    nariz = Cone(
        centroBase=nariz_base,
        raioBase=2,
        altura=10,
        vetorDir=[0, 0, 1],
        cor=[255, 120, 0],
        Kd=0.7, Ks=0.3, Ka=0.2,
        m=10
    )

    objs.append(nariz)

    return objs