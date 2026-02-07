"""
Projekt: BST Logic with Parent Links and DSW Algorithm
Autor: Julia Backa
Opis:
    Program umozliwia interaktywna wizualizacje algorytmu rownowazenia drzewa
    BST (Binary Search Tree) metoda DSW (Day–Stout–Warren) przy uzyciu biblioteki Pygame.

    Uzytkownik moze:
        - wstawiac kolejne wezly (I),
        - przeksztalcac drzewo w kregoslup (Vine) (V),
        - rownowazyc drzewo (B),
        - przesuwac i przyblizac kamere (mysz),
        - czyścic drzewo (C),
        - resetowac widok (R).
"""
import pygame
import sys
import time
from bst_dsw import BST

# konfiguracja wizualna
WIDTH, HEIGHT = 1200, 800
NODE_RADIUS = 22
COLOR_BG = (20, 22, 30)
COLOR_NODE = (52, 152, 219)
COLOR_TEXT = (255, 255, 255)
COLOR_LINE = (127, 140, 141)
COLOR_ACCENT = (241, 194, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BST DSW Visualizer - Julia Backa")
font = pygame.font.SysFont("Segoe UI", 18)
title_font = pygame.font.SysFont("Segoe UI", 24, bold=True)


def update_positions(node, x, y, dx):
    """
    Wyznacza wspolrzedne (x,y) kazdego wezla w drzewie.
    """
    if node:
        node.x, node.y = x, y
        update_positions(node.left, x - dx, y + 90, dx * 0.5)
        update_positions(node.right, x + dx, y + 90, dx * 0.5)


def draw_tree(screen, node, off_x, off_y, zoom):
    """
    Rysuje drzewo na ekranie.
    """
    if not node: return

    sx = int(node.x * zoom + off_x)
    sy = int(node.y * zoom + off_y)
    curr_radius = int(NODE_RADIUS * zoom)

    if node.left:
        lx = int(node.left.x * zoom + off_x)
        ly = int(node.left.y * zoom + off_y)
        pygame.draw.line(screen, COLOR_LINE, (sx, sy), (lx, ly), max(1, int(2 * zoom)))
        draw_tree(screen, node.left, off_x, off_y, zoom)

    if node.right:
        rx = int(node.right.x * zoom + off_x)
        ry = int(node.right.y * zoom + off_y)
        pygame.draw.line(screen, COLOR_LINE, (sx, sy), (rx, ry), max(1, int(2 * zoom)))
        draw_tree(screen, node.right, off_x, off_y, zoom)

    pygame.draw.circle(screen, COLOR_NODE, (sx, sy), curr_radius)
    pygame.draw.circle(screen, (255, 255, 255), (sx, sy), curr_radius, max(1, int(2 * zoom)))

    if zoom > 0.4:
        val_txt = font.render(str(node.data), True, COLOR_TEXT)
        screen.blit(val_txt, (sx - val_txt.get_width() // 2, sy - val_txt.get_height() // 2))


def refresh_screen(tree, msg, input_txt, cam_x, cam_y, zoom):
    """
    Odswieza ekran, rysujac aktualny stan drzewa
    i interfejs uzytkownika.
    """
    screen.fill(COLOR_BG)
    if tree.root:
        update_positions(tree.root, 0, 0, 400)
        draw_tree(screen, tree.root, cam_x, cam_y, zoom)

    pygame.draw.rect(screen, (40, 44, 52), (0, 0, WIDTH, 110))
    screen.blit(title_font.render("DSW Algorithm Project", True, COLOR_ACCENT), (20, 10))
    controls = "I: Insert | V: Vine | B: Balance | C: Clear | R: Reset Cam | Drag Mouse to Pan"
    screen.blit(font.render(controls, True, (200, 200, 200)), (20, 45))
    screen.blit(font.render(f"Status: {msg}", True, (46, 204, 113)), (20, 75))

    if input_txt:
        pygame.draw.rect(screen, (60, 60, 70), (WIDTH - 200, 20, 180, 40))
        screen.blit(font.render(f"Input: {input_txt}", True, (255, 255, 255)), (WIDTH - 190, 28))

    pygame.display.flip()


def main():
    tree = BST()
    msg = "Ready. Press 'I' to start adding nodes."
    input_text = ""
    typing = False
    is_vine = False #

    cam_x, cam_y = WIDTH // 2, 180
    zoom = 1.0
    dragging = False
    last_mouse_pos = (0, 0)

    def animate_step(custom_msg):
        """
        Odswieza ekran i wstrzymuje dzialanie programu na krotki czas,
        aby wizualizacja zmian w strukturze drzewa byla plynna i widoczna.
        """
        refresh_screen(tree, custom_msg, "", cam_x, cam_y, zoom)
        time.sleep(0.5)

    while True:
        refresh_screen(tree, msg, input_text if typing else "", cam_x, cam_y, zoom)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Obsluga myszy (Zoom i Pan)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: dragging = True; last_mouse_pos = event.pos
                if event.button == 4: zoom *= 1.1
                if event.button == 5: zoom *= 0.9
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                mx, my = event.pos
                cam_x += mx - last_mouse_pos[0]
                cam_y += my - last_mouse_pos[1]
                last_mouse_pos = event.pos

            if event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit():
                            tree.insert(int(input_text))
                            msg = f"Inserted {input_text}"
                            is_vine = False
                        typing = False; input_text = ""
                    elif event.key == pygame.K_BACKSPACE: input_text = input_text[:-1]
                    elif event.key == pygame.K_ESCAPE: typing = False; input_text = ""
                    elif event.unicode.isdigit(): input_text += event.unicode
                else:
                    if event.key == pygame.K_i: typing = True; msg = "Enter number and press ENTER"
                    if event.key == pygame.K_r: cam_x, cam_y, zoom = WIDTH // 2, 180, 1.0
                    if event.key == pygame.K_c:
                        tree = BST()
                        msg = "Tree cleared."
                        is_vine = False

                    if event.key == pygame.K_v:
                        tree.make_vine(animate_step)
                        is_vine = True
                        msg = "Vine complete. Now you can Balance (B)."

                    if event.key == pygame.K_b:
                        if is_vine:
                            tree.balance_dsw(animate_step)
                            is_vine = False
                            msg = "Tree Balanced!"
                        else:
                            msg = "ERROR: You must create a Vine (V) first!"

if __name__ == "__main__":
    main()