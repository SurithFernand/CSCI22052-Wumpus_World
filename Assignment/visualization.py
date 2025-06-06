import pygame
from wumpus_world import WumpusWorld
from agent import LogicAgent
import time

TILE_SIZE = 100
GRID_SIZE = 4
WIDTH = HEIGHT = TILE_SIZE * GRID_SIZE
screen_height = HEIGHT + 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wumpus World")
clock = pygame.time.Clock()

wumpus_image = pygame.image.load("assets/wumpus.png")
wumpus_image = pygame.transform.scale(wumpus_image, (60, 60))  # fit into 100x100 tile

gold_img = pygame.image.load("assets/gold.png")
gold_img = pygame.transform.scale(gold_img, (60, 60))

pit_img = pygame.image.load("assets/pit.jpeg")
pit_img = pygame.transform.scale(pit_img, (60, 60))

font = pygame.font.SysFont(None, 24)


def draw_arrow(x, y, direction):
    center = (y * TILE_SIZE + 50, x * TILE_SIZE + 50)
    if direction == "up":
        pygame.draw.polygon(screen, (0, 0, 255), [(center[0], center[1] - 20), (center[0] - 10, center[1] + 10), (center[0] + 10, center[1] + 10)])
    elif direction == "down":
        pygame.draw.polygon(screen, (0, 0, 255), [(center[0], center[1] + 20), (center[0] - 10, center[1] - 10), (center[0] + 10, center[1] - 10)])
    elif direction == "left":
        pygame.draw.polygon(screen, (0, 0, 255), [(center[0] - 20, center[1]), (center[0] + 10, center[1] - 10), (center[0] + 10, center[1] + 10)])
    elif direction == "right":
        pygame.draw.polygon(screen, (0, 0, 255), [(center[0] + 20, center[1]), (center[0] - 10, center[1] - 10), (center[0] - 10, center[1] + 10)])


def draw_grid(env):
    screen.fill((255, 255, 255))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x, y = j * TILE_SIZE, i * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            cell = env.world[i][j]
            percept_texts = []

            # Determine percepts based on surroundings
            stench, breeze = False, False
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + dx, j + dy
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                    adj_cell = env.world[ni][nj]
                    if adj_cell['wumpus'] and env.wumpus_alive:
                        stench = True
                    if adj_cell['pit']:
                        breeze = True

            if stench:
                percept_texts.append("Stench")
            if breeze:
                percept_texts.append("Breeze")
            if cell['gold']:
                percept_texts.append("Glitter")

            # Draw percept labels in the cell
            for idx, text in enumerate(percept_texts):
                label = font.render(text, True, (100, 100, 100))
                screen.blit(label, (x + 5, y + 5 + 15 * idx))

            # Draw pit, Wumpus, gold as symbols
            # if cell['pit']:
            #     pygame.draw.circle(screen, (0, 0, 0), (x + 50, y + 50), 10)
            if cell['pit']:
                screen.blit(pit_img, (x + 20, y + 20))
            # if cell['wumpus'] and env.wumpus_alive:
            #     pygame.draw.circle(screen, (255, 0, 0), (x + 50, y + 50), 10)
            if cell['wumpus'] and env.wumpus_alive:
                screen.blit(wumpus_image, (x + 20, y + 20))  # Centered in cell
            # if cell['gold']:
            #     pygame.draw.circle(screen, (255, 215, 0), (x + 50, y + 50), 10)
            if cell['gold']:
                screen.blit(gold_img, (x + 20, y + 20))

    # Draw the agent
    ax, ay = env.agent_pos
    draw_arrow(ax, ay, env.agent_dir)


    # Show current percepts (bottom of the screen)
    percepts = env.percepts
    percept_list = []
    if percepts["stench"]:
        percept_list.append("Stench")
    if percepts["breeze"]:
        percept_list.append("Breeze")
    if percepts["glitter"]:
        percept_list.append("Glitter")
    if percepts["bump"]:
        percept_list.append("Bump")
    if percepts["scream"]:
        percept_list.append("Scream")
    if not percept_list:
        percept_list.append("None")

    percept_text = "Percepts: " + ", ".join(percept_list)
    text_surface = font.render(percept_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, HEIGHT + 10))


def animate_arrow_shot(env):
    start_x, start_y = env.agent_pos
    dx, dy = 0, 0

    if env.agent_dir == "up":
        dx = -1
    elif env.agent_dir == "down":
        dx = 1
    elif env.agent_dir == "left":
        dy = -1
    elif env.agent_dir == "right":
        dy = 1

    for step in range(1, GRID_SIZE):
        nx = start_x + dx * step
        ny = start_y + dy * step
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            draw_grid(env)
            pygame.draw.line(screen, (255, 0, 0), (start_y * TILE_SIZE + 50, start_x * TILE_SIZE + 50),
                             (ny * TILE_SIZE + 50, nx * TILE_SIZE + 50), 4)
            pygame.display.flip()
            time.sleep(0.2)
        else:
            break


def main():
    env = WumpusWorld()
    agent = LogicAgent(env)

    screen_height = HEIGHT + 100
    pygame.display.set_mode((WIDTH, screen_height))

    running = True
    steps = 0

    while running and steps < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid(env)
        pygame.display.flip()
        time.sleep(1.5)  #  Pause before each action

        # Stench → Shoot Wumpus
        if env.percepts['stench'] and env.has_arrow:
            animate_arrow_shot(env)
            env.shoot_arrow()
            draw_grid(env)
            pygame.display.flip()
            time.sleep(1.0)

        # Agent decides and moves
        agent.make_move()
        draw_grid(env)
        pygame.display.flip()
        time.sleep(1.5)  #  Pause after each move

        # Check for end of game
        game_state = env.is_game_over()
        if game_state != "continue":
            print("Game Over:", game_state)
            time.sleep(2)
            break

        steps += 1
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()