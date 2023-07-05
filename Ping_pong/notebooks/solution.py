import pygame
import time

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
WINNING_SCORE = 5

pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans", 50)


class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, height, width):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.height = height
        self.width = width

    def draw_paddle(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw_ball(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0


def draw(win, paddles, ball, left_Score, right_Score):
    win.fill(BLACK)

    left_Score_text = SCORE_FONT.render(f"{left_Score}", 1, WHITE)
    right_Score_text = SCORE_FONT.render(f"{right_Score}", 1, WHITE)

    win.blit(left_Score_text, (WIDTH // 4 - left_Score_text.get_width() // 2, 20))
    win.blit(
        right_Score_text, (WIDTH * (3 / 4) - right_Score_text.get_width() // 2, 20)
    )

    for padd in paddles:
        padd.draw_paddle(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        else:
            pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw_ball(win)

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1

    if ball.x_vel > 0:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / (ball.MAX_VEL)
                y_vel = difference_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / (ball.MAX_VEL)
                y_vel = difference_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(key, left_handle, right_handle):
    if key[pygame.K_w] and left_handle.y - left_handle.VEL >= 0:
        left_handle.move(up=True)
    if key[pygame.K_s] and left_handle.y + left_handle.VEL + PADDLE_HEIGHT <= HEIGHT:
        left_handle.move(up=False)
    if key[pygame.K_UP] and right_handle.y - right_handle.VEL >= 0:
        right_handle.move(up=True)
    if (
        key[pygame.K_DOWN]
        and right_handle.y + right_handle.VEL + PADDLE_HEIGHT <= HEIGHT
    ):
        right_handle.move(up=False)


def handle_score(score, ball, left_handle, right_handle):
    score += 1
    ball.reset()
    left_handle.reset()
    right_handle.reset()
    time.sleep(1)

    return score


def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(
        10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_HEIGHT, PADDLE_WIDTH
    )
    right_paddle = Paddle(
        WIDTH - 10 - PADDLE_WIDTH,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_HEIGHT,
        PADDLE_WIDTH,
    )

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_Score, right_Score = 0, 0
    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_Score, right_Score)
        ball.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_Score = handle_score(right_Score, ball, left_paddle, right_paddle)
        if ball.x > WIDTH:
            left_Score = handle_score(left_Score, ball, left_paddle, right_paddle)

        won = False
        if right_Score >= WINNING_SCORE:
            won = True
            win_text = "RIGHT WON!!"
        elif left_Score >= WINNING_SCORE:
            win_text = "LEFT WON!!"
            won = True

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_Score = 0
            right_Score = 0

    pygame.quit()


if __name__ == "__main__":
    main()
