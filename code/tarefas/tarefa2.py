import numpy as np
import pygame
import sys
from modules.objects import Esfera, Ray 
from modules.light import LuzPontual
from modules.utils import calcular_iluminacao, normalize

# 1) Defina uma janela através da qual o pintor verá a esfera 
# definir as dimensoes da janela, em metros
Wjanela = 3.0
Hjanela = 3.0
Djanela = 1.0
centro_jan = np.array([0.0, 0.0, -Djanela])
# 2) O olho do pintor está na origem do sistema de coordenadas (0,0,0)
# definir o olho do pintor como origem do sistema de coord
origem = np.array([0.0, 0.0, 0.0])
# 3) O raio da esfera deve ser armazenado na variável rEsfera
# definir o raio da esfera 
r_esfera = 5.0
# 4) O centro da esfera deve estar sobre o eixo z com coordenada z< -(dJanela + rEsfera)
# definir o centro da esfe

centro_esf = np.array([0.0, 0.0, -(Djanela + r_esfera + 0.01)])

#  5) A cor da esfera deve ser esfColor = 255, 0, 0
#  definir a cor da esfera
cor_esf = np.array([255, 0, 0], dtype= float)
bg_color = np.array([100, 100, 100], dtype=float) / 255.0

# 7) Defina o número de colunas nCol e o número de linhas nLin da matriz de cores da imagem.
n_col, n_lin = 200, 200
# definir as dimensoes dos retangulos
dx = Wjanela / n_col
dy = Hjanela / n_lin

# inicializacao da janela 
PIXELS_PER_METER = 200
window_w = int(Wjanela * PIXELS_PER_METER)
window_h = int(Hjanela * PIXELS_PER_METER)

pygame.init()
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Esfera com luz")
clock = pygame.time.Clock()

# grade de pixels 
# cada pixel (x, y) eh convertido para coordenada 3D no plano da janela
x_vals = np.linspace(-Wjanela/2 + dx/2, Wjanela/2 - dx/2, n_col)
y_vals = np.linspace(Hjanela/2 - dy/2, -Hjanela/2 + dy/2, n_lin)
xx, yy = np.meshgrid(x_vals, y_vals)
zz = -Djanela * np.ones_like(xx)

image = np.zeros((n_lin, n_col, 3), dtype=float)


luz = LuzPontual(intensidade=(0.7, 0.7, 0.7), posicao=(0, 0, 0))

esfera = Esfera(centro= centro_esf, raio= r_esfera, cor= cor_esf)

for i in range(n_lin):
    for j in range(n_col):
        dir_ray = np.array([xx[i, j], yy[i, j], zz[i, j]]) - origem
        raio = Ray(origem, dir_ray)
        intersec = esfera.intersect(raio)

        if intersec is not None:
            P = intersec["ponto"]
            normal = intersec["normal"]
            normal /= np.linalg.norm(normal)
            view_dir = -raio.direcao
            view_dir /= np.linalg.norm(view_dir)
            Kd, Ks, m = intersec["Kd"], intersec["Ks"], intersec["m"]
            I = calcular_iluminacao(P, normal, view_dir, luz, Kd, Ks, m)
            color = intersec["cor"]   
            image[i, j] = np.clip(color * I, 0, 1)
        else:
            image[i, j] = bg_color

image = (image * 255).astype(np.uint8)
surface = pygame.surfarray.make_surface(np.flipud(np.rot90(image)))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.blit(pygame.transform.scale(surface, (window_w, window_h)), (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()