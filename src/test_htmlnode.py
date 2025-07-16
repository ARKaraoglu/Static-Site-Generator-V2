import unittest
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        textnode = TextNode("This is a textnode", TextType.ITALIC, "/")
        node = HTMLNode(tag = "html", value = "3", children = [textnode], props = {"href":"/"})
        self.assertEqual(node.__repr__(), "HTMLNode(html, 3, [TextNode(This is a textnode, italic, /)], {'href': '/'})")

    def test_repr2(self):
        node = HTMLNode(tag = "html", value = "3", children = None, props = None)
        self.assertEqual(node.__repr__(), "HTMLNode(html, 3, None, None)")

    def test_repr3(self):
        node = HTMLNode(None, "3", None, None)
        self.assertEqual(node.__repr__(), "HTMLNode(None, 3, None, None)")

    def test_repr4(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.__repr__(), "HTMLNode(None, None, None, None)")

    def test_props_to_html(self):
        node = HTMLNode("html", None, None, props = {"href":"/", "src":"src"})
        self.assertEqual(node.props_to_html(), " href=/ src=src")

    def test_props_to_html2(self):
        node = HTMLNode("html", None, None, props = None)
        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        node = HTMLNode("html", None, None, props = None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        leafnode = LeafNode("p", "This is a leafnode")
        self.assertTrue(leafnode)

    def test_init2(self):
        leafnode = LeafNode("b", "This is a leafnode", {"href": "/"})
        self.assertTrue(leafnode)

    def test_to_html(self):
        node = LeafNode("p", "This is a leafnode")
        self.assertEqual(node.to_html(), "<p>This is a leafnode</p>")

    def test_to_html2(self):
        node = LeafNode("b", "This is a leafnode", {"href": "/"})
        self.assertEqual(node.to_html(), '<b href=/>This is a leafnode</b>')





if __name__ == "__main__":
    unittest.main()
