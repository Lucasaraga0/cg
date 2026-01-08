import numpy as np

def translate(PInicial, PFinal):
    """retorna a matriz de translacao da transformacao"""
    deltaX = PFinal[0] - PInicial[0]
    deltaY = PFinal[1] - PInicial[1]
    deltaZ = PFinal[2] - PInicial[2]

    matrizT = np.eye(n = 4)
    matrizT[0][3] = deltaX
    matrizT[1][3] = deltaY
    matrizT[2][3] = deltaZ
    
    return matrizT

def scale(scale):
    """retorna a matriz de escala"""
    scaleX = scale[0]
    scaleY = scale[1]
    scaleZ = scale[2]

    matrizS = np.eye(n = 4)
    matrizS[0][0] = scaleX
    matrizS[1][1] = scaleY
    matrizS[2][2] = scaleZ

    return matrizS

def rotateX(thetaX):
    """retorna a matriz de rotacao baseada no angulo thetaX"""
    cos = np.cos(thetaX)
    sin = np.sin(thetaX)

    matrizRot = np.eye(n = 4)
    matrizRot[1][1] = cos
    matrizRot[1][2] = - sin
    matrizRot[2][1] = sin
    matrizRot[2][2] = cos

    return matrizRot

def rotateY(thetaY):
    """retorna a matriz de rotacao baseada no angulo thetaY"""

    cos = np.cos(thetaY)
    sin = np.sin(thetaY)

    matrizRot = np.eye(n = 4)
    matrizRot[0][0] = cos
    matrizRot[0][2] = sin
    matrizRot[2][0] = - sin
    matrizRot[2][2] = cos

    return matrizRot

def rotateZ(thetaZ):
    """retorna a matriz de rotacao baseada no angulo thetaZ"""

    cos = np.cos(thetaZ)
    sin = np.sin(thetaZ)

    matrizRot = np.eye(n = 4)
    matrizRot[0][0] = cos
    matrizRot[0][1] = -sin
    matrizRot[1][0] = sin
    matrizRot[1][1] = cos

    return matrizRot

def rotateArb():
    """retorna a matriz de rotacao em torno de um eixo arbitrario"""
    #TODO
    pass

def shear(gamma1, gamma2= None, plano = "xy", eixo = "y"):
    """retorna a matriz de cisalhamento

    cisalhamento de um plano (str) em relacao a um eixo (str)
    """
    # TODO: plano yz e xz em relacao a eixos arbitrarios
    tan1 = np.tg(gamma1)
    tan2 = np.tg(gamma2)

    matrizC = np.eye(n = 4)

    if plano == "xz":
        if eixo == "x":
            matrizC[0][3] = tan1
        elif eixo == "y":
            matrizC[1][0] = tan1
        else:
        # em relacao a um eixo arbitrario
            matrizC[0][2] = tan1 #tan(gammaX)
            matrizC[1][2] = tan2 #tan(gammaY) 

    elif plano == "xz":
        if eixo == "x":
            matrizC[0][2] = tan1
        elif eixo == "z":
            matrizC[2][0] = tan1
        else:
            pass

    elif plano == "yz":
        if eixo == "y":
            matrizC[1][2] = tan1
        elif eixo == "z":
            matrizC[2][1] = tan1
        else:
            pass
    
    return matrizC

def reflect():
    #TODO
    pass