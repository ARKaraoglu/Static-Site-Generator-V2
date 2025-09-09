import unittest
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode
from markdown_logic import tokenizer, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnode, markdown_to_html

class TestTokenizer(unittest.TestCase):
    def test_tokenizer_text(self):
        textnode = TextNode("This is a paragraph textnode", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is a paragraph textnode)"]])

    def test_tokenizer_bold(self):
        textnode = TextNode("This is a textnode with **bold** text in it", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is a textnode with )", "star", "star", "text(bold)", "star", "star", "text( text in it)"]])
    
    def test_tokenizer_multi_bold(self):
        textnode = TextNode("This is a **textnode** with **bold** text in it", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is a )", "star", "star", "text(textnode)", "star", "star", "text( with )", "star", "star", "text(bold)", "star", "star", "text( text in it)"]])
    
    def test_tokenizer_italic(self):
        textnode = TextNode("This is a textnode with *bold* text in it", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is a textnode with )", "star", "text(bold)", "star", "text( text in it)"]])
    
    def test_tokenizer_multi_italic(self):
        textnode = TextNode("This is a *textnode* with *bold* text in it", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is a )", "star", "text(textnode)", "star", "text( with )", "star", "text(bold)", "star", "text( text in it)"]])
   
    def test_tokenizer_bold_underscore(self):
        textnode = TextNode("This sentence has __bold text__ made with underscores", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This sentence has )", "underscore", "underscore", "text(bold text)", "underscore", "underscore", "text( made with underscores)"]])

    def test_tokenizer_italic_underscore(self):
        textnode = TextNode("This sentence has _bold text_ made with underscores", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This sentence has )", "underscore", "text(bold text)", "underscore", "text( made with underscores)"]])

    def test_tokenizer_code(self):
        textnode = TextNode("This is a node with `code` inline markdown in it", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is a node with )", "code", "text(code)", "code", "text( inline markdown in it)"]])

    def test_tokenizer_multi_code(self):
        textnode = TextNode("This is a `textnode` with `code` inline markdown in it", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is a )", "code", "text(textnode)", "code", "text( with )", "code", "text(code)", "code", "text( inline markdown in it)"]])
    
    def test_tokenizer_multi_type(self):
        textnode = TextNode("This is **bold**, this is _italic_, and this is `inline code`.", TextType.TEXT)
        tokens = tokenizer([textnode])
        self.assertEqual(tokens, [["text(This is )", "star", "star", "text(bold)", "star", "star", "text(, this is )", "underscore", "text(italic)", "underscore", "text(, and this is )", "code", "text(inline code)", "code", "text(.)"]])

    def test_tokenizer_multi_nodes(self):
        textnode1 = TextNode("This is a **textnode** with **bold** text in it", TextType.TEXT)
        textnode2 = TextNode("This is a *textnode* with *bold* text in it", TextType.TEXT)
        textnode3 = TextNode("This sentence has __bold text__ made with underscores", TextType.TEXT)
        textnode4 = TextNode("This is a node with `code` inline markdown in it", TextType.TEXT)
        textnode5 = TextNode("This is a `textnode` with `code` inline markdown in it", TextType.TEXT)
        textnode6 = TextNode("This is **bold**, this is _italic_, and this is `inline code`.", TextType.TEXT)
        textnode7 = TextNode("This is a paragraph textnode", TextType.TEXT)

        tokens = tokenizer([textnode1, textnode2, textnode3, textnode4, textnode5, textnode6, textnode7])
        self.assertEqual(tokens, [
            ["text(This is a )", "star", "star", "text(textnode)", "star", "star", "text( with )", "star", "star", "text(bold)", "star", "star", "text( text in it)"],
            ["text(This is a )", "star", "text(textnode)", "star", "text( with )", "star", "text(bold)", "star", "text( text in it)"],
            ["text(This sentence has )", "underscore", "underscore", "text(bold text)", "underscore", "underscore", "text( made with underscores)"],
            ["text(This is a node with )", "code", "text(code)", "code", "text( inline markdown in it)"],
            ["text(This is a )", "code", "text(textnode)", "code", "text( with )", "code", "text(code)", "code", "text( inline markdown in it)"],
            ["text(This is )", "star", "star", "text(bold)", "star", "star", "text(, this is )", "underscore", "text(italic)", "underscore", "text(, and this is )", "code", "text(inline code)", "code", "text(.)"],
            ["text(This is a paragraph textnode)"]
        ])



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

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode_bold(self):
        text = "There is a **bold** text in this text."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("There is a ", TextType.TEXT),TextNode("bold", TextType.BOLD),TextNode(" text in this text.", TextType.TEXT)])
    
    def test_text_to_textnode_multi_bold(self):
        text = "The **sunset** painted the sky in shades of **crimson**, orange, and gold. A **cool breeze** drifted across the **field**, carrying the scent of **freshly cut** grass. Somewhere in the **distance**, a **lone bird** sang, its voice **echoing** through the trees. The **path** ahead was **narrow**, winding between **ancient** oaks and **whispering** pines. Every step felt **lighter**, as though the **world** had paused to **breathe**."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("The ", TextType.TEXT), TextNode("sunset", TextType.BOLD),TextNode(" painted the sky in shades of ", TextType.TEXT),TextNode("crimson", TextType.BOLD),TextNode(", orange, and gold. A ", TextType.TEXT),TextNode("cool breeze", TextType.BOLD),TextNode(" drifted across the ", TextType.TEXT),TextNode("field", TextType.BOLD),TextNode(", carrying the scent of ", TextType.TEXT),TextNode("freshly cut", TextType.BOLD),TextNode(" grass. Somewhere in the ", TextType.TEXT),TextNode("distance", TextType.BOLD),TextNode(", a ", TextType.TEXT),TextNode("lone bird", TextType.BOLD),TextNode(" sang, its voice ", TextType.TEXT),TextNode("echoing", TextType.BOLD),TextNode(" through the trees. The ", TextType.TEXT),TextNode("path", TextType.BOLD),TextNode(" ahead was ", TextType.TEXT),TextNode("narrow", TextType.BOLD),TextNode(", winding between ", TextType.TEXT),TextNode("ancient", TextType.BOLD),TextNode(" oaks and ", TextType.TEXT),TextNode("whispering", TextType.BOLD),TextNode(" pines. Every step felt ", TextType.TEXT),TextNode("lighter", TextType.BOLD),TextNode(", as though the ", TextType.TEXT),TextNode("world", TextType.BOLD),TextNode(" had paused to ", TextType.TEXT),TextNode("breathe", TextType.BOLD), TextNode(".", TextType.TEXT)])

    def test_text_to_textnode_italic(self):
        text = "There is an _italic_ word in this text."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("There is an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word in this text.", TextType.TEXT)])

    def test_text_to_textnode_multi_italic(self):
        text = "The _sunset_ spread across the _horizon_ in waves of orange and gold, while a _soft breeze_ whispered through the _trees_. Somewhere beyond the _hills_, a _river_ glimmered under the fading _light_, and the _world_ seemed to _pause_ in quiet reflection."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("The ", TextType.TEXT),TextNode("sunset", TextType.ITALIC),TextNode(" spread across the ", TextType.TEXT),TextNode("horizon", TextType.ITALIC),TextNode(" in waves of orange and gold, while a ", TextType.TEXT),TextNode("soft breeze", TextType.ITALIC),TextNode(" whispered through the ", TextType.TEXT),TextNode("trees", TextType.ITALIC),TextNode(". Somewhere beyond the ", TextType.TEXT),TextNode("hills", TextType.ITALIC),TextNode(", a ", TextType.TEXT),TextNode("river", TextType.ITALIC),TextNode(" glimmered under the fading ", TextType.TEXT),TextNode("light", TextType.ITALIC),TextNode(", and the ", TextType.TEXT),TextNode("world", TextType.ITALIC), TextNode(" seemed to ", TextType.TEXT),TextNode("pause", TextType.ITALIC), TextNode(" in quiet reflection.", TextType.TEXT)])
    
    def test_text_to_textnode_code(self):
        text = "There is a `int main(){ return 0;}` word in this text."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("There is a ", TextType.TEXT), TextNode("int main(){ return 0;}", TextType.CODE), TextNode(" word in this text.", TextType.TEXT)])

    def test_text_to_textnode_multi_code(self):
        text = "I set `timeout=30` in the config, replaced `foo()` with `bar()`, updated `API-KEY`, and removed the unused `debug-mode`."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("I set ", TextType.TEXT), TextNode("timeout=30", TextType.CODE),TextNode(" in the config, replaced ", TextType.TEXT),TextNode("foo()", TextType.CODE),TextNode(" with ", TextType.TEXT),TextNode("bar()", TextType.CODE),TextNode(", updated ", TextType.TEXT),TextNode("API-KEY", TextType.CODE),TextNode(", and removed the unused ", TextType.TEXT),TextNode("debug-mode", TextType.CODE), TextNode(".", TextType.TEXT)])

    def test_text_to_textnode_image_and_link(self):
        text = "There is an ![image](image source) and [link](link url) in this text."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("There is an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "image source"), TextNode(" and ", TextType.TEXT), TextNode("link", TextType.LINK, "link url"), TextNode(" in this text.", TextType.TEXT)])

    def test_text_to_textnode_multi_image_and_link(self):
        text = "![Mountain Sunrise](https://example.com/mountain.jpg) The beauty of nature can inspire us in many ways, and you can learn more about mountain ranges [here](https://example.com/mountains). ![City Lights](https://example.com/city.jpg) Urban landscapes have their own kind of charm, and you can discover famous skylines [here](https://example.com/cities). ![Ocean Waves](https://example.com/ocean.jpg) The sea has always fascinated humanity, and you can read more about marine life [here](https://example.com/ocean-life)."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("Mountain Sunrise", TextType.IMAGE, "https://example.com/mountain.jpg"),TextNode(" The beauty of nature can inspire us in many ways, and you can learn more about mountain ranges ", TextType.TEXT),TextNode("here", TextType.LINK, "https://example.com/mountains"),TextNode(". ", TextType.TEXT),TextNode("City Lights", TextType.IMAGE, "https://example.com/city.jpg"),TextNode(" Urban landscapes have their own kind of charm, and you can discover famous skylines ", TextType.TEXT),TextNode("here", TextType.LINK, "https://example.com/cities"),TextNode(". ", TextType.TEXT),TextNode("Ocean Waves", TextType.IMAGE, "https://example.com/ocean.jpg"),TextNode(" The sea has always fascinated humanity, and you can read more about marine life ", TextType.TEXT),TextNode("here", TextType.LINK, "https://example.com/ocean-life"), TextNode(".", TextType.TEXT)])

    def test_text_to_textnode_multi_type(self):
        text = "The **sunset** painted the _horizon_ in warm colors, while the `camera` captured the moment perfectly ![Golden Hour](https://example.com/sunset.jpg). Later, I checked the details [here](https://example.com/photography) and learned how to adjust `exposure` for better shots. Walking into the city, the **lights** reflected on the _wet streets_ ![City Reflections](https://example.com/city.jpg), making me think about optimizing my `render-lights()` function, which I read about [here](https://example.com/code-tips). Finally, standing by the _shore_, the **waves** rolled in rhythm ![Ocean Waves](https://example.com/ocean.jpg), and I logged the sound frequency using `analyze-wave()` from the guide [here](https://example.com/ocean-research)."
        split_nodes = text_to_textnode(text)
        self.assertListEqual(split_nodes, [TextNode("The ", TextType.TEXT),TextNode("sunset", TextType.BOLD),TextNode(" painted the ", TextType.TEXT),TextNode("horizon", TextType.ITALIC),TextNode(" in warm colors, while the ", TextType.TEXT),TextNode("camera", TextType.CODE),TextNode(" captured the moment perfectly ", TextType.TEXT),TextNode("Golden Hour", TextType.IMAGE, "https://example.com/sunset.jpg"),TextNode(". Later, I checked the details ", TextType.TEXT),TextNode("here", TextType.LINK, "https://example.com/photography"),TextNode(" and learned how to adjust ", TextType.TEXT),TextNode("exposure", TextType.CODE),TextNode(" for better shots. Walking into the city, the ", TextType.TEXT),TextNode("lights", TextType.BOLD),TextNode(" reflected on the ", TextType.TEXT),TextNode("wet streets", TextType.ITALIC),TextNode("City Reflections", TextType.IMAGE, "https://example.com/city.jpg"),TextNode(", making me think about optimizing my ", TextType.TEXT),TextNode("render-lights()", TextType.CODE),TextNode(" function, which I read about ", TextType.TEXT),TextNode("here", TextType.LINK, "https://example.com/code-tips"),TextNode(". Finally, standing by the ", TextType.TEXT),TextNode("shore", TextType.ITALIC),TextNode(", the ", TextType.TEXT),TextNode("waves", TextType.BOLD),TextNode(" rolled in rhythm ", TextType.TEXT),TextNode("Ocean Waves", TextType.IMAGE, "https://example.com/ocean.jpg"),TextNode(", and I logged the sound frequency using ", TextType.TEXT),TextNode("analyze-wave()", TextType.CODE),TextNode(" from the guide ", TextType.TEXT),TextNode("here", TextType.LINK, "https://example.com/ocean-research"),TextNode(".", TextType.TEXT)])



