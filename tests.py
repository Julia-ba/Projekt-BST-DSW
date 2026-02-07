import unittest
import random
import math
from bst_dsw import BST


class TestDSW(unittest.TestCase):
    def setUp(self):
        self.tree = BST()

    def get_height(self, node):
        """Pomocnicza funkcja do obliczania wysokosci drzewa."""
        if not node:
            return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def test_insertion(self):
        nodes = [10, 5, 15]
        for n in nodes:
            self.tree.insert(n)
        self.assertEqual(self.tree.root.data, 10)
        self.assertEqual(self.tree.root.left.data, 5)
        self.assertEqual(self.tree.root.right.data, 15)

    def test_parent_links(self):
        self.tree.insert(10)
        self.tree.insert(5)
        self.assertEqual(self.tree.root.left.parent, self.tree.root)

    def test_balance(self):
        for i in range(1, 8):
            self.tree.insert(i)

        self.tree.make_vine()
        self.tree.balance_dsw()

        self.assertEqual(self.tree.root.data, 4)
        self.assertEqual(self.get_height(self.tree.root), 3)

    def test_stress_large_scale(self):
        """Test sprawdzajacy stabilnosc i wydajnosc dla 1000 wezlow."""
        n = 1000
        random.seed(42)
        nodes = random.sample(range(1, 10001), n)

        for val in nodes:
            self.tree.insert(val)

        self.tree.make_vine()
        self.tree.balance_dsw()

        self.assertIsNotNone(self.tree.root)

        expected_height = math.ceil(math.log2(n + 1))
        actual_height = self.get_height(self.tree.root)

        self.assertEqual(actual_height, expected_height,
                         f"Nieoptymalna wysokosc: Oczekiwano {expected_height}, otrzymano {actual_height}")

        curr = self.tree.root
        if curr.left:
            self.assertEqual(curr.left.parent, curr)
        if curr.right:
            self.assertEqual(curr.right.parent, curr)


if __name__ == "__main__":
    unittest.main()