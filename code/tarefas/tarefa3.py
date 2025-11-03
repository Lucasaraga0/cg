import numpy as np
import pygame
import sys
from modules.objects import Esfera,Ray, Plano
from modules.light import LuzPontual, LuzAmbiente
from modules.utils import calcular_iluminacao, cenario_intersect

#dimensoes da janela em cm
Wjanela = 60
Hjanela = 60
DJanela = 30
centro_jan = np.array([0.0, 0.0, -DJanela])

# esfera 
r_esfera = 40
centro_esf = np.array([0,0, -100])
cor_esf = np.array([255, 0, 0], dtype= float)
Kd_esf = Ke_esf = Ka_esf = np.array([0.7, 0.2, 0.2])
m_esf = 10

esfera = Esfera(centro= centro_esf, raio= r_esfera, cor= cor_esf, Kd= Kd_esf, Ks= Ke_esf, Ka= Ka_esf, m = m_esf)

#plano do chao 
pontoChao = np.array([0, -r_esfera, 0])
normalChao = np.array([0,1,0], dtype= float)
corChao = np.array([0, 255, 0], dtype= float)

Kd_chao = Ka_chao = np.array([0.2,0.7,0.2])
Ke_chao = np.array([0,0,0])
m_chao = 1
planoChao = Plano(pontoPi= pontoChao, normalPlano= normalChao, cor= corChao, Kd= Kd_chao, Ks= Ke_chao, Ka= Ka_chao, m = m_chao)

# plano do fundo 
pontoFundo = np.array([0,0,-200])
normalFundo = np.array([0,0,1], dtype= float)
corFundo = np.array([0,0,255])

Kd_fundo = Ka_fundo = np.array([0.3,0.3,0.7])
Ke_fundo = np.array([0,0,0])
m_fundo = 1
planoFundo = Plano(pontoPi= pontoFundo, normalPlano= normalFundo, cor=corFundo, Kd= Kd_fundo, Ks= Ke_fundo, Ka= Ka_fundo, m= m_fundo)

# luz pontual 
intensidadePontual = np.array([0.7,0.7,0.7])
posicaoPontual = np.array([0, 0.6, -0.3])
luzPontual = LuzPontual(intensidade=intensidadePontual, posicao= posicaoPontual)

# luz ambiente
intensidadeAmbiente = np.array([0.3,0.3,0.3])
luzAmbiente = LuzAmbiente(intensidadeAmbiente)

# window
n_col, n_lin = 500,500

dx = Wjanela/n_col
dy = Hjanela/n_lin

PIXELS_PER_CM = 10
window_w = int(Wjanela * PIXELS_PER_CM)
window_h = int(Hjanela * PIXELS_PER_CM)

pygame.init()
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Esfera com planos")
clock = pygame.time.Clock()

# grade de pixels 
# cada pixel (x, y) eh convertido para coordenada 3D no plano da janela
x_vals = np.linspace(-Wjanela/2 + dx/2, Wjanela/2 - dx/2, n_col)
y_vals = np.linspace(Hjanela/2 - dy/2, -Hjanela/2 + dy/2, n_lin)
xx, yy = np.meshgrid(x_vals, y_vals)
zz = -DJanela * np.ones_like(xx)

image = np.zeros((n_lin, n_col, 3), dtype=float)

# iterar sobre os objs e checar qual foi intersectado primeiro 

origem = np.array([0.0, 0.0, 0.0])
bg_color = np.array([100, 100, 100], dtype=float) / 255.0

cenario = [esfera, planoChao, planoFundo]

for i in range(n_lin):
    for j in range(n_col):
        
        dir_ray = np.array([xx[i, j], yy[i, j], zz[i, j]]) - origem
        raio = Ray(origem, dir_ray)
        intersec = cenario_intersect(cenario, raio)

        if intersec is not None:
            #print(i,j)
            P = intersec["ponto"]
            #print(P)
            normal = intersec["normal"]
            normal /= np.linalg.norm(normal)
            view_dir = -raio.direcao
            view_dir /= np.linalg.norm(view_dir)
            Kd, Ks, Ka ,m = intersec["Kd"], intersec["Ks"], intersec["Ka"] ,intersec["m"]
            I = calcular_iluminacao(P, normal, view_dir, luzPontual, Kd, Ks, Ka, luzAmbiente.intensidade ,m)
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