class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraph_block(self):
        block = """
The forest stretched endlessly before us
"""
        html = markdown_to_html(block)
        self.assertEqual(html.__repr__(), "ParentNode(div, [ParentNode(p, [LeafNode(None, The forest stretched endlessly before us, None)], None)], None)")
        self.assertEqual(html.to_html(),"<div><p>The forest stretched endlessly before us</p></div>")
    
    def test_paragraph_block_multi_lines(self):
        self.maxDiff = None

        block = """
The forest stretched endlessly before us
its canopy a dense roof of green that filtered the sunlight into shifting patterns on the mossy ground
"""
        html = markdown_to_html(block)
        self.assertEqual(html.__repr__(), "ParentNode(div, [ParentNode(p, [LeafNode(None, The forest stretched endlessly before us<br>, None), LeafNode(None, its canopy a dense roof of green that filtered the sunlight into shifting patterns on the mossy ground, None)], None)], None)")
        self.assertEqual(html.to_html(),"<div><p>The forest stretched endlessly before us<br>its canopy a dense roof of green that filtered the sunlight into shifting patterns on the mossy ground</p></div>")

    def test_paragraph_block_multi_lines2(self):
        block = """
The forest stretched endlessly before us
its canopy a dense roof of green that filtered the sunlight into shifting patterns on the mossy ground
the air carried the faint scent of pine and damp earth
a distant bird call echoed softly through the trees
while the leaves rustled gently in the passing breeze
"""
        html = markdown_to_html(block)
        
        test_leafnode1 = LeafNode(None, "The forest stretched endlessly before us<br>")
        test_leafnode2 = LeafNode(None, "its canopy a dense roof of green that filtered the sunlight into shifting patterns on the mossy ground<br>")
        test_leafnode3 = LeafNode(None, "the air carried the faint scent of pine and damp earth<br>")
        test_leafnode4 = LeafNode(None, "a distant bird call echoed softly through the trees<br>")
        test_leafnode5 = LeafNode(None, "while the leaves rustled gently in the passing breeze")
        test_p_element = ParentNode("p", [test_leafnode1, test_leafnode2, test_leafnode3, test_leafnode4, test_leafnode5])
        test_html = ParentNode("div", [test_p_element])
        self.assertEqual(html, test_html)


    def test_paragraph_block_single_line_multi_inline_markdown(self):
        block = """
The **forest** _stretched_ `endlessly before` us.
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "The ")
        test_leafnode2 = LeafNode("b", "forest")
        test_leafnode3 = LeafNode("i", "stretched")
        test_leafnode4 = LeafNode("code", "endlessly before")
        test_leafnode5 = LeafNode(None, " us.")
        test_p_element = ParentNode("p", [test_leafnode1, test_leafnode2, test_leafnode3, test_leafnode4, test_leafnode5])
        test_html = ParentNode("div", [test_p_element])
        self.assertEqual(html, test_html)



    def test_paragraph_block_multi_line_multi_inline_markdown(self):
        block = """
