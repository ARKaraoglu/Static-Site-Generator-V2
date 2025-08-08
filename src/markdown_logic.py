from textnode import TextNode, TextType

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

#NOTE: When this function supports multiple opening and closing brackets AND paranthesis, it will add the extra brackets to image alt text paranthesis to image source. 
 # So there won't be a need for split_nodes_image function to handle it
#WARNING: Multiple opening and/or closing parathesis won't work in the image source, so perhaps give a warning.
def extract_markdown_images(text):
    image_pattern = r'\!\[(.*?)\]\((.*?)\)'
    images = re.findall(image_pattern, text)
    # print(f"Inside extract images: {images}\n")
    return images

#NOTE: When this function supports multiple opening and closing brackets AND paranthesis, it will add the extra brackets to image alt text AND paranthesis to link source. 
 # So there won't be a need for split_nodes_link function to handle it
#WARNING: Multiple opening and/or closing parathesis won't work in the link source, so perhaps give a warning.
def extract_markdown_links(text):
    link_pattern = r'(?<!!)\[(.*?)\]\((.*?)\)'
    links = re.findall(link_pattern, text)
    return links

#NOTE: For now, this function adds all the split text nodes into a new list individually.
 # There may be a need to add the individual old nodes' splits into new nodes list as a list to be able to diffirentiate which nodes split into using a temp_node_list[]
def split_nodes_image(old_nodes):
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        new_texts = [node.text]
        for img in images:
            temp_list = []
            for t_node in new_texts:
                temp_list.extend(t_node.split(f"![{img[0]}]({img[1]})"))

            new_texts = temp_list

        total_length = len(new_texts) + len(images)
        for x in range(0, total_length):
            if len(new_texts) == 0 and len(images) == 0:
                break

            if x % 2 == 0:
                if new_texts[0] == "":
                    new_texts.pop(0)
                    continue
                else:
                    new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
                    new_texts.pop(0)
            else:
                new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
                images.pop(0)

    return new_nodes




def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        new_texts = [node.text]

        for link in links:
            temp_texts = []
            for n_text in new_texts:
                temp_texts.extend(n_text.split(f"[{link[0]}]({link[1]})"))
            new_texts = temp_texts


        total_length = len(links) + len(new_texts)
        for x in range(0, total_length):
            if len(links) == 0 and len(new_texts) == 0:
                break

            if x % 2 == 0:
                if new_texts[0] == "":
                    new_texts.pop(0)
                    continue
                else:
                    new_nodes.append(TextNode(f"{new_texts[0]}", TextType.TEXT))
                    new_texts.pop(0)
            else:
                new_nodes.append(TextNode(f"{links[0][0]}", TextType.LINK, f"{links[0][1]}"))
                links.pop(0)

    return new_nodes


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
