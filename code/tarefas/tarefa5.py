import numpy as np
import pygame
import sys
from modules.objects import Esfera, Ray, Plano, Cilindro, Cone
from modules.complexObjects import Cubo
from modules.light import LuzPontual, LuzAmbiente
from modules.utils import calcular_iluminacao, cenario_intersect

# fatores comuns nos planos laterais
KdLat = KeLat = KaLat = np.array([0.686, 0.933, 0.933])
corLat = np.array([255,255,255])
mLat = 10

# plano chao
p_PiChao = np.array([0,-150,0])
normalChao = np.array([0,1,0])
#TODO: Colocar cor, textura de madeira e coeficente m 
#planoChao = Plano(pontoPi= p_PiChao, normalPlano= normalChao)

#plano parede direita
P_PiDir = np.array([200,-150,0])
normalDir = np.array([0,0,1])
planoDir = Plano(pontoPi=P_PiDir, normalPlano= normalDir, cor= corLat, Kd= KdLat, Ks= KeLat, Ka= KaLat, m= mLat)

# plano parede esquerda
P_PiEsq = np.array([-200,-150,0])
normalEsq = np.array([1,0,0])
planoEsq = Plano(pontoPi=P_PiEsq, normalPlano= normalEsq, cor= corLat, Kd= KdLat, Ks= KeLat, Ka= KaLat, m= mLat)

# plano parede frontal
P_PiFront = np.array([200,-150,-400])
normalFront = np.array([0,0,1])
planoFront = Plano(pontoPi= P_PiFront, normalPlano= normalFront, cor= corLat, Kd= KdLat, Ks=KeLat, Ka=KaLat, m= mLat)

# plano teto
P_PiTeto = np.array([0,150,0])
normalTeto = np.array([0,-1,0])
KdTeto, KeTeto, KaTeto = np.array([0.933,0.933,0.933])
corTeto = np.array([0,0,0])
mTeto = 10
planoTeto = Plano(pontoPi=P_PiTeto, normalPlano= normalTeto, cor= corTeto, Kd= KdTeto, Ks=KeTeto, Ka=KaTeto, m= mTeto)

# cilindro 
centroBaseCil = np.array([0,-60,-200])
raioCil = 5
HCil = 90
dCil = np.array([0.,1.,0.])
KdCil = KeCil =  KaCil = np.array([0.824, 0.706, 0.549])
corCil = np.array([255,0,0])
cilindro = Cilindro(centroBase= centroBaseCil,raioBase= raioCil, altura= HCil, vetorDir= dCil, cor= corCil, Kd= KdCil, Ks= KeCil, Ka= KaCil, m = 2)

# cone 
centroBaseCone = np.array([0,-60,-200])
raioCone = 90
HCone = 150
dCone = np.array([0,1,0]) 
KdCone = KeCone = KaCone = np.array([0,1,0.498])
corCone = np.array([255,255,0])
cone = Cone(centroBase=centroBaseCone, raioBase= raioCone, altura= HCone, vetorDir= dCone, cor= corCone,Kd= KdCone,Ks=KeCone ,Ka= KaCone, m = 3)

#cubo
arestaCubo = 40
centroBaseCubo = np.array([0,-150,-165])
ux = np.array([1,0,0])
uy = np.array([0,1,0])
uz = np.array([0,0,1]) 
KdCubo = KeCubo = KaCubo = np.array([0,1,0.498])
cubo = Cubo(tamAresta=arestaCubo, centro_base = centroBaseCubo, ux= ux, uy= uy, uz= uz, cor = corCone , Kd= KdCubo, Ks = KeCubo, Ka= KaCubo, m = 10)

#esfera
centroEsf = np.array([0,95, -200])
raioEsf = 5
kdEsf = KeEsf = KaEsf = np.array([0.854, 0.647, 0.125])
corEsf = np.array([0,0,255])
esfera = Esfera(centro= centroEsf, raio = raioEsf, cor = corEsf, Kd= kdEsf, Ks= KeEsf, Ka= KaEsf)

# luz pontual 
intensidadePontual = np.array([0.7,0.7,0.7])
pFonte = np.array([-100,140,-20])
luzPontual = LuzPontual(intensidade= intensidadePontual, posicao= pFonte)

# luz ambiente
intensidadeAmbiente = np.array([0.3,0.3,0.3])
luzAmbiente = LuzAmbiente(intensidadeAmbiente)

# window
Wjanela = 60
Hjanela = 60
DJanela = 30
centro_jan = np.array([0.0, 0.0, -DJanela])


n_col, n_lin = 500,500

dx = Wjanela/n_col
dy = Hjanela/n_lin

PIXELS_PER_CM = 10
window_w = int(Wjanela * PIXELS_PER_CM)
window_h = int(Hjanela * PIXELS_PER_CM)

pygame.init()
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Cena com cubo")
clock = pygame.time.Clock()

# grade de pixels 
# cada pixel (x, y) eh convertido para coordenada 3D no plano da janela
x_vals = np.linspace(-Wjanela/2 + dx/2, Wjanela/2 - dx/2, n_col)
y_vals = np.linspace(Hjanela/2 - dy/2, -Hjanela/2 + dy/2, n_lin)
xx, yy = np.meshgrid(x_vals, y_vals)
zz = -DJanela * np.ones_like(xx)

image = np.zeros((n_lin, n_col, 3), dtype=float)

origem = np.array([0.0, 0.0, 0.0])
bg_color = np.array([100, 100, 100], dtype=float) / 255.0

cenario = [planoDir, planoEsq, planoFront, cilindro, cone, esfera, cubo]

for i in range(n_lin):
    for j in range(n_col):
        
        dir_ray = np.array([xx[i, j], yy[i, j], zz[i, j]]) - origem
        raio = Ray(origem, dir_ray)
        intersec = cenario_intersect(cenario, raio)

        if intersec is not None:
            P = intersec["ponto"]
            normal = intersec["normal"] / np.linalg.norm(intersec["normal"])
            view_dir = -raio.direcao / np.linalg.norm(raio.direcao)
            obj_intersec = intersec["obj"]
            Kd, Ks, Ka, m = obj_intersec.Kd, obj_intersec.Ks, obj_intersec.Ka, obj_intersec.m

            I = calcular_iluminacao(
                P, normal, view_dir,
                luzPontual, Kd, Ks, Ka,
                luzAmbiente.intensidade, m,
                cenario, obj_intersec 
            )

            color = obj_intersec.cor
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