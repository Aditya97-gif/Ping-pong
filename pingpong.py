import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)


BG = (30, 30, 30)
WHITE = (240, 240, 240)
LINE = (70, 70, 70)


PADDLE_W, PADDLE_H = 12, 90
BALL_SIZE = 14
PADDLE_SPEED = 6
BALL_SPEED = 5

left_paddle = pygame.Rect(30, (HEIGHT - PADDLE_H) // 2, PADDLE_W, PADDLE_H)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_W, (HEIGHT - PADDLE_H) // 2, PADDLE_W, PADDLE_H)
ball = pygame.Rect((WIDTH - BALL_SIZE)//2, (HEIGHT - BALL_SIZE)//2, BALL_SIZE, BALL_SIZE)

score_left = 0
score_right = 0

ball_vel = pygame.Vector2()
serving = True
serve_dir = 1  

def reset_ball(direction=None):
    global ball, ball_vel, serving, serve_dir
    ball.center = (WIDTH//2, HEIGHT//2)
    serving = True
    if direction is None:
        serve_dir = random.choice([-1, 1])
    else:
        serve_dir = direction
    ball_vel = pygame.Vector2(0, 0)

def serve_ball():
    global ball_vel, serving
    angle = random.uniform(-0.35, 0.35)  # slight angle
    ball_vel = pygame.Vector2(serve_dir * BALL_SPEED, BALL_SPEED * angle)
    serving = False

def draw():
    SCREEN.fill(BG)
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(SCREEN, LINE, (WIDTH//2 - 1, y+6, 2, 12))
    pygame.draw.rect(SCREEN, WHITE, left_paddle)
    pygame.draw.rect(SCREEN, WHITE, right_paddle)
    pygame.draw.ellipse(SCREEN, WHITE, ball)
    left_text = FONT.render(str(score_left), True, WHITE)
    right_text = FONT.render(str(score_right), True, WHITE)
    SCREEN.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
    SCREEN.blit(right_text, (WIDTH*3//4 - right_text.get_width()//2, 20))
    instr = FONT.render("W/S  - Left   Up/Down - Right   Space - Serve   R - Reset   Esc - Quit", True, (160,160,160))
    SCREEN.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT - 40))
    if serving:
        hint = FONT.render("Press SPACE to serve", True, (180,180,180))
        SCREEN.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 - 40))
    pygame.display.flip()

def clamp_paddles():
    if left_paddle.top < 0:
        left_paddle.top = 0
    if left_paddle.bottom > HEIGHT:
        left_paddle.bottom = HEIGHT
    if right_paddle.top < 0:
        right_paddle.top = 0
    if right_paddle.bottom > HEIGHT:
        right_paddle.bottom = HEIGHT

def update():
    global score_left, score_right, serving
    if not serving:
        ball.x += int(ball_vel.x)
        ball.y += int(ball_vel.y)
        # top/bottom bounce
        if ball.top <= 0:
            ball.top = 0
            ball_vel.y *= -1
        if ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_vel.y *= -1
        if ball.colliderect(left_paddle) and ball_vel.x < 0:
            overlap = (ball.centery - left_paddle.centery) / (PADDLE_H/2)
            ball_vel.x *= -1.05
            ball_vel.y = BALL_SPEED * overlap
            ball.left = left_paddle.right
        if ball.colliderect(right_paddle) and ball_vel.x > 0:
            overlap = (ball.centery - right_paddle.centery) / (PADDLE_H/2)
            ball_vel.x *= -1.05
            ball_vel.y = BALL_SPEED * overlap
            ball.right = right_paddle.left

        if ball.right < 0:
            score_right += 1
            reset_ball(direction=1)
        if ball.left > WIDTH:
            score_left += 1
            reset_ball(direction=-1)


reset_ball()

def main():
    global serving
    running = True
    while running:
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and serving:
                    serve_ball()
                if event.key == pygame.K_r:
                    reset_ball()
                    reset_scores()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            right_paddle.y += PADDLE_SPEED

        clamp_paddles()
        update()
        draw()

    pygame.quit()
    sys.exit()

def reset_scores():
    global score_left, score_right
    score_left = 0
    score_right = 0

if __name__ == "__main__":
    main()
