import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
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
        self.assertEqual(node.props_to_html(), ' href="/" src="src"')

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
        self.assertEqual(node.to_html(), '<b href="/">This is a leafnode</b>')


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        child1 = LeafNode("p", "This is a leafnode")
        child2 = LeafNode("b", "This is a leafnode with b tag", {"href": "#"})
        child3 = LeafNode("i", "This is an italic leafnode")
        parentnode = ParentNode("div", [child1, child2, child3], {"src": "/"})
        
        self.assertEqual(parentnode.__repr__(), "ParentNode(div, [LeafNode(p, This is a leafnode, None), LeafNode(b, This is a leafnode with b tag, {'href': '#'}), LeafNode(i, This is an italic leafnode, None)], {'src': '/'})")

    def test_to_html(self):
        child1 = LeafNode("p", "This is a paragraph")
        child2 = ParentNode("div", [child1], {"href": "#", "src": "/"})
        child3 = LeafNode("b", "This is a bold text")
        child4 = LeafNode("i", "This is italic text")

        parent = ParentNode("div", [child2, child3, child4])

        self.assertEqual(parent.to_html(), '<div><div href="#" src="/"><p>This is a paragraph</p></div><b>This is a bold text</b><i>This is italic text</i></div>')
        

    def test_to_html2(self):
        parent = ParentNode("div", [])

        self.assertEqual(parent.to_html(), "<div></div>")

    def test_to_html3(self):
        parent1 = ParentNode("p", [], {"href": "/", "src": "#", "None": "None", "yo": "yo"})
        parent2 = ParentNode("div", [parent1])

        self.assertEqual(parent2.to_html(), '<div><p href="/" src="#" None="None" yo="yo"></p></div>')


    def test_to_html4(self):
        child1 = LeafNode("p", "LeafNode")
        parent1 = ParentNode("span", [child1])
        parent2 = ParentNode("div", [parent1])
        parent3 = ParentNode("html", [parent2])

        self.assertEqual(parent3.to_html(), "<html><div><span><p>LeafNode</p></span></div></html>")














if __name__ == "__main__":
    unittest.main()
