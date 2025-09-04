import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paradoxes de Zénon")
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# États possibles
MENU = "menu"
ACHILLE = "achille"
DICHOTOMIE = "dichotomie"
FLECHE = "fleche"

state = MENU

# --- Fonctions de rendu ---
def draw_menu():
    screen.fill((240, 240, 240))
    title = font.render("Choisissez un paradoxe", True, (0, 0, 0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    options = ["1 - Achille et la tortue", "2 - La dichotomie", "3 - La flèche", "ECHAP - Quitter"]
    for i, text in enumerate(options):
        t = font.render(text, True, (50, 50, 50))
        screen.blit(t, (200, 200 + i*60))


def draw_achille(step):
    screen.fill((220, 255, 220))
    achille_x = min(100 + step*5, WIDTH-50)
    tortue_x = min(200 + step*2, WIDTH-50)
    pygame.draw.circle(screen, (0, 0, 255), (achille_x, HEIGHT//2), 20)  # Achille
    pygame.draw.circle(screen, (255, 0, 0), (tortue_x, HEIGHT//2), 15)  # Tortue

    text = font.render("Achille et la tortue", True, (0, 0, 0))
    screen.blit(text, (20, 20))


def draw_dichotomie(step):
    screen.fill((255, 240, 220))
    start, end = 100, WIDTH - 100
    pos = start + (end-start) * (1 - 1/(step+1))
    pygame.draw.line(screen, (0, 0, 0), (start, HEIGHT//2), (end, HEIGHT//2), 3)
    pygame.draw.circle(screen, (0, 150, 0), (int(pos), HEIGHT//2), 15)

    text = font.render("La dichotomie", True, (0, 0, 0))
    screen.blit(text, (20, 20))


def draw_fleche(step):
    screen.fill((220, 220, 255))
    arrow_rect = pygame.Rect(WIDTH//2 - 40, HEIGHT//2 - 5, 80, 10)
    pygame.draw.rect(screen, (150, 0, 0), arrow_rect)
    pygame.draw.polygon(screen, (150, 0, 0), [(WIDTH//2+40, HEIGHT//2-10), (WIDTH//2+60, HEIGHT//2), (WIDTH//2+40, HEIGHT//2+10)])

    text = font.render(f"La flèche (t = {step})", True, (0, 0, 0))
    screen.blit(text, (20, 20))


# --- Boucle principale ---
step = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if state == MENU:
                if event.key == pygame.K_1:
                    state = ACHILLE; step = 0
                elif event.key == pygame.K_2:
                    state = DICHOTOMIE; step = 0
                elif event.key == pygame.K_3:
                    state = FLECHE; step = 0
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            else:
                if event.key == pygame.K_ESCAPE:
                    state = MENU

    # Dessins en fonction de l'état
    if state == MENU:
        draw_menu()
    elif state == ACHILLE:
        draw_achille(step)
        step += 1
    elif state == DICHOTOMIE:
        draw_dichotomie(step)
        step += 1
    elif state == FLECHE:
        draw_fleche(step)
        step += 1

    pygame.display.flip()
    clock.tick(30)
