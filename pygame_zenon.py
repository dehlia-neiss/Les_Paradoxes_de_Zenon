import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paradoxes de Zénon")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# États possibles
MENU = "menu"
ACHILLE = "achille"
DICHOTOMIE = "dichotomie"
FLECHE = "fleche"

# Mode normal/paradoxal
mode_paradoxal = False

state = MENU

# --- Explications textuelles ---
explications = {
    ACHILLE: {
        False: "Mode normal : Achille finit par dépasser la tortue.",
        True: "Mode paradoxal : Achille atteint toujours la position que la tortue occupait avant, sans la dépasser."
    },
    DICHOTOMIE: {
        False: "Mode normal : La bille parcourt la ligne et atteint la fin.",
        True: "Mode paradoxal : La bille divise la distance par deux à chaque étape, sans jamais atteindre la fin."
    },
    FLECHE: {
        False: "Mode normal : La flèche avance régulièrement avec le temps.",
        True: "Mode paradoxal : La flèche est figée dans l’espace, mais le temps continue d’avancer."
    }
}

# --- Fonctions de rendu ---
def draw_menu():
    screen.fill((240, 240, 240))
    title = font.render("Choisissez un paradoxe (touche 1-3)", True, (0, 0, 0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    options = [
        "1 - Achille et la tortue",
        "2 - La dichotomie",
        "3 - La flèche",
        "P - Activer/désactiver mode paradoxal",
        "ECHAP - Retour / Quitter"
    ]
    for i, text in enumerate(options):
        t = font.render(text, True, (50, 50, 50))
        screen.blit(t, (200, 200 + i*50))


def draw_textbox(text):
    # zone en bas de l’écran pour l’explication
    box_rect = pygame.Rect(0, HEIGHT-80, WIDTH, 80)
    pygame.draw.rect(screen, (230, 230, 230), box_rect)
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 2)
    wrapped = []
    # simple wrap manuel
    while len(text) > 70:
        wrapped.append(text[:70])
        text = text[70:]
    wrapped.append(text)
    for i, line in enumerate(wrapped):
        txt = font.render(line, True, (0, 0, 0))
        screen.blit(txt, (10, HEIGHT-75 + i*25))


def draw_achille(step):
    screen.fill((220, 255, 220))
    
    if mode_paradoxal:
        # Position de la tortue
        tortue_x = 200 + step * 20  

        # Achille essaie de rattraper la tortue, mais ne peut pas la dépasser
        cible = tortue_x
        achille_x = min(100 + step * 30, cible - 1)
    else:
        achille_x = min(100 + step * 5, WIDTH-50)
        tortue_x = min(200 + step * 2, WIDTH-50)

    pygame.draw.circle(screen, (0, 0, 255), (achille_x, HEIGHT//2), 20)
    pygame.draw.circle(screen, (255, 0, 0), (tortue_x, HEIGHT//2), 15)

    text = font.render("Achille et la tortue" + (" (paradoxal)" if mode_paradoxal else ""), True, (0, 0, 0))
    screen.blit(text, (20, 20))
    draw_textbox(explications[ACHILLE][mode_paradoxal])

    # Affichage console
    print(f"[Achille] step={step}, Achille={achille_x}, Tortue={tortue_x}")


def draw_dichotomie(step):
    screen.fill((255, 240, 220))
    start, end = 100, WIDTH - 100
    
    if mode_paradoxal:
        pos = start + (end - start) * (1 - 1/(2**step))
    else:
        pos = start + step*10
    
    pygame.draw.line(screen, (0, 0, 0), (start, HEIGHT//2), (end, HEIGHT//2), 3)
    pygame.draw.circle(screen, (0, 150, 0), (int(pos), HEIGHT//2), 15)

    text = font.render("La dichotomie" + (" (paradoxal)" if mode_paradoxal else ""), True, (0, 0, 0))
    screen.blit(text, (20, 20))
    draw_textbox(explications[DICHOTOMIE][mode_paradoxal])

    # Affichage console
    print(f"[Dichotomie] step={step}, pos={pos:.2f}")


def draw_fleche(step, x, t):
    screen.fill((220, 220, 255))
    start_x, end_x = 100, WIDTH - 100
    pygame.draw.line(screen, (0, 0, 0), (start_x, HEIGHT//2), (end_x, HEIGHT//2), 3)

    if mode_paradoxal:
        arrow_x = start_x + 100
    else:
        arrow_x = start_x + int(x)

    arrow_rect = pygame.Rect(arrow_x, HEIGHT//2 - 10, 40, 20)
    pygame.draw.rect(screen, (150, 0, 0), arrow_rect)
    pygame.draw.polygon(screen, (150, 0, 0), [
        (arrow_x+40, HEIGHT//2-15),
        (arrow_x+60, HEIGHT//2),
        (arrow_x+40, HEIGHT//2+15)
    ])

    text = font.render(f"La flèche {'(paradoxal)' if mode_paradoxal else ''} - t={t:.0f}s, x={x:.1f}", True, (0, 0, 0))
    screen.blit(text, (20, 20))
    draw_textbox(explications[FLECHE][mode_paradoxal])

    # Affichage console
    print(f"[Flèche] step={step}, t={t}, x={x:.1f}")


# --- Boucle principale ---
step = 0
x, v, t, dt, temps_total = 0, 20, 0, 1, 15

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if state == MENU:
                if event.key == pygame.K_1:
                    state = ACHILLE; step = 0
                elif event.key == pygame.K_2:
                    state = DICHOTOMIE; step = 0
                elif event.key == pygame.K_3:
                    state = FLECHE; step = 0; x, t = 0, 0
                elif event.key == pygame.K_p:
                    mode_paradoxal = not mode_paradoxal
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            else:
                if event.key == pygame.K_ESCAPE:
                    state = MENU

    if state == MENU:
        draw_menu()
    elif state == ACHILLE:
        draw_achille(step)
        step += 1
    elif state == DICHOTOMIE:
        draw_dichotomie(step)
        step += 1
    elif state == FLECHE:
        if not mode_paradoxal:
            x += v * dt
            t += dt
        else:
            t += dt
        draw_fleche(step, x, t)
        step += 1

    pygame.display.flip()
    clock.tick(2)
