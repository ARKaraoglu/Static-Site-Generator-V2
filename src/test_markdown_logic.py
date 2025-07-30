import unittest
from textnode import TextNode, TextType
from markdown_logic import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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
        self.maxDiff = None
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
            split_nodes = split_nodes_delimiter([child], "**", TextType.BOLD)

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


if __name__ == "__main__":
    unittest.main()
