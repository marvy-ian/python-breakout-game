import math
import random
import sys
import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

PADDLE_W, PADDLE_H = 100, 14
PADDLE_SPEED = 9
BALL_RADIUS = 8
BASE_BALL_SPEED = 6.0
MAX_BALL_ANGLE = math.radians(65)

BRICK_COLS = 12
BRICK_ROWS = 7
BRICK_W, BRICK_H = 58, 22
BRICK_GAP = 4
BRICK_TOP = 70

START_LIVES = 3
POWERUP_CHANCE = 0.15
WIDE_DURATION = 10 * FPS

BG = (12, 12, 24)
WHITE = (240, 240, 240)
ROW_COLORS = [
    (231, 76, 60),
    (230, 126, 34),
    (241, 196, 15),
    (46, 204, 113),
    (26, 188, 156),
    (52, 152, 219),
    (155, 89, 182),
]

class Brick:
    def __init__(self, x, y, row, hp):
        self.rect = pygame.Rect(x, y, BRICK_W, BRICK_H)
        self.color = ROW_COLORS[row % len(ROW_COLORS)]
        self.hp = hp
        self.max_hp = hp
        self.points = (BRICK_ROWS - row) * 10

    def draw(self, surf):
        color = self.color
        if self.hp > 1:  
            color = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(surf, color, self.rect, border_radius=4)
        if self.hp > 1:
            pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=4)