The **forest** stretched endlessly before us with its _mystery_
its canopy a _dense roof_ of green that filtered the sunlight into shifting patterns on the `mossy ground`
the air carried the faint scent of **pine** and damp earth like a `whisper`
a distant bird call echoed softly through the _trees_
while the leaves rustled gently in the passing `breeze` beneath the **sky**
"""
        html = markdown_to_html(block)
        
        test_leafnodes1 = LeafNode(None, "The ")
        test_leafnodes2 = LeafNode("b", "forest")
        test_leafnodes3 = LeafNode(None, " stretched endlessly before us with its ")
        test_leafnodes4 = LeafNode("i", "mystery")
        test_leafnodes20 = LeafNode(None, "<br>")
        test_leafnodes5 = LeafNode(None, "its canopy a ")
        test_leafnodes6 = LeafNode("i", "dense roof")
        test_leafnodes7 = LeafNode(None, " of green that filtered the sunlight into shifting patterns on the ")
        test_leafnodes8 = LeafNode("code", "mossy ground")
        test_leafnodes21 = LeafNode(None, "<br>")
        test_leafnodes9 = LeafNode(None, "the air carried the faint scent of ")
        test_leafnodes10 = LeafNode("b", "pine")
        test_leafnodes11 = LeafNode(None, " and damp earth like a ")
        test_leafnodes12 = LeafNode("code", "whisper")
        test_leafnodes22 = LeafNode(None, "<br>")
        test_leafnodes13 = LeafNode(None, "a distant bird call echoed softly through the ")
        test_leafnodes14 = LeafNode("i", "trees")
        test_leafnodes15 = LeafNode(None, "<br>")
        test_leafnodes16 = LeafNode(None, "while the leaves rustled gently in the passing ")
        test_leafnodes17 = LeafNode("code", "breeze")
        test_leafnodes18 = LeafNode(None, " beneath the ")
        test_leafnodes19 = LeafNode("b", "sky")
        test_p_element = ParentNode("p", [
            test_leafnodes1, 
            test_leafnodes2,
            test_leafnodes3,
            test_leafnodes4,
            test_leafnodes20,
            test_leafnodes5,
            test_leafnodes6,
            test_leafnodes7,
            test_leafnodes8,
            test_leafnodes21,
            test_leafnodes9,
            test_leafnodes10,
            test_leafnodes11,
            test_leafnodes12,
            test_leafnodes22,
            test_leafnodes13,
            test_leafnodes14,
            test_leafnodes15,
            test_leafnodes16,
            test_leafnodes17,
            test_leafnodes18,
            test_leafnodes19
        ])
        test_html = ParentNode("div", [test_p_element])
        self.assertEqual(html, test_html)


    def test_heading_block_h1(self):
        block = """
