import pygame
import numpy as np

from modules.transformations import translate, rotateX, rotateY, rotateZ, rotateArb, scale
from modules.camera import Projecao

import numpy as np

def menu_camera(camera):
    """
    Menu interativo para alterar parâmetros da câmera.
    Só retorna needs_render=True quando sair com alterações feitas.
    """

    changed = False

    while True:

        print("\n==============================")
        print(" MENU DA CAMERA")
        print("==============================")

        print("Eye (posicao):", camera.posicao)
        print("At  (alvo)   :", camera.AtPoint)
        print("Up           :", camera.UpPoint)

        print("\n1 - Alterar Eye")
        print("2 - Alterar At")
        print("3 - Alterar Up")
        print("4 - Reset basis (recalcular u,v,w)")
        print("0 - Sair")

        op = input("Escolha: ")

        # sair
        if op == "0":
            if changed:
                camera.update_basis()
            return camera, changed

        # Eye completo
        elif op == "1":
            x = float(input("Eye X: "))
            y = float(input("Eye Y: "))
            z = float(input("Eye Z: "))
            camera.posicao = np.array([x, y, z])
            changed = True

        # At completo
        elif op == "2":
            x = float(input("At X: "))
            y = float(input("At Y: "))
            z = float(input("At Z: "))
            camera.AtPoint = np.array([x, y, z])
            changed = True

        # Up completo
        elif op == "3":
            x = float(input("Up X: "))
            y = float(input("Up Y: "))
            z = float(input("Up Z: "))
            camera.UpPoint = np.array([x, y, z])
            changed = True

        # recalcular base manualmente
        elif op == "4":
            camera.update_basis()
            changed = True


def menu_projecao(projecao):
    """
    Menu simples para alterar parâmetros da projeção.
    Retorna (projecao, needs_render)
    """

    while True:

        print("\n==============================")
        print(" MENU DE PROJECAO")
        print("==============================")

        modo = "Ortografica" if projecao.ortho else "Perspectiva"
        print("Modo atual:", modo)

        if not projecao.ortho:
            print("FOV:", np.rad2deg(projecao.fov))
            print("Focal:", projecao.focal)
        else:
            print("Largura ortho:", projecao.w * 2)
            print("Altura ortho :", projecao.h * 2)

        print("\n1 - Alterar FOV")
        print("2 - Alterar distancia focal")
        print("3 - Trocar para Ortografica")
        print("4 - Trocar para Perspectiva")
        print("5 - Alterar tamanho ortografico")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "0":
            return projecao, False

        elif op == "1":
            if projecao.ortho:
                continue
            grau = float(input("Novo FOV (graus): "))
            projecao.set_fov(np.deg2rad(grau))
            return projecao, True

        elif op == "2":
            if projecao.ortho:
                continue
            focal = float(input("Nova focal: "))
            if focal > 0:
                projecao.focal = focal
                return projecao, True

        elif op == "3":
            projecao.set_ortho(True)
            return projecao, True

        elif op == "4":
            projecao.set_ortho(False)
            return projecao, True

        elif op == "5":
            if not projecao.ortho:
                continue
            largura = float(input("Nova largura: "))
            altura  = float(input("Nova altura: "))
            projecao.w = largura / 2
            projecao.h = altura / 2
            return projecao, True


class EditorController:
    def __init__(self, cenario):
        self.cenario = cenario
        self.selected_obj = None
        self.mode = None
        self.needs_render = True

    def select_object(self, hit):
        if hit is None:
            self.selected_obj = None
            print("Nenhum objeto selecionado.")
        else:
            self.selected_obj = hit["obj"]
            print("Selecionado:", type(self.selected_obj).__name__)

    def delete_selected(self):
        if self.selected_obj in self.cenario:
            self.cenario.remove(self.selected_obj)

        self.selected_obj = None
        self.needs_render = True

    def apply_translate(self):
        dx = float(input("dx: "))
        dy = float(input("dy: "))
        dz = float(input("dz: "))

        T = translate([0, 0, 0], [dx, dy, dz])
        self.selected_obj.translateObject(T)

        print("Translação aplicada.")
        self.needs_render = True

    def apply_scale(self):
        sx = float(input("sx: "))
        sy = float(input("sy: "))
        sz = float(input("sz: "))

        S = scale([sx, sy, sz])
        self.selected_obj.scaleObject(S)

        print("Escala aplicada.")
        self.needs_render = True

    def apply_rotation(self):
        ang = float(input("Ângulo em graus: "))
        ang = np.radians(ang)

        axis = input("Eixo (x/y/z) ou (a = arbitrário): ").lower()

        if axis == "x":
            R = rotateX(ang)

        elif axis == "y":
            R = rotateY(ang)

        elif axis == "z":
            R = rotateZ(ang)

        elif axis == "a":
            print("\n--- Rotação Arbitrária ---")

            x0 = float(input("P0.x: "))
            y0 = float(input("P0.y: "))
            z0 = float(input("P0.z: "))

            x1 = float(input("P1.x: "))
            y1 = float(input("P1.y: "))
            z1 = float(input("P1.z: "))

            P0 = [x0, y0, z0]
            P1 = [x1, y1, z1]

            R = rotateArb(ang, P0, P1)

        else:
            print("Eixo inválido. Use x, y, z ou a.")
            return

        self.selected_obj.rotateObject(R)

        print("Rotação aplicada com sucesso.")
        self.needs_render = True

    def handle_key(self, key):
        if self.selected_obj is None:
            return

        if key == pygame.K_g:
            self.apply_translate()

        elif key == pygame.K_s:
            self.apply_scale()

        elif key == pygame.K_r:
            self.apply_rotation()
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            self.delete_selected()

    def draw_overlay(self, screen):
        font = pygame.font.SysFont("Arial", 18)

        # Painel
        pygame.draw.rect(screen, (30, 30, 30), (10, 10, 260, 120))
        pygame.draw.rect(screen, (200, 200, 200), (10, 10, 260, 120), 2)

        # Texto
        if self.selected_obj is None:
            txt = "Nenhum objeto selecionado"
        else:
            txt = f"Selecionado: {type(self.selected_obj).__name__}"

        screen.blit(font.render(txt, True, (255, 255, 255)), (20, 20))
        screen.blit(font.render("G = mover", True, (200, 200, 200)), (20, 50))
        screen.blit(font.render("R = rotacionar", True, (200, 200, 200)), (20, 70))
        screen.blit(font.render("S = escala", True, (200, 200, 200)), (20, 90))
        screen.blit(font.render("DEL = remover", True, (200, 200, 200)), (20, 110))
