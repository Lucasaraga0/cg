## AP1 CG1 - 2025.2
- Aluno: Lucas Rodrigues Aragão 
A = 5, B = 3, C = 8, D = 3 , E = 9, F = 0
k = (300  + 5 + 3 + 8 + 3 + 9 + 0) % 10 = (328) % 10 = 8

## Questão 1 
- Plano: Se manteve na mesma posição

### Anel cilíndrico:
- Centro da base inicial: (0,0,0)
Centro da base final: (92, 208, 0)

- Raio inicial: 1
Raio final:18

- Altura inicial: $||{C_T - C_B}|| = ||(0,1,0) - (0,0,0)|| = 1$ 
Altura final: 165 

- Centro do topo inicial: (0,1,0)
- Centro do topo final: Centro da base final +altura

Ok, com o aumento do raio e altura, claramente foi aplicada uma matriz de escala $S_{cil}$. Além disso, temos o deslocamento do centro da base, ou seja, uma translação $T_{C_B}$. 

Se a base do cilindro está alinhada com o eixo do chão, o aumento do raio é igual ao aumento nos eixos $x$ e $z$. Como temos que o aumento do raio é de 18 vezes, os valores $s_x$ e $s_z$ são iguais a 18. Além disso temos que o aumento em y vai ser igual ao aumento da altura, nesse caso, $s_y = 165$.  Logo a matriz de escala do anel cilíndrico é dada por 

$$S_{cil} = \begin{bmatrix}
18 & 0 & 0 & 0\\
0 & 165 & 0 & 0\\
0 & 0 & 18 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

Além disso temos a translação da base, que é dada pelo deslocamento $C_{inicial} \rightarrow C_{final} = (92,208, 0)$, já que o ponto original era na origem do sistema de coordenadas. Logo, a matriz de translação do anel cilindrico é dada por:

$$T_{Cil} = \begin{bmatrix}
1 & 0 & 0 & 92\\
0 & 1 & 0 & 208\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

Portante temos, a aplicação da escala seguida da translação do objeto, resultando em:
$$Cil_{Final} = T_{cil} S_{cil}$$


### Esfera
- Centro da esfera inicial: (0,0,0)
Centro da esfera final: (92, 208, 155.5)

- Raio da esfera inicial: 1
Raio da esfera final: 28

Assim como no anel cilindrico, a esfera sofre aplicações de escala e translação.

Iniciando pela translação, por se tratar de um ponto inicial na origem, temos como $t_x, t_y$ e $t_z$, os valores do ponto final, (92, 208, 155.5). Logo a matriz de translação do centro da esfera é:

$$T_{esf} = \begin{bmatrix}
1 & 0 & 0 & 92\\
0 & 1 & 0 & 208\\
0 & 0 & 1 & 155.5\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

A matriz de escala também é bem simples, apenas aplicamos o aumento do raio em todas as direções da esfera. 

$$S_{esf} = \begin{bmatrix}
28 & 0 & 0 & 0\\
0 & 28 & 0 & 0\\
0 & 0 & 28 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

Por fim, a sequência aplicada é dada pela equação:

$$Esf_{final} = T_{esf} S_{esf}$$

### Cone de base aberta

- Centro da base inicial: (0,0,0)
Centro da base final: (208, 92, 0)

- Raio da base inicial: 1
Raio da base final: 38

- Altura inicial: 1
Altura final: 410

Mais uma vez as transformações aplicadas foram de escala e translação. A escala no eixo X e no eixo Z é dada pelo aumento do raio, enquanto a escala do eixo Y é dado pelo aumento da altura. Com isso, a matriz de escala do cone é vista a seguir,

$$S_{cone} = \begin{bmatrix}
38 & 0 & 0 & 0\\
0 & 410 & 0 & 0\\
0 & 0 & 38 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

Enquanto a translação é dada pelo deslocamento do centro da base, (208,92,0). 

$$T_{cone} = \begin{bmatrix}
1 & 0 & 0 & 208\\
0 & 1 & 0 & 92\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

Logo, a sequência aplicada é dada pela equação:

$$Cone_{final} = T_{cone} S_{cone}$$

### Pirâmide de base quadrada

- Centro da base inicial: (0,0,0)
Centro da base final: (208,208, 0)

- Vértice inicial: (0,0,1)

- Comprimento das arestas da base inicial: 1
Comprimento das arestas da base final: 5

- Altura inicial: 1
Altura final: 420

Além disso, a pirâmide é rotacionada em um ângulo $\theta = \pi/5$ em relação ao eixo que passa pelo centro da base e pelo vértice. Esse eixo é o eixo z do sistema de coordenadas. 

Logo, as transformações aplicadas são escala, translação e rotação.

Iniciando pela translação, assim como nos casos anteriores, vamos apenas colocar as coordenadas do vetor de deslocamento, que é dado pelo ponto final, já que o inicial é a origem do sistema de coordenadas. Nisso temos, 

$$T_{pir} = \begin{bmatrix}
1 & 0 & 0 & 208\\
0 & 1 & 0 & 208\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

As escalas aplicadas no eixo X e Y são relativas ao aumento das arestas, enquanto o aumento no eixo Z é o aumento da altura. Por isso temos, 

$$S_{pir} = \begin{bmatrix}
5 & 0 & 0 & 0\\
0 & 5 & 0 & 0\\
0 & 0 & 420 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

Por fim, a matriz de rotação em torno do eixo z é dada pelo ângulo $\theta = \pi/5$,

$$R_z(\pi/5) = \begin{bmatrix}
\cos(\pi/5) & -\sin(\pi/5) & 0 & 0\\
\sin(\pi/5) & \cos(\pi/5) & 0 & 0\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1\\
\end{bmatrix}$$

Inicialmente aumentamos, depois rotacionamos e por fim transladamos o objeto, logo a sequência de operações deve ser dada por:

$$Pir_{final} = T_{pir} R_z(\pi/5) S_{pir}$$

## Questão 2
