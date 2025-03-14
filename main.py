import pygame
from levels import Level1, Level2, Level3, Level4, Level5, Level6, Epilogue, Prologue


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Persimona's investigation")

    levels = [Prologue(), Level1(), Level2(), Level3(), Level4(), Level5(), Level6(), Epilogue()]
    current_level_index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            levels[current_level_index].handle_event(event)

        current_level = levels[current_level_index]
        current_level.run(screen)

        if current_level.is_completed():
            current_level_index += 1
            if current_level_index >= len(levels):
                running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
