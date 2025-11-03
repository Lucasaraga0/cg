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
    
