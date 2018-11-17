
import sys, pygame
from Player import *
from enemy import *
from GameManager import *
from bazier import *



if __name__ == "__main__":
    pygame.init()

    size = width, height = 1080, 420
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)
    screen.get_height()
    player = Player(10, screen.get_height() - 20)

    clock = pygame.time.get_ticks() + 50
    clock_temp = pygame.time.get_ticks() + 1000

    units.extend([Enemy(10 + unit * 30,20, 1) for unit in range(0, 30)])

    clock_2 = pygame.time.Clock()
    prev_speed = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        current = pygame.time.get_ticks()

        for unit in units:
            unit.move(0, 1)
        if current >= clock:
            clock = current + 20


        """
        current = pygame.time.get_ticks()
        if current >= clock_temp:
            clock_temp = current + 1000
            create_wave()
            """


        player.key_pressed()


        screen.fill(black)
        pygame.draw.rect(screen, pygame.Color(0,0,128), pygame.Rect(player.position.x, player.position.y, 5, 5),
                         5)

        for unit in units:
            # Draw each path
            pygame.draw.rect(screen, pygame.Color(0, 128, 0), pygame.Rect(unit.position.x, unit.position.y, 5, 5), 5)

        for missile in missiles:
            missile.update()
            occured_collision = collision(missile, units)
            pygame.draw.rect(screen, pygame.Color(128, 0, 0), pygame.Rect(missile.position.x, missile.position.y, 3, 3), 3)
            if occured_collision[0]:
                print(occured_collision)
                missiles.remove(missile)
                units.remove(occured_collision[1])



        pygame.display.flip()
        pygame.display.update()
