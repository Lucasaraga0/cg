import numpy as np
import pygame
import sys
import multiprocessing as mp

from modules.objetosProntos import criar_quarto, criar_arvore_natal, criar_puff, criar_snowman
from modules.transformations import translate, scale, rotateX
from modules.camera import Camera, ProjecaoPerspectiva   
from modules.picking import pick_object
from modules.objects import load_texture
from modules.light import LuzPontual, LuzAmbiente, LuzDirecional, LuzSpot
from modules.utils import render_linhas

# ----------------------------
# Dimensões da janela em cm
# ----------------------------
Wjanela = 60
Hjanela = 60

n_col, n_lin = 500, 500

PIXELS_PER_CM = 10
window_w = int(Wjanela * PIXELS_PER_CM)
window_h = int(Hjanela * PIXELS_PER_CM)

# ----------------------------
# CAMERA (perto da parede da frente, olhando para o fundo)
# ----------------------------
# Quarto: W=300, H=200, D=300
camera_pos = np.array([150.0, 100.0, 290.0])   # quase na parede da frente
camera_at  = np.array([150.0, 80.0, 50.0])     # olhando para dentro do quarto
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
# TEXTURAS E QUARTO
# ----------------------------
texturaChao = load_texture("../textures/grass.jpg")
texturaParede = load_texture("../textures/brick_wall.jpg")

# quarto com texturas
quarto = criar_quarto(
    W=300, H=200, D=300,
    textura_paredes=texturaParede,
    textura_chao=texturaChao,
)

# ----------------------------
# OBJETOS DO CENÁRIO
# ----------------------------
base_puff = np.array([220.0, 0.0, 90.0])

base_snowman = np.array([
    base_puff[0],          
    30.0,           
    base_puff[2]          
])


arvore = (criar_arvore_natal())   
#puff = criar_puff(base_pos= base_puff)
snow_men = criar_snowman(base_pos= base_snowman)

cenario = [quarto, arvore, snow_men]
cenarioObjs = []
for bigObj in cenario:
    for obj in bigObj:
        #print(type(obj))
        cenarioObjs.append(obj)

#print("fim")

# ----------------------------
# LUZES (coerentes com o quarto)
# ----------------------------

# luz ambiente
intensidadeAmbiente = np.array([0.6, 0.6, 0.6])
luzAmbiente = LuzAmbiente(intensidadeAmbiente)

# luz pontual no teto, mais para o centro
posicaoPontual = np.array([150, 180, 150])
intensidadePontual = np.array([0.6, 0.6, 0.6])
luzPontual = LuzPontual(intensidade=intensidadePontual, posicao=posicaoPontual)

# luz direcional suave
intensidadeDirecional = np.array([0.4, 0.4, 0.4])
direcaoLuz = np.array([-1, -2, -1])  # vindo de cima e do fundo
luzDirecional = LuzDirecional(intensidade=intensidadeDirecional, direcao=direcaoLuz)

# luz spot apontando para o snowman + puff
pontoSpot   = np.array([200, 180, 200])
direcaoSpot = np.array([-0.3, -1.0, -0.7])  # para baixo e para o fundo
intensidadeSpot = np.array([1.0, 1.0, 1.0])
aberturaSpot = np.pi / 4
luzSpot = LuzSpot(intensidadeSpot, pontoSpot, direcaoSpot, aberturaSpot)

luzes = [luzAmbiente, luzPontual, luzSpot]

bg_color = np.array([100, 100, 100], dtype=float) / 255.0

# ----------------------------
# PYGAME
# ----------------------------

pygame.init()
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Natal do snow man'")
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
            cenarioObjs,
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
                    cenarioObjs
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
