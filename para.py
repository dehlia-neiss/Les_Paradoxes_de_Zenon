import pygame
import sys

# =====================
# CONFIGURATION INITIALE
# =====================
pygame.init()
FPS = 60
clock = pygame.time.Clock()

# Taille de la fenêtre
LARGEUR, HAUTEUR = 800, 300
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Paradoxe de Zénon - Version pédagogique")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
MARRON = (139, 69, 19)
GRIS_PIERRE = (100, 100, 100)
VERT_BASE = (0, 200, 0)
GRIS_FONCE = (200, 200, 200)

# Police
font = pygame.font.SysFont("Arial", 22)

# =====================
# PARAMÈTRES DE L'ANIMATION
# =====================
DISTANCE_TOTALE = 8.0          # mètres
DEPART_PX = 50
ARRIVEE_PX = LARGEUR - 100
PIXELS_PAR_METRE = (ARRIVEE_PX - DEPART_PX) / DISTANCE_TOTALE
VITESSE = 2                     # pixels/frame

# Barre de progression
BARRE_X = DEPART_PX
BARRE_Y = 220
BARRE_LONGUEUR = ARRIVEE_PX - DEPART_PX
BARRE_HAUTEUR = 20

# =====================
# VARIABLES DYNAMIQUES
# =====================
etape = 0
reste_m = DISTANCE_TOTALE
position_m = 0.0
position_px = DEPART_PX
target_m = 0.0
target_px = DEPART_PX
derniere_distance_avancee = 0.0  # pour afficher combien la pierre avance à chaque étape

# =====================
# FONCTION POUR PASSER À L'ÉTAPE SUIVANTE
# =====================
def avancer_etape():
    global etape, reste_m, target_m, target_px, derniere_distance_avancee
    if reste_m > 1e-3:
        etape += 1
        derniere_distance_avancee = reste_m / 2
        reste_m /= 2
        target_m = DISTANCE_TOTALE - reste_m
        target_px = DEPART_PX + target_m * PIXELS_PAR_METRE

# =====================
# BOUCLE PRINCIPALE
# =====================
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        # Touche ESPACE pour avancer
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                avancer_etape()

    # --------- ANIMATION FLUIDE ---------
    if position_px < target_px:
        position_px += VITESSE
        if position_px > target_px:
            position_px = target_px
    elif position_px > target_px:
        position_px -= VITESSE
        if position_px < target_px:
            position_px = target_px
    position_m = (position_px - DEPART_PX) / PIXELS_PAR_METRE

    # --------- DESSIN ---------
    fenetre.fill(BLANC)

    # Arbre
    pygame.draw.rect(fenetre, MARRON, (ARRIVEE_PX, HAUTEUR//2 - 40, 30, 80))

    # Pierre (couleur fixe)
    pygame.draw.circle(fenetre, GRIS_PIERRE, (int(position_px), HAUTEUR//2), 15)

    # Barre de progression (vert dynamique)
    vert = int(50 + (position_m / DISTANCE_TOTALE) * 205)
    couleur_barre = (0, vert, 0)
    pygame.draw.rect(fenetre, GRIS_FONCE, (BARRE_X, BARRE_Y, BARRE_LONGUEUR, BARRE_HAUTEUR))
    pygame.draw.rect(fenetre, couleur_barre, (BARRE_X, BARRE_Y, position_m * PIXELS_PAR_METRE, BARRE_HAUTEUR))

    # Texte distance sous barre
    texte_barre = font.render(f"{position_m:.3f} m / {DISTANCE_TOTALE} m", True, NOIR)
    fenetre.blit(texte_barre, (BARRE_X, BARRE_Y + BARRE_HAUTEUR + 5))

    # Texte étape
    texte_etape = font.render(f"Étape {etape}", True, NOIR)
    fenetre.blit(texte_etape, (20, 20))

    # Instruction
    instruction = font.render("Appuie sur ESPACE pour avancer", True, NOIR)
    fenetre.blit(instruction, (20, 60))

    # Affichage calcul du paradoxe
    calcul_paradoxe = font.render(
        f"Distance avancée cette étape: {derniere_distance_avancee:.3f} m | "
        f"Distance restante: {reste_m:.3f} m", True, NOIR
    )
    fenetre.blit(calcul_paradoxe, (20, BARRE_Y + BARRE_HAUTEUR + 35))

    # Actualiser écran
    pygame.display.flip()

pygame.quit()