# Heading 1
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "Heading 1")
        test_heading_element = ParentNode("h1", [test_leafnode1])
        test_html = ParentNode("div", [test_heading_element])
        self.assertEqual(html, test_html)

    def test_heading_block_h2(self):
        block = """
## Heading 2
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "Heading 2")
        test_heading_element = ParentNode("h2", [test_leafnode1])
        test_html = ParentNode("div", [test_heading_element])
        self.assertEqual(html, test_html)
    

    def test_heading_block_h3(self):
        block = """
### Heading 3
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "Heading 3")
        test_heading_element = ParentNode("h3", [test_leafnode1])
        test_html = ParentNode("div", [test_heading_element])
        self.assertEqual(html, test_html)
    

    def test_heading_block_h4(self):
        block = """
#### Heading 4
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "Heading 4")
        test_heading_element = ParentNode("h4", [test_leafnode1])
        test_html = ParentNode("div", [test_heading_element])
        self.assertEqual(html, test_html)

    def test_heading_block_h5(self):
        block = """
##### Heading 5
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "Heading 5")
        test_heading_element = ParentNode("h5", [test_leafnode1])
        test_html = ParentNode("div", [test_heading_element])
        self.assertEqual(html, test_html)
    
    def test_heading_block_h6(self):
        block = """
###### Heading 6
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "Heading 6")
        test_heading_element = ParentNode("h6", [test_leafnode1])
        test_html = ParentNode("div", [test_heading_element])
        self.assertEqual(html, test_html)
    
    def test_heading_block_h3_multi_inline_markdown(self):
        block = """
