from enum import Enum
from htmlnode import LeafNode
from markdown_logic import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    
def text_node_to_html_node(textnode):
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
        case _:
            raise Exception(f"Invalid text_type: {textnode.text_type}")

def text_to_textnode(text):
    t_nodes = [TextNode(text, TextType.TEXT)]

    detected_delimiter = False
    while detected_delimiter == True:
        temp_node_list = []
        for node in t_nodes:
            if node.text_type != TextType.TEXT:
                temp_node_list.append(node)

            if "**" in node.text:
                detected_delimiter = True
                split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
                temp_node_list.extend(split_nodes)
                break

            if "_" in node.text:
                detected_delimiter = True
                split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
                temp_node_list.extend(split_nodes)
                break

            if "`" in node.text:
                detected_delimiter = True
                split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
                temp_node_list.extend(split_nodes)
                break

            if len(extract_markdown_images(node.text)) > 1:
                detected_delimiter = True
                split_nodes = split_nodes_image([node])
                temp_node_list.extend(split_nodes)
                break

            if len(extract_markdown_links(node.text)) > 1:
                detected_delimiter = True
                split_nodes = split_nodes_link([node])
                temp_node_list.extend(split_nodes)
                break

        t_nodes = temp_node_list
    return t_nodes


