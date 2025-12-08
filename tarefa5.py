import numpy as np
import pygame
import sys
from modules.objects import Esfera, Ray, Plano, Cilindro, Cone
from modules.light import LuzPontual, LuzAmbiente
from modules.utils import calcular_iluminacao, cenario_intersect

# plano chao
p_PiChao = np.array([0,-150,0])
normalChao = np.array([0,1,0])
#TODO: Colocar cor, textura de madeira e coeficente m 
planoChao = Plano(pontoPi= p_PiChao, normalPlano= normalChao)

#plano parede direita
P_PiDir = np.array([200,-150,0])
normalDir = np.array([0,0,1])
KdDir = KeDir = KaDir = np.array([0,686,0.933, 0.933])
#TODO: Colocar cor e coeficente m 

#TODO: Fazer planos restantes
# plano parede esquerda
# plano parede frontal
# plano teto

#TODO: Fazer cilindro, cone e cubo

#esfera: 
centroEsf = np.array([0,95, -200])
rEsf = 5
kdEsf = KeEsf = KaEsf = np.array([0.854, 0.647, 0.125])
corEsf = np.array([0,0,255])
esfera = Esfera(centro= centroEsf, raio = rEsf, cor = corEsf, Kd= kdEsf, Ks= KeDir, Ka= KaDir)