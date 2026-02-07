"""
Projekt: BST Logic with Parent Links and DSW Algorithm
Autor: Julia Backa
Opis:
    Modul implementuje drzewo BST (Binary Search Tree) z laczami do rodzicow
    oraz algorytm rownowazenia DSW (Day–Stout–Warren).
    Struktura jest zaprojektowana w sposob obiektowy i moze byc uzywana
    z graficznymi wizualizacjami (np. w Pygame lub Matplotlib).

"""


class Node:
    """
    Klasa reprezentujaca pojedynczy wezel drzewa BST.
    """
    def __init__(self, data=None, left=None, right=None, parent=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.x = 0
        self.y = 0

    def __str__(self):
        return str(self.data)


class BST:
    """
    Klasa reprezentujaca drzewo BST z mozliwoscia
    rownowazenia za pomoca algorytmu DSW.
    """
    def __init__(self):
        self.root = None

    def insert(self, data):
        """
        Wstawia nowy element do drzewa BST.
        """
        if self.root is None:
            self.root = Node(data)
            return
        cur = self.root
        while True:
            if data < cur.data:
                if cur.left:
                    cur = cur.left
                else:
                    cur.left = Node(data, parent=cur)
                    return
            elif data > cur.data:
                if cur.right:
                    cur = cur.right
                else:
                    cur.right = Node(data, parent=cur)
                    return
            else:
                return

    def rotate_right(self, node):
        """
        Wykonuje rotacje w prawo wzgledem podanego wezla.
        """
        parent = node.parent
        left_child = node.left
        if not left_child: return

        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node

        left_child.right = node
        left_child.parent = parent

        if not parent:
            self.root = left_child
        elif parent.left == node:
            parent.left = left_child
        else:
            parent.right = left_child
        node.parent = left_child

    def rotate_left(self, node):
        """
        Wykonuje rotacje w lewo wzgledem podanego wezla.
        """
        parent = node.parent
        right_child = node.right
        if not right_child: return

        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node

        right_child.left = node
        right_child.parent = parent

        if not parent:
            self.root = right_child
        elif parent.right == node:
            parent.right = right_child
        else:
            parent.left = right_child
        node.parent = right_child

    def make_vine(self, callback=None):
        """
        Krok 1 algorytmu DSW:
        Przeksztalca drzewo w "kregoslup" (vine),
        czyli liste polaczona prawymi wskaznikami.
        """
        pseudo_root = Node(None)
        pseudo_root.right = self.root
        if self.root: self.root.parent = pseudo_root

        tail = pseudo_root
        rest = tail.right
        while rest:
            if rest.left:
                self.rotate_right(rest)
                rest = tail.right
                if callback: callback("Vine: Rotating Right...")
            else:
                tail = rest
                rest = tail.right

        self.root = pseudo_root.right
        if self.root: self.root.parent = None

    def _compress(self, count, callback=None):
        """
        Wykonuje faze kompresji algorytmu DSW
        poprzez zadana liczbe rotacji w lewo.
        """
        pseudo_root = Node(None)
        pseudo_root.right = self.root
        if self.root: self.root.parent = pseudo_root
        curr_scan = pseudo_root
        for _ in range(count):
            child = curr_scan.right
            if child and child.right:
                self.rotate_left(child)
                curr_scan = curr_scan.right
                if callback: callback("Balancing: Rotating Left...")
        self.root = pseudo_root.right
        if self.root: self.root.parent = None

    def balance_dsw(self, callback=None):
        """
        Krok 2 algorytmu DSW:
        Wykonuje kolejne rotacje w lewo,
        aby uzyskac zbalansowane drzewo.
        """

        n = 0
        curr = self.root
        while curr:
            n += 1
            curr = curr.right

        if n > 0:
            m = 2 ** (n.bit_length() - 1) - 1
            self._compress(n - m, callback)
            while m > 1:
                m //= 2
                self._compress(m, callback)