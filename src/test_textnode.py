import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode

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

    def test_textnode_to_html(self):
        textnode = TextNode("This is a text", TextType.TEXT)
        htmlnode = text_node_to_html_node(textnode)
        
        assert isinstance(htmlnode, LeafNode)

        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, "This is a text")

    def test_textnode_to_html2(self):
        textnode = TextNode("This is a bold", TextType.BOLD)
        htmlnode = text_node_to_html_node(textnode) 
        
        assert isinstance(htmlnode, LeafNode)
        
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode.to_html(), "<b>This is a bold</b>")

    def test_textnode_to_html3(self):
        textnode = TextNode("This is an italic", TextType.ITALIC)
        htmlnode = text_node_to_html_node(textnode)
        
        assert isinstance(htmlnode, LeafNode)
        
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode.to_html(), "<i>This is an italic</i>")

    def test_textnode_to_html4(self):
        textnode = TextNode("This is a code", TextType.CODE)
        htmlnode = text_node_to_html_node(textnode)
        
        assert isinstance(htmlnode, LeafNode)
        
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode.to_html(), "<code>This is a code</code>")

    def test_textnode_to_html5(self):
        textnode = TextNode("This is a link", TextType.LINK, "#")
        htmlnode = text_node_to_html_node(textnode)
        
        assert isinstance(htmlnode, LeafNode)
        
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode.to_html(), '<a href="#">This is a link</a>')

    def test_textnode_to_html6(self):
        textnode = TextNode("This is an image", TextType.IMAGE, "/")
        htmlnode = text_node_to_html_node(textnode)
        
        assert isinstance(htmlnode, LeafNode)
        
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode.to_html(), '<img src="/" alt="This is an image"></img>')



if __name__ == "__main__":
    unittest.main()
