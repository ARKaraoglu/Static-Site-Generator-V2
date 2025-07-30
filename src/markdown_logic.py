from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

import re


# old_nodes = List of TextNodes
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        new_split_nodes = []
        split_values = node.text.split(delimiter)

        # If No matching delimiters found, the length of the values list will be dividable by 2.
        if len(split_values) % 2 == 0:
            raise Exception("No Matching delimiters: " + split_values)

        for x in range(0, len(split_values)):
            # If a value is empty or full of empty space, we skip
            if split_values[x].strip() == "":
                continue

            if x % 2 == 0:
                new_split_nodes.append(TextNode(split_values[x], TextType.TEXT))
            else:
                new_split_nodes.append(TextNode(split_values[x], text_type))
        


        new_nodes.extend(new_split_nodes)
    return new_nodes


def extract_markdown_images(text):
    image_pattern = r'\!\[(.*?)\]\((.*?)\)'
    images = re.findall(image_pattern, text)
    return images

def extract_markdown_links(text):
    link_pattern = r'(?<!!)\[(.*?)\]\((.*?)\)'
    links = re.findall(link_pattern, text)
    return links

#
# node1 = TextNode("Testnode 1 **Bold**     ", TextType.TEXT)
# node2 = TextNode("TextNode 2", TextType.TEXT)
# node3 = TextNode("TextNode 3 `cODE`", TextType.TEXT)
#
# split_nodes_delimiter([TextNode("Testnode 1 **Bold**     ", TextType.TEXT)], "**", TextType.BOLD)
# split_nodes_delimiter([TextNode("TextNode 2", TextType.TEXT)], "_", TextType.ITALIC)
# split_nodes_delimiter([TextNode("TextNode 3 `cODE`", TextType.TEXT)], "`", TextType.CODE)
#
# split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
