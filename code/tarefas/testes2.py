import numpy as np
import pygame
import sys
import multiprocessing as mp

from modules.objects import Esfera, Ray, Plano, load_texture, Cilindro, Cone
from modules.complexObjects import Cubo
from modules.light import LuzPontual, LuzAmbiente, LuzDirecional, LuzSpot
from modules.utils import render_linhas
from modules.transformations import translate, scale, rotateX
from modules.camera import Camera, ProjecaoPerspectiva   
from modules.picking import pick_object
# ----------------------------
# Dimensões da janela em cm
# ----------------------------
Wjanela = 60
Hjanela = 60

# resolução
n_col, n_lin = 500, 500

PIXELS_PER_CM = 10
window_w = int(Wjanela * PIXELS_PER_CM)
window_h = int(Hjanela * PIXELS_PER_CM)

# ----------------------------
# CÂMERA
# ----------------------------
camera_pos = np.array([50.0, 50.0, 0.0])
camera_at  = np.array([50.0, 50.0, 1.0])   # olhando para +z
camera_up  = np.array([0.0, 1.0, 0.0])

camera = Camera(
    posicao=camera_pos,
    AtPoint=camera_at,
    UpPoint=camera_up
)


# FOV em radianos
fov = np.deg2rad(60.0)
aspect_ratio = n_col / n_lin

projecao = ProjecaoPerspectiva(
    fov=fov,
    aspect_ratio=aspect_ratio
)

# ----------------------------
# OBJETOS DA CENA
# ----------------------------

# esfera
r_esfera = 40
centro_esf = np.array([50, 50, 120])
cor_esf = np.array([255, 0, 0], dtype=float)
Kd_esf = Ke_esf = Ka_esf = np.array([0.7, 0.2, 0.2])
m_esf = 10

esfera = Esfera(
    centro=centro_esf,
    raio=r_esfera,
    cor=cor_esf,
    Kd=Kd_esf,
    Ks=Ke_esf,
    Ka=Ka_esf,
    m=m_esf
)

# cilindro
centroBaseCil = np.array([80, 50, 100])
raioCil = 20
HCil = 90
dCil = np.array([0., 1., 0.])
KdCil = KeCil = KaCil = np.array([0.824, 0.706, 0.549])
corCil = np.array([255, 0, 0])

cilindro = Cilindro(
    centroBase=centroBaseCil,
    raioBase=raioCil,
    altura=HCil,
    vetorDir=dCil,
    cor=corCil,
    Kd=KdCil,
    Ks=KeCil,
    Ka=KaCil,
    m=2
)

# cone
cone = Cone(
    centroBase=centroBaseCil,
    raioBase=raioCil,
    altura=HCil,
    vetorDir=dCil,
    cor=corCil,
    Kd=KdCil,
    Ks=KeCil,
    Ka=KaCil,
    m=2
)

# plano do chão
texturaChao = load_texture("../textures/grass.jpg")
pontoChao = np.array([0, 0, 0])
normalChao = np.array([0, 1, 0], dtype=float)
corChao = np.array([137, 81, 41], dtype=float)

Kd_chao = Ka_chao = np.array([0.2, 0.7, 0.2])
Ke_chao = np.array([0, 0, 0])
m_chao = 10

planoChao = Plano(
    pontoPi=pontoChao,
    normalPlano=normalChao,
    cor=corChao,
    Kd=Kd_chao,
    Ks=Ke_chao,
    Ka=Ka_chao,
    m=m_chao,
    texture=texturaChao,
    tex_scale=0.01
)

# plano do fundo
texturaFundo = load_texture("../textures/brick_wall.jpg")
pontoFundo = np.array([0, 0, 200])
normalFundo = np.array([0, 0, -1], dtype=float)  # olhando para dentro da cena
corFundo = np.array([0, 0, 255])

Kd_fundo = Ka_fundo = np.array([0.3, 0.3, 0.7])
Ke_fundo = np.array([0, 0, 0])
m_fundo = 10

planoFundo = Plano(
    pontoPi=pontoFundo,
    normalPlano=normalFundo,
    cor=corFundo,
    Kd=Kd_fundo,
    Ks=Ke_fundo,
    Ka=Ka_fundo,
    m=m_fundo,
    texture=texturaFundo,
    tex_scale=0.01
)

# ----------------------------
# LUZES
# ----------------------------


# luz ambiente
intensidadeAmbiente = np.array([0.8, 0.8, 0.8])
luzAmbiente = LuzAmbiente(intensidadeAmbiente)

# luz pontual
posicaoPontual = np.array([150, 150, 50])
intensidadePontual = np.array([0.5, 0.5, 0.5])
luzPontual = LuzPontual(intensidade=intensidadePontual, posicao=posicaoPontual)

# luz direcional
intensidadeDirecional = np.array([0.8, 0.8, 0.8])
direcaoLuz = np.array([1, -1, -1])
luzDirecional = LuzDirecional(intensidade=intensidadeDirecional, direcao=direcaoLuz)

# luz spot
pontoSpot   = np.array([50, 100, 10])
direcaoSpot = np.array([0, -1, 1])  # apontando para frente e para baixo
intensidadeSpot = np.array([1, 1, 1])
aberturaSpot = np.pi / 3
luzSpot = LuzSpot(intensidadeSpot, pontoSpot, direcaoSpot, aberturaSpot)

luzes = [luzSpot, luzAmbiente]


cenario = [cone, planoChao, planoFundo]

bg_color = np.array([100, 100, 100], dtype=float) / 255.0

pygame.init()
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("testes fodasticos")
clock = pygame.time.Clock()

image = np.zeros((n_lin, n_col, 3), dtype=float)

# ----------------------------
# MULTIPROCESSAMENTO
# ----------------------------
if __name__ == "__main__":

    num_processos = mp.cpu_count()
    linhas_por_proc = n_lin // num_processos

    tasks = []

    for p in range(num_processos):
        i_start = p * linhas_por_proc
        i_end = n_lin if p == num_processos - 1 else (p + 1) * linhas_por_proc

        tasks.append((
            i_start, i_end,
            n_col, n_lin,
            camera,
            projecao,
            cenario,
            luzes,
            bg_color
        ))

    with mp.Pool(processes=num_processos) as pool:
        resultados = pool.map(render_linhas, tasks)

    # junta os blocos na imagem final
    for i_start, bloco in resultados:
        image[i_start:i_start + bloco.shape[0], :, :] = bloco

    image = (image * 255).astype(np.uint8)
    surface = pygame.surfarray.make_surface(np.flipud(np.rot90(image)))

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # converter coords da janela para coords da imagem
                ix = int(mx / window_w * n_col)
                iy = int(my / window_h * n_lin)

                hit = pick_object(
                    ix, iy,
                    n_col, n_lin,
                    camera,
                    projecao,
                    cenario
                )

                if hit is not None:
                    print("\n=== PICK ===")
                    print("Objeto:", type(hit["obj"]).__name__)
                    print("t:", hit["t"])
                    print("Ponto:", hit["ponto"])
                    print("Normal:", hit["normal"])

                    if "cor" in hit:
                        print("Cor (plano/textura):", hit["cor"])
                else:
                    print("\n=== PICK ===")
                    print("Nenhum objeto selecionado")

        window.blit(pygame.transform.scale(surface, (window_w, window_h)), (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