### _This_ is a **Heading 3** with 3 `inline markdowns`
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode("i", "This")
        test_leafnode2 = LeafNode(None, " is a ")
        test_leafnode3 = LeafNode("b", "Heading 3")
        test_leafnode4 = LeafNode(None, " with 3 ")
        test_leafnode5 = LeafNode("code", "inline markdowns")
        test_heading_element = ParentNode("h3", [test_leafnode1, test_leafnode2, test_leafnode3, test_leafnode4, test_leafnode5])
        test_html = ParentNode("div", [test_heading_element])
        self.assertEqual(html, test_html)
    
    def test_code_block(self):
        block = """```
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");

    int x = 10;
    int y = 20;
    printf("Sum: %d\n", x + y);

    return 0;
}
```
"""
        html = markdown_to_html(block)
        test_leafnode1 = LeafNode("code", """#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");

    int x = 10;
    int y = 20;
    printf("Sum: %d\n", x + y);

    return 0;
}
"""
)
        test_code_element = ParentNode("pre", [test_leafnode1])
        test_html = ParentNode("div", [test_code_element])
        self.assertEqual(html, test_html)
   

    def test_code_block_incorrect(self):
        block = """```
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");

    int x = 10;
    int y = 20;
    printf("Sum: %d\n", x + y);

    return 0;
}
```
"""
        html = markdown_to_html(block)
        test_leafnode1 = LeafNode("code", """
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");

    int x = 10;
    int y = 20;
    printf("Sum: %d\n", x + y);

    return 0;}
"""
)
        test_code_element = ParentNode("pre", [test_leafnode1])
        test_html = ParentNode("div", [test_code_element])
        self.assertNotEqual(html, test_html)
   


    def test_quote_block(self):
        block = """
> quote 1
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "quote 1")
        test_paragraph_element = ParentNode("p", [test_leafnode1])
        test_quote_element = ParentNode("blockquote", [test_paragraph_element])
        test_html = ParentNode("div", [test_quote_element])
        self.assertEqual(html, test_html)

    def test_quote_block_multi_line(self):
        block = """
> quote 1
> quote 2
> quote 3
> quote 4
> quote 5
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "quote 1<br>")
        test_leafnode2 = LeafNode(None, "quote 2<br>")
        test_leafnode3 = LeafNode(None, "quote 3<br>")
        test_leafnode4 = LeafNode(None, "quote 4<br>")
        test_leafnode5 = LeafNode(None, "quote 5")
        test_paragraph_element = ParentNode("p", [test_leafnode1, test_leafnode2, test_leafnode3, test_leafnode4, test_leafnode5])
        test_quote_element = ParentNode("blockquote", [test_paragraph_element])
        test_html = ParentNode("div", [test_quote_element])
        self.assertEqual(html, test_html)
    
    def test_quote_block_multi_line_multi_inline_markdown(self):
        block = """
> This is a **bold** statement inside a quote
> Sometimes we use _italic_ text for emphasis
> You can even insert `inline code` within quotes
> Quotes can also contain [links](https://example.com)
> And even an ![image](https://via.placeholder.com/100) if you like
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "This is a ")
        test_leafnode2 = LeafNode("b", "bold")
        test_leafnode3 = LeafNode(None, " statement inside a quote<br>")
        test_leafnode4 = LeafNode(None, "Sometimes we use ")
        test_leafnode5 = LeafNode("i", "italic")
        test_leafnode6 = LeafNode(None, " text for emphasis<br>")
        test_leafnode7 = LeafNode(None, "You can even insert ")
        test_leafnode8 = LeafNode("code", "inline code")
        test_leafnode9 = LeafNode(None, " within quotes<br>")
        test_leafnode10 = LeafNode(None, "Quotes can also contain ")
        test_leafnode11 = LeafNode("a", "links", {"href": "https://example.com"})
        test_leafnode12 = LeafNode(None, "<br>")
        test_leafnode13 = LeafNode(None, "And even an ")
        test_leafnode14 = LeafNode("img", "", {"src": "https://via.placeholder.com/100", "alt": "image"})
        test_leafnode15 = LeafNode(None, " if you like")
        
        test_paragraph_element = ParentNode("p", [test_leafnode1, test_leafnode2, test_leafnode3, test_leafnode4, test_leafnode5, test_leafnode6, test_leafnode7, test_leafnode8, test_leafnode9, test_leafnode10, test_leafnode11, test_leafnode12, test_leafnode13, test_leafnode14, test_leafnode15 ])
        test_quote_element = ParentNode("blockquote", [test_paragraph_element])
        test_html = ParentNode("div", [test_quote_element])
        self.assertEqual(html, test_html)

    def test_quote_block_multi_line_plus_empty_line(self):
        block = """
