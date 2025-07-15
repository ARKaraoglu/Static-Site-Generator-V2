import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a TextNode", TextType.TEXT)
        node2 = TextNode("This is a TextNode", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a TextNode", TextType.BOLD)
        node2 = TextNode("This is a TextNode", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq3(self):
        node = TextNode("This is a TextNode", TextType.ITALIC)
        node2 = TextNode("This is a TextNode", TextType.ITALIC)
        self.assertEqual(node, node2)
    
    def test_eq4(self):
        node = TextNode("This is a TextNode", TextType.CODE)
        node2 = TextNode("This is a TextNode", TextType.CODE)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a TextNode", TextType.TEXT)
        node2 = TextNode("This is a TextNode", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a TextNode", TextType.TEXT)
        self.assertEqual(node.__repr__(), "TextNode(This is a TextNode, text, None)")
    
    def test_repr2(self):
        node = TextNode("This is a TextNode", TextType.BOLD)
        self.assertEqual(node.__repr__(), "TextNode(This is a TextNode, bold, None)")
    
    def test_repr3(self):
        node = TextNode("This is a TextNode", TextType.CODE)
        self.assertEqual(node.__repr__(), "TextNode(This is a TextNode, code, None)")
    
    def test_repr4(self):
        node = TextNode("This is a TextNode", TextType.ITALIC)
        self.assertEqual(node.__repr__(), "TextNode(This is a TextNode, italic, None)")
   
    def test_repr5(self):
        node = TextNode("This is a TextNode", TextType.TEXT, "#")
        self.assertEqual(node.__repr__(), "TextNode(This is a TextNode, text, #)")



if __name__ == "__main__":
    unittest.main()
