import pygame
import time
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
SIZE = 10

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    return updated_cells

def main():
    pygame.init()
    pygame.display.set_caption("Tendi's Game of Life")
    screen = pygame.display.set_mode((80 * SIZE, 60 * SIZE))

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                print(f"Key pressed: {pygame.key.name(event.key)}")
                # Toggle the simulation on spacebar press
                if event.key == pygame.K_SPACE:  
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()

                # Generate a random grid when Enter is pressed
                elif event.key == pygame.K_RETURN:
                    running = False
                    cells = np.random.randint(2, size=(60, 80))
                    update(screen, cells, 10)
                    pygame.display.update()
                    

                # Clear the grid when Backspace is pressed
                elif event.key == pygame.K_BACKSPACE:
                    running = False
                    cells = np.zeros((60, 80))
                    update(screen, cells, 10)
                    pygame.display.update()

            # This checks if the left mouse button is pressed and updates the cells accordingly
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.04)

if __name__ == '__main__':
    main()


