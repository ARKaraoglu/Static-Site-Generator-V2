import unittest
from textnode import TextNode, TextType
from markdown_logic import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_1_child(self):
        child = TextNode("This is a regular textnode with **bold** text in it.", TextType.TEXT)
        node_list = split_nodes_delimiter([child], "**", TextType.BOLD)
        self.assertEqual(node_list, [TextNode("This is a regular textnode with ", TextType.TEXT, None), TextNode("bold", TextType.BOLD, None), TextNode(" text in it.", TextType.TEXT, None)])

    def test_split_nodes_delimiter_multi_child_bold(self):
        child = TextNode("This is a regular textnode with **bold and bolder** text in it.", TextType.TEXT)
        child2 = TextNode("Node with **italic**", TextType.TEXT)
        child3 = TextNode("**BOLD** word in the beginning", TextType.TEXT)
        node_list = split_nodes_delimiter([child, child2, child3], "**", TextType.BOLD)
        self.assertEqual(node_list, [TextNode("This is a regular textnode with ", TextType.TEXT,None),TextNode("bold and bolder", TextType.BOLD,None),TextNode(" text in it.", TextType.TEXT,None),TextNode("Node with ", TextType.TEXT,None),TextNode("italic", TextType.BOLD,None),TextNode("BOLD", TextType.BOLD,None),TextNode(" word in the beginning", TextType.TEXT,None)])

    def test_split_nodes_delimiter_multi_child_italic(self):
        child = TextNode("This is a regular textnode with _bold and bolder_text in it.", TextType.TEXT)
        child2 = TextNode("Node with _italic_", TextType.TEXT)
        child3 = TextNode("_ITALIC_ word in the beginning", TextType.TEXT)
        child4 = TextNode("_this is a node with only italic text_", TextType.TEXT)
        node_list = split_nodes_delimiter([child, child2, child3, child4], "_", TextType.ITALIC)
        self.assertEqual(node_list, [TextNode("This is a regular textnode with ", TextType.TEXT,None),TextNode("bold and bolder", TextType.ITALIC,None),TextNode("text in it.", TextType.TEXT,None),TextNode("Node with ", TextType.TEXT,None),TextNode("italic", TextType.ITALIC,None),TextNode("ITALIC", TextType.ITALIC,None),TextNode(" word in the beginning", TextType.TEXT,None), TextNode("this is a node with only italic text", TextType.ITALIC, None)])

    def test_split_nodes_delimiter_multi_child_code(self):
        child = TextNode("This is a regular textnode with `<p>there is code here</p>` text in it.", TextType.TEXT)
        child2 = TextNode("Node with `code`", TextType.TEXT)
        child3 = TextNode("`Code` word in the beginning", TextType.TEXT)
        child4 = TextNode("`<html><div><p>THIS IS CODE TEXT</p></div></html>`", TextType.TEXT)
        node_list = split_nodes_delimiter([child, child2, child3, child4], "`", TextType.CODE)
        self.assertEqual(node_list, [TextNode("This is a regular textnode with ", TextType.TEXT,None),TextNode("<p>there is code here</p>", TextType.CODE,None),TextNode(" text in it.", TextType.TEXT,None),TextNode("Node with ", TextType.TEXT,None),TextNode("code", TextType.CODE,None),TextNode("Code", TextType.CODE,None),TextNode(" word in the beginning", TextType.TEXT,None), TextNode("<html><div><p>THIS IS CODE TEXT</p></div></html>", TextType.CODE, None)])

    def test_split_nodes_delimiter_mix_text_types(self):
        child1 = TextNode("This is of text type with **bold** word in it.", TextType.TEXT)
        child2 = TextNode("This is a bold node", TextType.BOLD)
        child3 = TextNode("This is the second text type child with _italic_ word in it!", TextType.TEXT)
        child4 = TextNode("Italic word", TextType.ITALIC)
        child5 = TextNode("<p>code</p>", TextType.CODE)
        child6 = TextNode("This is the last textnode with `code` and **bold**", TextType.TEXT)
        node_list = split_nodes_delimiter([child1, child2, child3, child4, child5, child6], "**", TextType.BOLD)
        self.assertEqual(node_list, [TextNode("This is of text type with ", TextType.TEXT,None),TextNode("bold", TextType.BOLD,None),TextNode(" word in it.", TextType.TEXT,None),TextNode("This is a bold node", TextType.BOLD,None),TextNode("This is the second text type child with _italic_ word in it!", TextType.TEXT,None),TextNode("Italic word", TextType.ITALIC,None),TextNode("<p>code</p>", TextType.CODE,None),TextNode("This is the last textnode with `code` and ", TextType.TEXT,None),TextNode("bold", TextType.BOLD,None)])

    def test_split_nodes_delimiter_non_matching_delimiter(self):
        child = TextNode("This is a **bold text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([child], "**", TextType.BOLD)

    def test_split_delimiter_bold_and_italic(self):
        child = TextNode("**Bold** and _italic_ text.", TextType.TEXT)
        node_list = split_nodes_delimiter([child], "**", TextType.BOLD)
        node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
        self.assertEqual(node_list, [TextNode("Bold", TextType.BOLD, None), TextNode(" and ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None), TextNode(" text.", TextType.TEXT, None)])



class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_image1(self):
        text = "Here is the ![image](https://url)"
        image_list = extract_markdown_images(text)
        self.assertListEqual(image_list, [("image", "https://url")])

    def test_extract_markdown_image2(self):
        text = "![image in front](https://url) image is in the front of the sentence."
        image_list = extract_markdown_images(text)
        self.assertListEqual(image_list, [("image in front", "https://url")])

    def test_extract_markdown_image_multiple1(self):
        text = "This is a sentence with ![image one](/) and another image at the end![image two](/)"
        image_list = extract_markdown_images(text)
        self.assertListEqual(image_list, [("image one", "/"),("image two", "/")])

    def test_extract_markdown_image_multiple2(self):
        text = "![image three](#)This is a ![image four]() sentence with ![image one](/) and another image at the end![image two](/)"
        image_list = extract_markdown_images(text)
        self.assertListEqual(image_list, [("image three", "#"), ("image four", ""), ("image one", "/"), ("image two", "/")])
    
    def test_extract_markdown_image_no_image(self):
        text = "[link](url), no image!"
        image_list = extract_markdown_images(text)
        self.assertListEqual(image_list, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links1(self):
        text = "Here is the [anchor text for link](/)"
        link_list = extract_markdown_links(text)
        self.assertListEqual(link_list, [("anchor text for link", "/")])

    def test_extract_markdown_links2(self):
        text = "[link](href://#) Link at the start"
        link_list = extract_markdown_links(text)
        self.assertListEqual(link_list, [("link", "href://#")])
    
    def test_extract_markdown_links_multiple1(self):
        text = "Here is the [link 1](/) and [link two](/)"
        link_list = extract_markdown_links(text)
        self.assertListEqual(link_list, [("link 1", "/"), ("link two", "/")])
    
    def test_extract_markdown_links_multiple2(self):
        text = "This [Link one](/) sentence have [link two](#) four [anchor text for link](/) links in it! [final link](/)"
        link_list = extract_markdown_links(text)
        self.assertListEqual(link_list, [("Link one", "/"), ("link two", "#"), ("anchor text for link", "/"), ("final link", "/")])
    
    def test_extract_markdown_links_no_link(self):
        text = "Here is the ![anchor text for link](/)"
        link_list = extract_markdown_links(text)
        self.assertListEqual(link_list, [])


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image1(self):
        text = "This is a **bold** text with an image at the end ![image](image url)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertListEqual(split_nodes, [TextNode("This is a **bold** text with an image at the end ", TextType.TEXT), TextNode("image", TextType.IMAGE, "image url")])

    def test_split_nodes_image2(self):
        text = "![image](image url) This is a **bold** text with an image at the start."
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertListEqual(split_nodes, [TextNode("image", TextType.IMAGE, "image url"), TextNode(" This is a **bold** text with an image at the start.", TextType.TEXT)])

    def test_split_nodes_image3(self):
        text = "This is a **bold** text with ![image](image url) an image at _italic_ the middle."
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertListEqual(split_nodes, [TextNode("This is a **bold** text with ", TextType.TEXT), TextNode("image", TextType.IMAGE, "image url"), TextNode(" an image at _italic_ the middle.", TextType.TEXT)])

    def test_split_nodes_image4(self):
        text = "![image 1](image)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertListEqual(split_nodes, [TextNode("image 1", TextType.IMAGE, "image")])

    def test_split_nodes_image_multiple_image(self):
        text = "![image 1](image 1) This text have ![image 2]( http://www.google.com ) 3 images in total ![image 3](image 3)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertListEqual(split_nodes, [TextNode("image 1", TextType.IMAGE, "image 1"),TextNode(" This text have ", TextType.TEXT),TextNode("image 2", TextType.IMAGE, " http://www.google.com "),TextNode(" 3 images in total ",TextType.TEXT),TextNode("image 3", TextType.IMAGE, "image 3")])

    def test_split_nodes_image_no_image(self):
        text = "[image 1](image 1) This text have [image 2]( http://www.google.com ) 3 images in total [image 3](image 3)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_image([node])
        self.assertListEqual(split_nodes, [TextNode("[image 1](image 1) This text have [image 2]( http://www.google.com ) 3 images in total [image 3](image 3)", TextType.TEXT)])

    def test_split_nodes_image_multi_children(self):
        node1 = TextNode("This is ![image](image source) a textnode [link](link url)", TextType.TEXT)
        node2 = TextNode("![image 2](image source)", TextType.TEXT)
        node3 = TextNode("[link](#)", TextType.TEXT)
        node4 = TextNode("![image 3](/)", TextType.BOLD)
        node5 = TextNode("image", TextType.IMAGE, "src")
        split_nodes = split_nodes_image([node1, node2, node3, node4, node5])
        self.assertListEqual(split_nodes, [TextNode("This is ", TextType.TEXT),TextNode("image", TextType.IMAGE, "image source"),TextNode(" a textnode [link](link url)", TextType.TEXT),TextNode("image 2", TextType.IMAGE, "image source"),TextNode("[link](#)", TextType.TEXT),TextNode("![image 3](/)", TextType.BOLD),TextNode("image", TextType.IMAGE, "src")])

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link1(self):
        text = "[link1](src=/)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertListEqual(split_nodes, [TextNode("link1", TextType.LINK, "src=/")])

    def test_split_nodes_link2(self):
        text = "There is a link at the end [link](url)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertListEqual(split_nodes, [TextNode("There is a link at the end ", TextType.TEXT), TextNode("link", TextType.LINK, "url")])

    def test_split_nodes_link3(self):
        text = "There is a [link](url) link in the middle."
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertListEqual(split_nodes, [TextNode("There is a ", TextType.TEXT), TextNode("link", TextType.LINK, "url"), TextNode(" link in the middle.", TextType.TEXT)])

    def test_split_nodes_link4(self):
        text = "[link](url) There is a link in the beginning"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertListEqual(split_nodes, [TextNode("link", TextType.LINK, "url"), TextNode(" There is a link in the beginning", TextType.TEXT)])

    def test_split_nodes_link_multi_link(self):
        text = "[link 1](url 1) There **is** multiple [link 2](url 2) links _in_ this node. [link 3](url 3)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertListEqual(split_nodes, [TextNode("link 1", TextType.LINK, "url 1"), TextNode(" There **is** multiple ", TextType.TEXT), TextNode("link 2", TextType.LINK, "url 2"), TextNode(" links _in_ this node. ", TextType.TEXT), TextNode("link 3", TextType.LINK, "url 3")])

    def test_split_nodes_link_no_link(self):
        text = "There is no link in this text except an image ![image](image url)"
        node = TextNode(text, TextType.TEXT)
        split_nodes = split_nodes_link([node])
        self.assertListEqual(split_nodes, [TextNode("There is no link in this text except an image ![image](image url)", TextType.TEXT)])




if __name__ == "__main__":
    unittest.main()