class PowerUp:
    KINDS = {"W": ((52, 152, 219), "Wide paddle"), "L": ((231, 76, 60), "Extra life")}

    def __init__(self, x, y):
        self.kind = random.choice(list(self.KINDS))
        self.rect = pygame.Rect(0, 0, 28, 18)
        self.rect.center = (x, y)

    def update(self):
        self.rect.y += 3

    def draw(self, surf, font):
        pygame.draw.rect(surf, self.KINDS[self.kind][0], self.rect, border_radius=8)
        label = font.render(self.kind, True, WHITE)
        surf.blit(label, label.get_rect(center=self.rect.center))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Breakout")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas,arial", 22)
        self.small = pygame.font.SysFont("consolas,arial", 16, bold=True)
        self.big = pygame.font.SysFont("consolas,arial", 56, bold=True)
        self.reset()

    def reset(self):
        self.score = 0
        self.lives = START_LIVES
        self.level = 1
        self.state = "ready"  
        self.build_level()

    def build_level(self):
        self.paddle = pygame.Rect(0, HEIGHT - 40, PADDLE_W, PADDLE_H)
        self.paddle.centerx = WIDTH // 2
        self.wide_timer = 0
        self.powerups = []
        self.speed = BASE_BALL_SPEED + (self.level - 1) * 0.7

        total_w = BRICK_COLS * BRICK_W + (BRICK_COLS - 1) * BRICK_GAP
        left = (WIDTH - total_w) // 2
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                if self.level % 2 == 0 and (row + col) % 5 == 0:
                    continue
                x = left + col * (BRICK_W + BRICK_GAP)
                y = BRICK_TOP + row * (BRICK_H + BRICK_GAP)
                hp = 2 if (self.level >= 2 and row < min(self.level, 3)) else 1
                self.bricks.append(Brick(x, y, row, hp))
        self.reset_ball()

    def reset_ball(self):
        self.pos = pygame.Vector2(self.paddle.centerx, self.paddle.top - BALL_RADIUS - 1)
        self.vel = pygame.Vector2(0, 0)
        self.state = "ready" if self.state != "paused" else self.state

    def launch(self):
        angle = random.uniform(-math.radians(30), math.radians(30))
        self.vel = pygame.Vector2(math.sin(angle), -math.cos(angle)) * self.speed
        self.state = "playing"

    def move_paddle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.x += PADDLE_SPEED
        if pygame.mouse.get_rel() != (0, 0):  
            self.paddle.centerx = pygame.mouse.get_pos()[0]
        self.paddle.clamp_ip(self.screen.get_rect())

    def update_wide_paddle(self):
        if self.wide_timer > 0:
            self.wide_timer -= 1
            target = int(PADDLE_W * 1.6)
        else:
            target = PADDLE_W
        if self.paddle.width != target:
            cx = self.paddle.centerx
            self.paddle.width = target
            self.paddle.centerx = cx
            self.paddle.clamp_ip(self.screen.get_rect())

    def update_ball(self):
        self.pos += self.vel
        r = BALL_RADIUS

        if self.pos.x - r <= 0:
            self.pos.x = r
            self.vel.x = abs(self.vel.x)
        elif self.pos.x + r >= WIDTH:
            self.pos.x = WIDTH - r
            self.vel.x = -abs(self.vel.x)
        if self.pos.y - r <= 0:
            self.pos.y = r
            self.vel.y = abs(self.vel.y)

        if self.pos.y - r > HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.state = "gameover"
            else:
                self.reset_ball()
            return

        ball_rect = pygame.Rect(self.pos.x - r, self.pos.y - r, r * 2, r * 2)

        if ball_rect.colliderect(self.paddle) and self.vel.y > 0:
            offset = (self.pos.x - self.paddle.centerx) / (self.paddle.width / 2)
            offset = max(-1, min(1, offset))
            angle = offset * MAX_BALL_ANGLE
            self.vel = pygame.Vector2(math.sin(angle), -math.cos(angle)) * self.speed
            self.pos.y = self.paddle.top - r - 1
            return

        for brick in self.bricks:
            if ball_rect.colliderect(brick.rect):
                overlap_x = min(ball_rect.right - brick.rect.left,
                                brick.rect.right - ball_rect.left)
                overlap_y = min(ball_rect.bottom - brick.rect.top,
                                brick.rect.bottom - ball_rect.top)
                if overlap_x < overlap_y:
                    self.vel.x = -self.vel.x
                else:
                    self.vel.y = -self.vel.y

                brick.hp -= 1
                if brick.hp <= 0:
                    self.bricks.remove(brick)
                    self.score += brick.points
                    if random.random() < POWERUP_CHANCE:
                        self.powerups.append(PowerUp(*brick.rect.center))
                else:
                    self.score += 5
                break

        if not self.bricks:
            self.level += 1
            self.state = "ready"
            self.build_level()

    def update_powerups(self):
        for p in self.powerups[:]:
            p.update()
            if p.rect.colliderect(self.paddle):
                if p.kind == "W":
                    self.wide_timer = WIDE_DURATION
                elif p.kind == "L":
                    self.lives = min(self.lives + 1, 9)
                self.powerups.remove(p)
            elif p.rect.top > HEIGHT:
                self.powerups.remove(p)

    def update(self):
        if self.state in ("paused", "gameover"):
            return
        self.move_paddle()
        self.update_wide_paddle()
        if self.state == "ready":
            self.pos.update(self.paddle.centerx, self.paddle.top - BALL_RADIUS - 1)
        elif self.state == "playing":
            self.update_ball()
            self.update_powerups()

    def draw_centered(self, text, font, y, color=WHITE):
        surf = font.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=(WIDTH // 2, y)))

    def draw(self):
        self.screen.fill(BG)

        for brick in self.bricks:
            brick.draw(self.screen)
        for p in self.powerups:
            p.draw(self.screen, self.small)

        pygame.draw.rect(self.screen, WHITE, self.paddle, border_radius=7)
        pygame.draw.circle(self.screen, WHITE, (int(self.pos.x), int(self.pos.y)), BALL_RADIUS)

        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (15, 15))
        lvl = self.font.render(f"Level {self.level}", True, WHITE)
        self.screen.blit(lvl, lvl.get_rect(midtop=(WIDTH // 2, 15)))
        lives = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives, lives.get_rect(topright=(WIDTH - 15, 15)))

        if self.state == "ready":
            self.draw_centered("Press SPACE or click to launch", self.font, HEIGHT // 2 + 60)
        elif self.state == "paused":
            self.draw_centered("PAUSED", self.big, HEIGHT // 2)
        elif self.state == "gameover":
            self.draw_centered("GAME OVER", self.big, HEIGHT // 2 - 20, (231, 76, 60))
            self.draw_centered(f"Final score: {self.score}", self.font, HEIGHT // 2 + 30)
            self.draw_centered("Press SPACE to play again", self.font, HEIGHT // 2 + 65)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_p and self.state in ("playing", "paused"):
                    self.state = "paused" if self.state == "playing" else "playing"
                elif event.key == pygame.K_SPACE:
                    self.action()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.action()

    def action(self):
        if self.state == "ready":
            self.launch()
        elif self.state == "gameover":
            self.reset()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def run(self):
        pygame.mouse.get_rel()  
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()