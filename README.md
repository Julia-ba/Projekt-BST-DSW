# Projekt-BST-DSW

Implementacja drzewa BST z algorytmem równoważenia Day–Stout–Warren (DSW) i wizualizacją graficzną. 

Projekt realizuje strukturę danych Binary Search Tree (BST), w której każdy węzeł przechowuje referencję do swojego rodzica (parent links). Głównym celem projektu jest demonstracja działania algorytmu DSW, który pozwala na zbalansowanie dowolnego drzewa BST do postaci drzewa o minimalnej wysokości, wykonując operacje w miejscu. 

# Interfejsy Użytkownika

Projekt został zaprojektowany w sposób modułowy, oferując dwa niezależne sposoby interakcji z drzewem:

- Moduł Graficzny (Pygame)
- Moduł Terminalowy (CLI)

#Uruchomienie

- Wizualizacja graficzna - python main_pygame.py
- Tryb tekstowy - python bst_dsw_text.py

#Pliki

- Dokumentacja_bst_dsw.pdf - pełna dokumentacja techniczna i opis 
- bst_dsw.py - logika drzewa i algorytmu DSW
- main_pygame.py - główny program z interfejsem graficznym
- bst_dsw_text.py - interfejs wiersza poleceń
- tests.py - testy poprawności struktury
