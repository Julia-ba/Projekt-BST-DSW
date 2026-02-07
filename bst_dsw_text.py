"""
Projekt: BST Logic with Parent Links and DSW Algorithm
Autor: Julia Backa
Opis:
    Wersja konsolowa drzewa BST z algorytmem DSW.
    Dostepne komendy:
        - i <liczba> : wstawia nowy wezel do drzewa (np. 'i 10')
        - v           : przeksztalca drzewo w kregoslup (Vine) - krok 1 DSW
        - b           : rownowazy drzewo - krok 2 DSW
        - c           : czysci drzewo
        - q           : wychodzi z programu
"""

from bst_dsw import BST

def print_tree(node, level=0, prefix="Root:"):
    """
    funkcja drukujaca strukture drzewa w terminalu.
    """
    if node is not None:
        print("   " * level + f"{prefix} {node.data}")
        if node.left or node.right:
            if node.left:
                print_tree(node.left, level + 1, "L:")
            else:
                print("   " * (level + 1) + "L: None")
            if node.right:
                print_tree(node.right, level + 1, "R:")
            else:
                print("   " * (level + 1) + "R: None")
    else:
        print("Tree is empty.")

def main():
    tree = BST()
    is_vine = False 

    print(" BST with DSW Balancing (Text Mode)")
    print("Commands: i <val> (insert), v (vine), b (balance), c (clear), q (quit)")
    print("----------------------------------------------------------------------")

    while True:
        cmd_input = input("\n>> ").strip().lower()

        if not cmd_input:
            continue

        if cmd_input == "q":
            print("Exiting...")
            break

        elif cmd_input.startswith("i "):
            try:
                val = int(cmd_input.split()[1])
                tree.insert(val)
                is_vine = False
                print(f"\n-- After Inserting {val} --")
                print_tree(tree.root)
            except (ValueError, IndexError):
                print("Error: Use 'i' followed by a number (e.g. 'i 10').")

        elif cmd_input == "c":
            tree = BST()
            is_vine = False
            print("\nTree cleared.")

        elif cmd_input == "v":
            tree.make_vine(lambda msg: print(f"[*] {msg}"))
            is_vine = True
            print("\n-- After Vine (Step 1) --")
            print_tree(tree.root)

        elif cmd_input == "b":
            if is_vine:
                tree.balance_dsw(lambda msg: print(f"[*] {msg}"))
                is_vine = False
                print("\n--- After Balancing (Step 2) ---")
                print_tree(tree.root)
            else:
                print("\n[!] ERROR: You must create a Vine ('v') before Balancing ('b')!")

        else:
            print("Unknown command. Use: i <val>, v, b, c, q.")

if __name__ == "__main__":
    main()