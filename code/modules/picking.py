# modules/picking.py

def pick_object(mx, my, nx, ny, camera, projecao, cenario):
    """
    mx, my   -> pixel clicado (em coords da imagem, não da janela)
    nx, ny   -> resolução da imagem (n_col, n_lin)
    camera   -> instância de Camera
    projecao -> ProjecaoPerspectiva ou ProjecaoOrtografica
    cenario  -> lista de objetos
    """

    # gera raio passando exatamente pelo pixel clicado
    raio = projecao.generate_ray(camera, mx, my, nx, ny)

    t_min = float("inf")
    hit = None

    for obj in cenario:
        intersec = obj.intersect(raio)

        if intersec is None:
            continue

        t = intersec["t"]

        # só aceita interseções na frente da câmera
        if t > 1e-6 and t < t_min:
            t_min = t
            hit = intersec

    # hit já é exatamente no formato que você usa no render:
    # {
    #   "t": ...,
    #   "ponto": ...,
    #   "normal": ...,
    #   "obj": ...
    #   ("cor" no caso do plano)
    # }

    return hit
