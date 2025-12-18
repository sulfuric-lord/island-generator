import pygame
import random
import numpy as np

SCREEN_W, SCREEN_H = 900, 700
NUMBER_OF_MATRIXES = 4

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

def build_kernel(r):
    sigma = r / 3
    ax = np.arange(-r, r + 1)
    xx, yy = np.meshgrid(ax, ax)
    return np.exp(-((xx * xx + yy * yy) / (2 * sigma * sigma)))

def generate_complex_matrix(SCREEN_W, SCREEN_H, w, numseeds, numseeds_minus, r_inc):
    radii = [(i + 1) * r_inc for i in range(4)]
    matrix_list = []

    for i in range(4):
        r = radii[i]
        m = np.zeros((SCREEN_W, SCREEN_H), dtype=np.float32)
        seeds = [(random.randint(0, SCREEN_W - 1), random.randint(0, SCREEN_H - 1)) for _ in range(numseeds)]
        
        for x, y in seeds:
            m[x, y] = 1

        kernel = build_kernel(r)

        for sx, sy in seeds:
            x1 = max(0, sx - r)
            y1 = max(0, sy - r)
            x2 = min(SCREEN_W, sx + r + 1)
            y2 = min(SCREEN_H, sy + r + 1)

            kx1 = x1 - (sx - r)
            ky1 = y1 - (sy - r)
            kx2 = kx1 + (x2 - x1)
            ky2 = ky1 + (y2 - y1)

            m[x1:x2, y1:y2] += kernel[kx1:kx2, ky1:ky2]

        m -= m.min()
        m /= m.max()

        for x, y in seeds:
            m[x, y] = m[x + 1 if x < SCREEN_W - 1 else x - 1, y]

        matrix_list.append(m)
        numseeds -= numseeds_minus

    res = (
        matrix_list[0] * w[3] +
        matrix_list[1] * w[2] +
        matrix_list[2] * w[1] +
        matrix_list[3] * w[0]
    )

    return (res / res.max()) ** 0.8

def make_surf(res):
    rgb = np.zeros((SCREEN_W, SCREEN_H, 3), dtype=np.uint8)

    terrain = res > 0.55

    rgb[terrain, 1] = 100

    mountains = res > 0.85
    under_mountain = res > 0.75
    peaks = res > 0.95
    rgb[under_mountain, 0] = 90
    rgb[under_mountain, 1] = 130
    rgb[under_mountain, 2] = 89

    rgb[mountains, 0] = 171
    rgb[mountains, 1] = 148
    rgb[mountains, 2] = 126

    rgb[peaks, 0] = 205
    rgb[peaks, 1] = 211
    rgb[peaks, 2] = 213

    sand = terrain & (res < 0.60)
    rgb[sand, 0] = 250
    rgb[sand, 1] = 216
    rgb[sand, 2] = 174

    # rgb[heat_mask, 0] = 255
    # rgb[heat_mask, 1] = 0
    # rgb[heat_mask, 2] = 0

    rgb[~terrain, 2] = 150 


    return pygame.surfarray.make_surface(rgb)

def make_bw(matrix):
    img = (matrix * 255).astype(np.uint8)
    rgb = np.dstack([img, img, img])
    surf = pygame.surfarray.make_surface(rgb)
    return surf

matrix = generate_complex_matrix(SCREEN_W, SCREEN_H, [0.9, 0.4, 0.2, 0.05], 1500, 400, 35)
surf = make_surf(matrix)
bw_surf = make_bw(matrix)

show = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                matrix = generate_complex_matrix(SCREEN_W, SCREEN_H, [0.9, 0.4, 0.2, 0.05], 1500, 400, 35)
                surf = make_surf(matrix)
                bw_surf = make_bw(matrix)
            elif event.key == pygame.K_1:
                if show >= 1:
                    show = 0
                else:
                    show += 1
            elif event.key == pygame.K_2:
                if show is not 2:
                    show = 2
                else:
                    show = 1
    if show == 0:
        screen.blit(bw_surf, (0, 0))
    elif show == 1:
        screen.blit(surf, (0, 0))
    elif show == 1:
        screen.blit(surf, (0, 0))
    pygame.display.update()