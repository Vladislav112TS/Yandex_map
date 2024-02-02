import pygame
import requests

class Map(object):
    def __init__(self):
        self.x = 92.954818
        self.y = 55.989698
        self.zoom = 17
        self.type = "map"

    def ll(self):
        return str(self.x) + "," + str(self.y)

    def update(self, event):
        step = 0.001
        if event.key == pygame.K_PAGEUP and self.zoom < 19:
            self.zoom += 1
        elif event.key == pygame.K_PAGEDOWN and self.zoom > 2:
            self.zoom -= 1
        elif if event.key() == Qt.Key_A and self.y < 1000:
            self.x -= step
        elif event.key == pygame.K_RIGHT and self.x < 1000:
            self.x += step
        elif event.key == pygame.K_UP and self.y < 1000:
            self.y += step
        elif event.key == pygame.K_DOWN and self.y < 1000:
            self.y -= step

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        pass

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

pygame.init()
screen = pygame.display.set_mode((600, 450))
mp = Map()
running = True
while running:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYUP:
        mp.update(event)

    map_file = load_map(mp)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