> quote 1
> quote 2
> quote 3
> 
> 
> quote 4
> quote 5
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "quote 1<br>")
        test_leafnode2 = LeafNode(None, "quote 2<br>")
        test_leafnode3 = LeafNode(None, "quote 3<br>")
        test_leafnode4 = LeafNode(None, "<br>")
        test_leafnode5 = LeafNode(None, "<br>")
        test_leafnode6 = LeafNode(None, "quote 4<br>")
        test_leafnode7 = LeafNode(None, "quote 5")
        test_paragraph_element = ParentNode("p", [test_leafnode1, test_leafnode2, test_leafnode3, test_leafnode4, test_leafnode5, test_leafnode6, test_leafnode7])
        test_quote_element = ParentNode("blockquote", [test_paragraph_element])
        test_html = ParentNode("div", [test_quote_element])
        self.assertEqual(html, test_html)
    
    def test_unordered_list_block(self):
        block = """
- Unordered list item 1
"""
        html = markdown_to_html(block)

        test_leafnode1 = LeafNode(None, "Unordered list item 1")
        test_list_items = ParentNode("li", [test_leafnode1])
        test_ulist_element = ParentNode("ul", [test_list_items])
        test_html = ParentNode("div", [test_ulist_element])

        self.assertEqual(html, test_html)


    def test_unordered_list_block_multi_line(self):
        block = """
- Unordered list item 1
- Unordered list item 2
- Unordered list item 3
- Unordered list item 4
- Unordered list item 5
- Unordered list item 6
"""
        html = markdown_to_html(block)

        test_ln1 = LeafNode(None, "Unordered list item 1")
        test_ln2 = LeafNode(None, "Unordered list item 2")
        test_ln3 = LeafNode(None, "Unordered list item 3")
        test_ln4 = LeafNode(None, "Unordered list item 4")
        test_ln5 = LeafNode(None, "Unordered list item 5")
        test_ln6 = LeafNode(None, "Unordered list item 6")
        test_list_item1 = ParentNode("li", [test_ln1])
        test_list_item2 = ParentNode("li", [test_ln2])
        test_list_item3 = ParentNode("li", [test_ln3])
        test_list_item4 = ParentNode("li", [test_ln4])
        test_list_item5 = ParentNode("li", [test_ln5])
        test_list_item6 = ParentNode("li", [test_ln6])
        test_unordered_list_element = ParentNode("ul", [test_list_item1, test_list_item2, test_list_item3, test_list_item4, test_list_item5, test_list_item6])
        test_html = ParentNode("div", [test_unordered_list_element])
        self.assertEqual(html, test_html)

    def test_unordered_list_block_multi_line2(self):
        block = """
- **Unordered** list item 1
- Unordered list item with _italic_ text 2
- Unordered list item 3 and some `inline code`
- **Bold** and _italic_ mixed in list item 4
- Unordered list item 5 with a [link](https://example.com)
- Final item 6 with an ![image](https://via.placeholder.com/50)
"""
    
        html = markdown_to_html(block)

        test_ln1 = LeafNode("b", "Unordered")
        test_ln2 = LeafNode(None, " list item 1")
        test_ln3 = LeafNode(None, "Unordered list item with ")
        test_ln4 = LeafNode("i", "italic")
        test_ln5 = LeafNode(None, " text 2")
        test_ln6 = LeafNode(None, "Unordered list item 3 and some ")
        test_ln7 = LeafNode("code", "inline code")
        test_ln8 = LeafNode("b", "Bold")
        test_ln9 = LeafNode(None, " and ")
        test_ln10 = LeafNode("i", "italic")
        test_ln11 = LeafNode(None, " mixed in list item 4")
        test_ln12 = LeafNode(None, "Unordered list item 5 with a ")
        test_ln13 = LeafNode("a", "link", {"href": "https://example.com"})
        test_ln14 = LeafNode(None, "Final item 6 with an ")
        test_ln15 = LeafNode("img", "", {"src": "https://via.placeholder.com/50", "alt": "image"})
        
        test_li1 = ParentNode("li", [test_ln1, test_ln2])
        test_li2 = ParentNode("li", [test_ln3, test_ln4, test_ln5])
        test_li3 = ParentNode("li", [test_ln6, test_ln7])
        test_li4 = ParentNode("li", [test_ln8, test_ln9, test_ln10, test_ln11])
        test_li5 = ParentNode("li", [test_ln12, test_ln13])
        test_li6 = ParentNode("li", [test_ln14, test_ln15])
        test_ul_element = ParentNode("ul", [test_li1, test_li2, test_li3, test_li4, test_li5, test_li6])
        test_html = ParentNode("div", [test_ul_element])
        self.assertEqual(html, test_html)


    def test_unordered_list_block_multi_line3(self):
        block = """
- **Unordered** list item 1
- Unordered list item with _italic_ text 2
- 
- **Bold** and _italic_ mixed in list item 4
- Unordered list item 5 with a [link](https://example.com)
- Final item 6 with an ![image](https://via.placeholder.com/50)
"""
    
        html = markdown_to_html(block)

        test_ln1 = LeafNode("b", "Unordered")
        test_ln2 = LeafNode(None, " list item 1")
        test_ln3 = LeafNode(None, "Unordered list item with ")
        test_ln4 = LeafNode("i", "italic")
        test_ln5 = LeafNode(None, " text 2")
        test_ln6 = LeafNode(None, "")
        test_ln8 = LeafNode("b", "Bold")
        test_ln9 = LeafNode(None, " and ")
        test_ln10 = LeafNode("i", "italic")
        test_ln11 = LeafNode(None, " mixed in list item 4")
        test_ln12 = LeafNode(None, "Unordered list item 5 with a ")
        test_ln13 = LeafNode("a", "link", {"href": "https://example.com"})
        test_ln14 = LeafNode(None, "Final item 6 with an ")
        test_ln15 = LeafNode("img", "", {"src": "https://via.placeholder.com/50", "alt": "image"})
        
        test_li1 = ParentNode("li", [test_ln1, test_ln2])
        test_li2 = ParentNode("li", [test_ln3, test_ln4, test_ln5])
        test_li3 = ParentNode("li", [test_ln6])
        test_li4 = ParentNode("li", [test_ln8, test_ln9, test_ln10, test_ln11])
        test_li5 = ParentNode("li", [test_ln12, test_ln13])
        test_li6 = ParentNode("li", [test_ln14, test_ln15])
        test_ul_element = ParentNode("ul", [test_li1, test_li2, test_li3, test_li4, test_li5, test_li6])
        test_html = ParentNode("div", [test_ul_element])
        self.assertEqual(html, test_html)
    
    def test_ordered_list_block(self):
        block = """
1. List item 1
"""

        html = markdown_to_html(block)

        test_ln1 = LeafNode(None, "List item 1")
        test_li1 = ParentNode("li", [test_ln1])
        test_ol_element = ParentNode("ol", [test_li1])
        test_html = ParentNode("div", [test_ol_element])
        self.assertEqual(html, test_html)

    def test_ordered_list_block_multi_line(self):
        block = """
1. list item 1
2. list item 2
3. list item 3
4. list item 4
5. list item 5
"""
        html = markdown_to_html(block)

        test_lf1 = LeafNode(None, "list item 1")
        test_lf2 = LeafNode(None, "list item 2")
        test_lf3 = LeafNode(None, "list item 3")
        test_lf4 = LeafNode(None, "list item 4")
        test_lf5 = LeafNode(None, "list item 5")

        test_li1 = ParentNode("li", [test_lf1])
        test_li2 = ParentNode("li", [test_lf2])
        test_li3 = ParentNode("li", [test_lf3])
        test_li4 = ParentNode("li", [test_lf4])
        test_li5 = ParentNode("li", [test_lf5])

        test_ol_element = ParentNode("ol", [test_li1, test_li2, test_li3, test_li4, test_li5])
        test_html = ParentNode("div", [test_ol_element])
        self.assertEqual(html, test_html)

    def test_ordered_list_block_multi_line_multi_inline_markdown(self):
        block = """
1. **list item 1**
2. list item 2 with _italic_ text
3. list item 3 and some `inline code`
4. **Bold** and _italic_ mixed in list item 4
5. list item 5 with `code` snippet
6. list item 6 with a [useful link](https://example.com) and ![small image](https://via.placeholder.com/30)
"""
        html = markdown_to_html(block)

        test_ln1 = LeafNode("b", "list item 1")
        test_ln2 = LeafNode(None, "list item 2 with ")
        test_ln3 = LeafNode("i", "italic")
        test_ln4 = LeafNode(None, " text")
        test_ln5 = LeafNode(None, "list item 3 and some ")
        test_ln6 = LeafNode("code", "inline code")
        test_ln7 = LeafNode("b", "Bold")
        test_ln8 = LeafNode(None, " and ")
        test_ln9 = LeafNode("i", "italic")
        test_ln10 = LeafNode(None, " mixed in list item 4")
        test_ln11 = LeafNode(None, "list item 5 with ")
        test_ln12 = LeafNode("code", "code")
        test_ln13 = LeafNode(None, " snippet")
        test_ln14 = LeafNode(None, "list item 6 with a ")
        test_ln15 = LeafNode("a", "useful link", {"href": "https://example.com"})
        test_ln16 = LeafNode(None, " and ")
        test_ln17 = LeafNode("img", "", {"src": "https://via.placeholder.com/30", "alt": "small image"})

        test_li1 = ParentNode("li", [test_ln1])
        test_li2 = ParentNode("li", [test_ln2, test_ln3, test_ln4])
        test_li3 = ParentNode("li", [test_ln5, test_ln6])
        test_li4 = ParentNode("li", [test_ln7, test_ln8, test_ln9, test_ln10])
        test_li5 = ParentNode("li", [test_ln11, test_ln12, test_ln13])
        test_li6 = ParentNode("li", [test_ln14, test_ln15, test_ln16, test_ln17])

        test_ol_element = ParentNode("ol", [test_li1, test_li2, test_li3, test_li4, test_li5, test_li6])
        test_html = ParentNode("div", [test_ol_element])
        self.assertEqual(html, test_html)

    def test_ordered_list_block_multi_line2(self):
        block = """
1. list item 1
2. list item 2
3. 
4. list item 4
5. list item 5
"""
        html = markdown_to_html(block)

        test_lf1 = LeafNode(None, "list item 1")
        test_lf2 = LeafNode(None, "list item 2")
        test_lf3 = LeafNode(None, "")
        test_lf4 = LeafNode(None, "list item 4")
        test_lf5 = LeafNode(None, "list item 5")

        test_li1 = ParentNode("li", [test_lf1])
        test_li2 = ParentNode("li", [test_lf2])
        test_li3 = ParentNode("li", [test_lf3])
        test_li4 = ParentNode("li", [test_lf4])
        test_li5 = ParentNode("li", [test_lf5])

        test_ol_element = ParentNode("ol", [test_li1, test_li2, test_li3, test_li4, test_li5])
        test_html = ParentNode("div", [test_ol_element])
        self.assertEqual(html, test_html)


    def test_markdown_to_html_paragraph_to_html(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        html = markdown_to_html(md)
        self.assertEqual(html.to_html(),"<div><p>This is <b>bolded</b> paragraph<br>text in a p<br>tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")

    def test_markdown_to_html_heading_to_html(self):
        markdown = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

####### Not Heading
"""
        html = markdown_to_html(markdown)
        self.assertEqual(html.to_html(), "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6><p>####### Not Heading</p></div>")

    def test_markdown_to_html_code_to_html(self):
        md="""
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        html = markdown_to_html(md)
        self.assertEqual(
            html.to_html(),
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_quote_to_html(self):
        markdown = """
> quote 1
> quote 2
> quote 3
> quote 4
> quote 5
> quote 6

This is a paragraph
"""

        html = markdown_to_html(markdown)
        self.assertEqual(html.to_html(), "<div><blockquote><p>quote 1<br>quote 2<br>quote 3<br>quote 4<br>quote 5<br>quote 6</p></blockquote><p>This is a paragraph</p></div>")


    def test_markdown_to_html_unordered_list_to_html(self):
        markdown = """
- Unordered list item 1
- Unordered list item 2
- Unordered list item 3
- Unordered list item 4
- Unordered list item 5
- Unordered list item 6

This is a paragraph
"""
        html = markdown_to_html(markdown)
        self.assertEqual(html.to_html(), "<div><ul><li>Unordered list item 1</li><li>Unordered list item 2</li><li>Unordered list item 3</li><li>Unordered list item 4</li><li>Unordered list item 5</li><li>Unordered list item 6</li></ul><p>This is a paragraph</p></div>")
    
    def test_markdown_to_html_ordered_list_to_html(self):
        markdown = """
1. Ordered list item 1
2. Ordered list item 2
3. Ordered list item 3
4. Ordered list item 4
5. Ordered list item 5
6. Ordered list item 6

This is a paragraph
"""
        html = markdown_to_html(markdown)
        self.assertEqual(html.to_html(), "<div><ol><li>Ordered list item 1</li><li>Ordered list item 2</li><li>Ordered list item 3</li><li>Ordered list item 4</li><li>Ordered list item 5</li><li>Ordered list item 6</li></ol><p>This is a paragraph</p></div>")

    def test_markdown_to_html_markdown_to_html(self):
        markdown = """
# Main Heading

This is a **paragraph** with some _italic_ and **bold** text, along with `inline code`.
It continues here to make sure the paragraph spans multiple sentences.

## Subheading

> This is a blockquote that includes **bold emphasis**.
> It continues onto another line with _italic words_ and even `inline code`.
> Blockquotes can be multiple lines of quoted text.

### Lists Section

Here is an unordered list:

- First item with **bold** text
- Second item with _italic_ text
- Third item with `inline code` included

And here is an ordered list:

1. Ordered item one with a [link](https://example.com)
2. Ordered item two with an ![image](https://via.placeholder.com/50)
3. Ordered item three with **bold** and _italic_ text

### Code Block

Here is a C code block:

```
#include <stdio.h>

int main() {
    printf("Hello, Markdown World!\\n");
    return 0;
}
```

### Images and Links

Here is a sentence with an inline [link](https://openai.com).
And here is an image: ![Placeholder](https://via.placeholder.com/100)
"""

        html = markdown_to_html(markdown)
        self.assertEqual(html.to_html(), '<div><h1>Main Heading</h1><p>This is a <b>paragraph</b> with some <i>italic</i> and <b>bold</b> text, along with <code>inline code</code>.<br>It continues here to make sure the paragraph spans multiple sentences.</p><h2>Subheading</h2><blockquote><p>This is a blockquote that includes <b>bold emphasis</b>.<br>It continues onto another line with <i>italic words</i> and even <code>inline code</code>.<br>Blockquotes can be multiple lines of quoted text.</p></blockquote><h3>Lists Section</h3><p>Here is an unordered list:</p><ul><li>First item with <b>bold</b> text</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>inline code</code> included</li></ul><p>And here is an ordered list:</p><ol><li>Ordered item one with a <a href="https://example.com">link</a></li><li>Ordered item two with an <img src="https://via.placeholder.com/50" alt="image"></img></li><li>Ordered item three with <b>bold</b> and <i>italic</i> text</li></ol><h3>Code Block</h3><p>Here is a C code block:</p><pre><code>#include <stdio.h>\n\nint main() {\n    printf("Hello, Markdown World!\\n");\n    return 0;\n}\n</code></pre><h3>Images and Links</h3><p>Here is a sentence with an inline <a href="https://openai.com">link</a>.<br>And here is an image: <img src="https://via.placeholder.com/100" alt="Placeholder"></img></p></div>')

if __name__ == "__main__":
    unittest.main()
