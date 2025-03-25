import pygame, random, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]

        self.original_image = pygame.image.load('levels/memory_game_fonts/' + filename)

        self.back_image = pygame.image.load('levels/memory_game_fonts/' + filename)

        pygame.draw.rect(self.back_image, WHITE, self.back_image.get_rect())

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft = (x, y))
        self.shown = False # Должно быть False

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False


class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False
        self.game_completed = False

        # bakery_products
        self.all_bakery_products = [f for f in os.listdir('levels/memory_game_fonts') if os.path.join('levels/memory_game_fonts', f)]

        self.img_width, self.img_height = (128, 128)
        self.padding = 20 # Было 20
        self.margin_top = 170
        self.cols = 10
        self.rows = 5
        self.width = 1920

        self.tiles_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level()


    def update(self, event_list):
        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if self.game_completed and event.type == pygame.KEYDOWN:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.level += 1
                        if self.level >= 11:
                            self.level = 1
                        self.generate_level()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []


    def generate_level(self):
        self.bakery_products = self.select_random_bakery_products()
        self.level_complete = False
        self.rows = self.level
        self.cols = 4
        self.generate_tileset(self.bakery_products)

    def generate_tileset(self, bakery_products):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        self.tiles_group.empty()

        for i in range(len(bakery_products)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(bakery_products[i], x, y)
            self.tiles_group.add(tile)


    def select_random_bakery_products(self):
        bakery_products = random.sample(self.all_bakery_products, (self.level + self.level + 2))
        if self.level == 10:
            bakery_products = random.sample(self.all_bakery_products, (self.level + self.level + 5))
        bakery_products_copy = bakery_products.copy()
        bakery_products.extend(bakery_products_copy)
        random.shuffle(bakery_products)
        return bakery_products

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and self.game_completed:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 10:
                        self.game_completed = True
                    self.generate_level()


    def draw(self):
        screen.fill(BLACK)

        # fonts
        title_font = pygame.font.Font('assets/fonts/Persimmona.ttf', 44)
        content_font = pygame.font.Font('assets/fonts/Persimmona.ttf', 24)

        # text
        title_text = title_font.render('Cucumber Game', True, WHITE)
        title_rect = title_text.get_rect(midtop = (WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Level ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop = (WINDOW_WIDTH // 2, 80))

        info_text = content_font.render('Find 2 of each', True, WHITE)
        info_rect = info_text.get_rect(midtop = (WINDOW_WIDTH // 2, 120))

        if self.level == 10 and self.level_complete:
            next_text = content_font.render('Congrats. You Won. Press Any key to continue.', True, WHITE)
            self.game_completed = True
        else:
            next_text = content_font.render('Level complete. Press Space for next level', True, WHITE)
        next_rect = next_text.get_rect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete:
            screen.blit(next_text, next_rect)

pygame.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory Game')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

game = Game()

def main():
    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        game.update(event_list)

        pygame.display.update()
        clock.tick(FPS)


    pygame.quit()

if __name__ == '__main__':
    main()