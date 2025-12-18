import os
import numpy as np
import pygame

FRAME_DIR = "heightmaps"
frames = sorted(f for f in os.listdir(FRAME_DIR) if f.endswith(".npy"))
frame_id = 0

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((480, 360))

def load_frame(i):
    return np.load(os.path.join(FRAME_DIR, frames[i]))

def make_surf(h):
    h = h.T
    rgb = np.zeros((h.shape[0], h.shape[1], 3), dtype=np.uint8)

    terrain = h >= 40
    rgb[terrain] = [30, 100, 30]
    
    water = h <= 40
    rgb[water] = [30, 80, 200]

    sand = water & (h >= 20)
    rgb[sand] = [200, 200, 60]
    
    undermountains = terrain & (h > 160)
    rgb[undermountains] = [90, 130, 89]

    mountains = terrain & (h > 200)
    rgb[mountains] = [171, 148, 126]

    peaks = mountains & (h > 250)
    rgb[peaks] = [205, 211, 213]


    return pygame.surfarray.make_surface(rgb)


clock = pygame.time.Clock()
FPS = 30

current_height = load_frame(0)
surf = make_surf(current_height)

pygame.mixer.music.load("badapple.mp3")
pygame.mixer.music.play()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    current_height = load_frame(frame_id)
    surf = make_surf(current_height)
    screen.blit(surf, (0, 0))
    pygame.display.flip()
    frame_id = (frame_id + 1) % len(frames)