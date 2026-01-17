import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer Game")
clock = pygame.time.Clock()


forest_bg = pygame.image.load("forest.png").convert()
forest_bg = pygame.transform.scale(forest_bg, (WIDTH, HEIGHT))



def load_animation(folder, name, frame_count, size):
    frames = []
    for i in range(1, frame_count + 1):
        image = pygame.image.load(f"{folder}/{name} ({i}).png").convert_alpha()
        image = pygame.transform.scale(image, size)
        frames.append(image)
    return frames


player_animations = {
    "idle": load_animation("png", "Idle", 10, (50, 50)),
    "run": load_animation("png", "Run", 8, (50, 50)),
    "jump": load_animation("png", "Jump", 12, (50, 50)),
    "hurt": load_animation("png", "Hurt", 8, (50, 50)),
    "dead": load_animation("png", "Dead", 10, (50, 50)),
}

enemy_image = pygame.image.load("png/Run (1).png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (40, 40))



class Player:
    def __init__(self, x, y):
        self.start_pos = (x, y)
        self.rect = pygame.Rect(x, y, 50, 50)

        self.speed = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_strength = 12
        self.on_ground = False

        self.animations = player_animations
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.state][0]
        self.facing_right = True

    def reset(self):
        self.rect.topleft = self.start_pos
        self.vel_y = 0
        self.state = "idle"

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_strength

    def update_animation(self):
        frames = self.animations[self.state]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(frames):
            self.frame_index = 0

        self.image = frames[int(self.frame_index)]

    def move(self, keys, platforms):
        dx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.facing_right = True

        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx > 0:
                    self.rect.right = platform.left
                elif dx < 0:
                    self.rect.left = platform.right

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0


        if not self.on_ground:
            self.state = "jump"
        elif dx != 0:
            self.state = "run"
        else:
            self.state = "idle"

        self.update_animation()

    def draw(self, screen):
        image = self.image
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, self.rect)



class Enemy:
    def __init__(self, x, y, patrol_width=100):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.start_x = x
        self.patrol_width = patrol_width
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x > self.start_x + self.patrol_width:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

    def draw(self, screen):
        screen.blit(enemy_image, self.rect)


class LevelManager:
    def __init__(self):
        self.levels = [
            {
                "platforms": [
                    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
                    pygame.Rect(200, HEIGHT - 120, 150, 20),
                    pygame.Rect(450, HEIGHT - 220, 150, 20),
                ],
                "enemies": [
                    Enemy(230, HEIGHT - 160),
                    Enemy(480, HEIGHT - 260),
                ],
            }
        ]
        self.current_level = 0

    @property
    def platforms(self):
        return self.levels[self.current_level]["platforms"]

    @property
    def enemies(self):
        return self.levels[self.current_level]["enemies"]

    def draw(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, GREEN, platform)



class Game:
    def __init__(self):
        self.player = Player(50, HEIGHT - 70)
        self.level_manager = LevelManager()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.jump()

    def handle_enemy_collisions(self):
        for enemy in self.level_manager.enemies[:]:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.vel_y > 0:
                    self.level_manager.enemies.remove(enemy)
                    self.player.vel_y = -8
                else:
                    self.player.reset()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.level_manager.platforms)

        for enemy in self.level_manager.enemies:
            enemy.update()

        self.handle_enemy_collisions()

    def draw(self):
        screen.blit(forest_bg, (0, 0))

        self.level_manager.draw(screen)

        for enemy in self.level_manager.enemies:
            enemy.draw(screen)

        self.player.draw(screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
