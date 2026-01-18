import numpy as np
from abc import ABC, abstractmethod

class luz(ABC):
    def __init__(self, intensidade):
        """
        intensidade da luz que eh dada por um vetor rgb
        """
        self.intensidade = np.array(intensidade)

    @abstractmethod
    def dir_intensi(self,ponto):
        """
        retorna a direcao e a intensidade da luz dado um ponto no cenario
        """
        pass

class LuzAmbiente(luz):
    def __init__(self, intensidade):
        super().__init__(intensidade)
    def dir_intensi(self, ponto):
        pass
    
class LuzPontual(luz):
    def __init__(self, intensidade, posicao):
        """
        cria uma fonte de luz pontual
        """
        super().__init__(intensidade)
        self.posicao = np.array(posicao)

    def dir_intensi(self, ponto):
        # vetor da luz (do ponto para a fonte)
        l = self.posicao - ponto
        dist = np.linalg.norm(l)
        l = l / dist  # normaliza
        I = self.intensidade

        return l, I

class LuzDirecional(luz):
    def __init__(self, intensidade, direcao):
        """
        cria uma fonte de luz direcional, a luz no infinito
        """     
        super().__init__(intensidade)
        self.direcaoFonte = direcao

    def dir_intensi(self, ponto):
        l = -self.direcaoFonte
        l = l / np.linalg.norm(l)
        return l, self.intensidade
 
class LuzSpot(luz):
    def __init__(self, intensidade, pontoFonte, direcao, theta):
        """
        cria uma fonte de luz spot 
        """
        super().__init__(intensidade)
        self.pontoFonte = pontoFonte
        self.direcaoFonte = direcao/np.linalg.norm(direcao)
        self.theta = theta #abertura da fonte spot
    
    def dir_intensi(self, ponto):
        # iniciar calculando o vetor l 
        L = self.pontoFonte - ponto
        dist = np.linalg.norm(L)
        l = L/dist

        cosAlpha = np.dot(l, -self.direcaoFonte) 
        
        if cosAlpha < np.cos(self.theta):
            return l, np.zeros(3) # regiao nao eh iluminada pela fonte spot
        
        intensidade = self.intensidade * cosAlpha
        return l, intensidade