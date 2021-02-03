#!/usr/bin/env python

import pygame
from dataclasses import dataclass

import entity
import systems
import components


@dataclass
class VisibleImage():
    image: pygame.Surface


@dataclass
class Position2D():
    x: float
    y: float


@dataclass
class Speed2D():
    x: float
    y: float


def run():

    image = pygame.image.load('spaceship.png')
    components.add(entity.new(), Position2D(41,41), Speed2D(1,1), VisibleImage(image))
    components.add(entity.new(), Position2D(40,40), VisibleImage(image))

    FPS = 60
    WSIZE = (1024, 768)

    pygame.init()
    window = pygame.display.set_mode(WSIZE)
    pygame.display.set_caption('Example')
    clock = pygame.time.Clock()
    pygame.key.set_repeat(int(1e3/FPS), int(1e3/FPS))

    @systems.register
    def move():
        for _, position, speed in components.single_match(Position2D, Speed2D):
            position.x += speed.x
            position.y += speed.y
            position.x %= WSIZE[0]
            position.y %= WSIZE[1]

    @systems.register
    def render():
        window.fill((0,0,0))
        for _, pos, image in components.single_match(Position2D, VisibleImage):
            window.blit(image.image, (pos.x, pos.y))

        pygame.display.flip()

    timeToDie = False
    while not timeToDie:
       
        systems.run()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                timeToDie = True
            elif event.type == pygame.KEYDOWN:
                try:
                    v = {pygame.K_LEFT: (-0.1, 0),
                         pygame.K_RIGHT: (0.1, 0),
                         pygame.K_UP:   (0, -0.1),
                         pygame.K_DOWN: (0, 0.1)}[event.key]

                    _, speed = list(components.by_entity_and_class(0, Speed2D))[0]
                    speed.x += v[0]
                    speed.y += v[1]
                except KeyError:
                    pass


    pygame.quit()


if __name__ == '__main__':
    run()


# ___oOo___

