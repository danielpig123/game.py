import pygame
import random
import os

def main():
    pygame.init()

    FPS = 60
    WIDTH, HEIGHT = 500, 600
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("荒野亂鬥")
    clock = pygame.time.Clock()

    background_png = pygame.image.load("background.png").convert()
    bullet_png = pygame.image.load("bullet.png").convert()
    player_png = pygame.image.load("player.png").convert()
    rock_pngs = [pygame.image.load(f"rock{i}.png").convert() for i in range(6)]
    font_name = "font.ttf"

    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    def draw_health(surf, health, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(health, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

    def draw_init():
        screen.blit(background_png, (0, 0))
        draw_text(screen, "太空生存戰", 50, WIDTH * 1/4, HEIGHT / 4)
        draw_text(screen, "A D 移動飛船 空白鍵發射子彈", 25, WIDTH * 1/5, HEIGHT / 2)
        draw_text(screen, "按任意鍵開始遊戲", 25, WIDTH * 3/10, HEIGHT * 3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYUP:
                    waiting = False

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(player_png, (50, 28))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = 24
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 8

        def update(self):
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_d]:
                self.rect.x += self.speedx
            if key_pressed[pygame.K_a]:
                self.rect.x -= self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    class Rock(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image_ori = random.choice(rock_pngs)
            self.image = self.image_ori.copy()
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * 0.9 / 2)
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-60, -40)
            self.speedx = random.randrange(-1, 1)
            self.speedy = random.randrange(3, 10)
            self.total_degree = 0
            self.rot_degree = random.randrange(-3, 5)

        def rotate(self):
            self.total_degree += self.rot_degree
            self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center

        def update(self):
            self.rotate()
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
                self.__init__()

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = bullet_png
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    show_init = True
    running = True
    while running:
        if show_init:
            draw_init()
            show_init = False
            all_sprites = pygame.sprite.Group()
            rocks = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for _ in range(8):
                r = Rock()
                all_sprites.add(r)
                rocks.add(r)
            score = 0
            health = 100

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
        for hit in hits:
            score += hit.radius
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)

        hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
        for hit in hits:
            r = Rock()
            all_sprites.add(r)
            rocks.add(r)
            health -= hit.radius
            if health <= 0:
                show_init = True

        screen.fill(BLACK)
        screen.blit(background_png, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, "SCORE: " + str(score), 30, 100, -10)
        draw_health(screen, "HP: " + str(health), 30, 310, -10)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
