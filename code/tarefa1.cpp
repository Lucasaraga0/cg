#include <SDL2/SDL.h>
#include <iostream>
#include <vector>

// 1) Defina uma janela através da qual o pintor verá a esfera 
// definir as dimensoes da janela, em metros
const float Wjanela = 3.0f;
const float hJanela = 3.0f;
const float dJanela = 1.0f;
//definir o centro da janela 
const float centroJan[3] = {0.0f,0.0f, -dJanela};

// 2) O olho do pintor está na origem do sistema de coordenadas (0,0,0)
// definir o olho do pintor como origem do sistema de coord
const float origemCoord[3] = {0.0f,0.0f,0.0f};

// 3) O raio da esfera deve ser armazenado na variável rEsfera
// definir o raio da esfera 
const float rEsfera = 5.0f;

// 4) O centro da esfera deve estar sobre o eixo z com coordenada z< -(dJanela + rEsfera)
// definir o centro da esfera 
const float centroEsf[3] = {0,0, -(dJanela + rEsfera + 0.01)};

// 5) A cor da esfera deve ser esfColor = 255, 0, 0
// definir a cor da esfera
const Uint8 corEsf[3] = {255,0,0};
// 6)  A cor de background deve ser cinza bgColor = 100, 100, 100
// definir a cor do background
const Uint8 backGround[3] = {100,100,100};

// 7) Defina o número de colunas nCol e o número de linhas nLin da matriz de cores da imagem.
const int nCol = 200;
const int nLin = 200;

// Definir as dimensoes dos retangulos 

const float dx = Wjanela/nCol;
const float dy = hJanela/nLin;

struct Vec3 {
    float x, y, z;
    Vec3 operator-(const Vec3& b) const { return {x - b.x, y - b.y, z - b.z}; }
    float norm() const { return sqrt(x*x + y*y + z*z); }
    Vec3 normalized() const { float n = norm(); return {x/n, y/n, z/n}; }
    float dot(const Vec3& b) const { return x*b.x + y*b.y + z*b.z; }
};

int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << "Erro ao inicializar SDL: " << SDL_GetError() << std::endl;
        return 1;
    }

    const int PIXELS_PER_METER = 200;
    const int windowW = static_cast<int>(Wjanela * PIXELS_PER_METER);
    const int windowH = static_cast<int>(hJanela * PIXELS_PER_METER);

    SDL_Window* window = SDL_CreateWindow("Esfera",
                                          SDL_WINDOWPOS_CENTERED,
                                          SDL_WINDOWPOS_CENTERED,
                                          windowW, windowH,
                                          SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    // --- Canvas ---
    std::vector<std::vector<SDL_Color>> canvas(nLin, std::vector<SDL_Color>(nCol));
    
    Vec3 O = {0.0f, 0.0f, 0.0f};
    Vec3 C = {centroEsf[0], centroEsf[1], centroEsf[2]};

    for (int i = 0; i < nLin; ++i) {
        for (int j = 0; j < nCol; ++j) {
            // ponto no plano da janela
            float x = -Wjanela/2 + (j + 0.5f) * dx;
            float y =  hJanela/2 - (i + 0.5f) * dy;
            float z = -dJanela;

            Vec3 P = {x, y, z};
            Vec3 d = (P - O).normalized();

            // calcular o ponto da janela 
            Vec3 OC = O - C;
            float a = d.dot(d);
            float b = 2.0f * d.dot(OC);
            float c = OC.dot(OC) - rEsfera*rEsfera;
            float delta = b*b - 4*a*c;

            if (delta >= 0) {
                // Interseção existe
                canvas[i][j] = SDL_Color{corEsf[0], corEsf[1], corEsf[2], 255};
            } else {
                // Sem interseção -> background
                canvas[i][j] = SDL_Color{backGround[0], backGround[1], backGround[2], 255};
            }
        }
    }

    // renderizacao
    bool running = true;
    SDL_Event ev;
    const int cellW = windowW / nCol;
    const int cellH = windowH / nLin;

    while (running) {
        while (SDL_PollEvent(&ev)) {
            if (ev.type == SDL_QUIT) running = false;
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        for (int i = 0; i < nLin; ++i) {
            for (int j = 0; j < nCol; ++j) {
                SDL_Rect rect;
                rect.x = j * cellW;
                rect.y = i * cellH;
                rect.w = cellW;
                rect.h = cellH;

                SDL_Color c = canvas[i][j];
                SDL_SetRenderDrawColor(renderer, c.r, c.g, c.b, c.a);
                SDL_RenderFillRect(renderer, &rect);
            }
        }

        SDL_RenderPresent(renderer);
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
