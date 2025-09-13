from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from block_logic import BlockType, markdown_to_blocks, block_to_block_type
import re


# Description: Seperates a line into tuple tokens representing inline markdowns including regular text
# Parameters:
# line -> line of string type of a block
# Return:
# tokenized_nodes -> list containing list of tuples (type, val) of a line 
def tokenizer(line):
    filtered_tuples_list = []
    node_tuples_list = []
    current_text = ""
    # Converts indexes into tuple(type, val)
    for index in line:
        match(index):
            case "*":
                if len(current_text) == 0:
                    node_tuples_list.append(("STAR", 1))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("STAR", 1))

            case "_":
                if len(current_text) == 0:
                    node_tuples_list.append(("UNDERSCORE", 1))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("UNDERSCORE", 1))
            case "`":
                if len(current_text) == 0:
                    node_tuples_list.append(("CODE", 1))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("CODE", 1))
            case "!":
                if len(current_text) == 0:
                    node_tuples_list.append(("EX_MARK", "!"))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("EX_MARK", "!"))
            case "[":
                if len(current_text) == 0:
                    node_tuples_list.append(("OP_BR", 1))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("OP_BR", 1))
            case "]":
                if len(current_text) == 0:
                    node_tuples_list.append(("CL_BR", 1))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("CL_BR", 1))
            case "(":
                if len(current_text) == 0:
                    node_tuples_list.append(("OP_PA", 1))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("OP_PA", 1))
            case ")":
                if len(current_text) == 0:
                    node_tuples_list.append(("CL_PA", 1))
                else:
                    node_tuples_list.append(("TEXT", current_text))
                    current_text = ""
                    node_tuples_list.append(("CL_PA", 1))
            case _:
                current_text += index

    if len(current_text) != 0:
        node_tuples_list.append(("TEXT", current_text))
       
    ptr1 = 0
    ptr2 = 1
    # Merges tuples which have the same type by adding their values together
    while(ptr2 < len(node_tuples_list)):
   
        if node_tuples_list[ptr1][0] == node_tuples_list[ptr2][0]:
            node_tuples_list[ptr2] = (node_tuples_list[ptr2][0], node_tuples_list[ptr2][1] + node_tuples_list[ptr1][1])
        else:
            filtered_tuples_list.append(node_tuples_list[ptr1])
        ptr1 += 1
        ptr2 += 1
            
    filtered_tuples_list.append(node_tuples_list[ptr2 - 1])
    if len(node_tuples_list) == 1:
        filtered_tuples_list = node_tuples_list

    return filtered_tuples_list 

# Description: 
# Parameters:
# 
# 
# Return:
#


# CURRENT Path
# Markdown -> markdown_to_html -> markdown_to_block -> text_to_textnode

#NOTE: AST will turn tokens into textnodes
def AST(node_tokens_list):
    
    pre_ast_nodes = []
    for node_tokens in node_tokens_list:
        pass
    
        

# Description: Divides a list of text nodes into new text nodes using the entered delimiter and textype
# Parameters:
# old_nodes -> list of textnodes
# delimiter -> string character used as delimiter
# text_type -> TextType enum
# Return:
# new_nodes -> list of textnodes

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
            raise Exception(f"No Matching delimiters!\n    Text: {node.text}\n    Split_Values: {split_values}\n    Text Type: {text_type}\n")

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
                if new_texts[0].strip() == "":
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
                if new_texts[0].strip() == "":
                    new_texts.pop(0)
                    continue
                else:
                    new_nodes.append(TextNode(f"{new_texts[0]}", TextType.TEXT))
                    new_texts.pop(0)
            else:
                new_nodes.append(TextNode(f"{links[0][0]}", TextType.LINK, f"{links[0][1]}"))
                links.pop(0)

    return new_nodes

# Description: Takes a line of a block and splits it into as many inline markdown node as possible
def text_to_textnode(line, function_debug = None):
    t_nodes = [TextNode(line, TextType.TEXT)]

    detected_delimiter = True
    while detected_delimiter == True:
        detected_delimiter = False
        temp_node_list = []
        
        for node in t_nodes:
            if node.text_type != TextType.TEXT:
                temp_node_list.append(node)
                continue

            if "**" in node.text:
                detected_delimiter = True
                split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
                temp_node_list.extend(split_nodes)
                continue

            if "_" in node.text:
                detected_delimiter = True
                split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
                temp_node_list.extend(split_nodes)
                continue
            
            if "`" in node.text:
                detected_delimiter = True
                split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
                temp_node_list.extend(split_nodes)
                continue
            
            if len(extract_markdown_images(node.text)) > 0:
                detected_delimiter = True
                split_nodes = split_nodes_image([node])
                temp_node_list.extend(split_nodes)
                continue

            if len(extract_markdown_links(node.text)) > 0:
                detected_delimiter = True
                split_nodes = split_nodes_link([node])
                temp_node_list.extend(split_nodes)
                continue

            temp_node_list.append(node) # If it is a textnode with no inline markdown

        t_nodes = temp_node_list
    return t_nodes

def block_to_paragraph_element(block, function_debug = None):
    lines = block.split("\n")
    inline_textnodes = []
    
    if function_debug != None:
        print(f"inside block_to_paragraph_element function")
        

    line_break_counter = len(lines) - 1
    for line in lines:
        # If a <p> block has more than 1 line, then we add <br> at the end of each to merge them all under 1 <p> parent node to avoid excess space between lines
        if len(lines) > 1 and line_break_counter != 0:
            line += "<br>"
            line_break_counter -= 1

        inline_textnodes.extend(text_to_textnode(line))
    
    inline_leafnodes = []
    for node in inline_textnodes:
        inline_leafnodes.append(text_node_to_html_node(node))
    
    paragraph_element = ParentNode("p", inline_leafnodes)
    return paragraph_element

def block_to_header_element(block, function_debug = None):
    block_first_split = block.split(" ", 1)
    new_block = block_first_split[1]
    lines = new_block.split("\n")
    inline_textnodes = []
    for line in lines:
        inline_textnodes.extend(text_to_textnode(line, function_debug)) 
    
    inline_leafnodes = []
    
    if function_debug != None:
        print(f"\n{block_first_split}\n")
    
    for node in inline_textnodes:
        inline_leafnodes.append(text_node_to_html_node(node))

    heading_symbol = block_first_split[0].count("#")

    header_element = ParentNode(f"h{heading_symbol}", inline_leafnodes)
    return header_element

#NOTE: CODE has no inline markdown
def block_to_code_element(block):
    # block_first_split = block.split("\n", 1)
    # block_second_split = block_first_split[1].rsplit("\n", 1)
    # new_block = block_second_split[1]
    new_block = block.split("```")[1]

    child_leafnode = LeafNode(tag = "code", value = new_block.split("\n", 1)[1])
    code_element = ParentNode("pre", [child_leafnode])
    return code_element

def block_to_quote_element(block):
    old_lines = block.split("\n")
    new_lines = []
    line_counter = len(old_lines) - 1
    for line in old_lines:
        temp = line.split("> ", 1)[1]
        
        if line_counter != 0:
            temp += "\n"
            line_counter -= 1

        new_lines.append(temp)
    new_block = ""
    for line in new_lines:
        new_block += line

    paragraph_element = block_to_paragraph_element(new_block)

    quote_element = ParentNode("blockquote", [paragraph_element])
    return quote_element
    # e1 = LeafNode(None, new_block)
    # quote_element = ParentNode("blockquote", [e1])
    # return quote_element

def block_to_unordered_list_element(block):
    lines = block.split("\n")

    list_items = []
    for line in lines:
        new_line = line.split("- ")[1]

        inline_textnodes = text_to_textnode(new_line)
        
        inline_leafnodes = []
        for textnode in inline_textnodes:
            inline_leafnodes.append(text_node_to_html_node(textnode))

        list_items.append(ParentNode("li", inline_leafnodes))

    unordered_list_element = ParentNode("ul", list_items)
    return unordered_list_element

def block_to_ordered_list_element(block):
    lines = block.split("\n")

    list_items = []
    item_counter = 1
    for line in lines:
        new_line = line.split(f"{item_counter}. ", 1)[1]

        inline_textnodes = text_to_textnode(new_line)

        inline_leafnodes = []
        for textnode in inline_textnodes:
            inline_leafnodes.append(text_node_to_html_node(textnode))

        list_items.append(ParentNode("li", inline_leafnodes))
        item_counter += 1

    orderes_list_element = ParentNode("ol", list_items)
    return orderes_list_element



#NOTE: In BlockType.PARAGRAPH, we add extra <br> at the end of each line of a block to put all the lines into a single p html element . This process might be required to be done at a later stage. 
def markdown_to_html(markdown, function_debug = None):
    
    blocks = markdown_to_blocks(markdown)
    if function_debug != None:
        print(blocks)
    markdown_children = []
    for block in blocks:
        if function_debug != None:
            print(f"\n{block}")
            print(f"{block_to_block_type(block, function_debug)}\n")
        # if function_debug != None:
        #     print(block_to_block_type(block, True))
        match (block_to_block_type(block)):
            case BlockType.PARAGRAPH:
                markdown_children.append(block_to_paragraph_element(block))
            case BlockType.HEADING:
                markdown_children.append(block_to_header_element(block))
            case BlockType.CODE:
                markdown_children.append(block_to_code_element(block))
            case BlockType.QUOTE:
                markdown_children.append(block_to_quote_element(block))
            case BlockType.UNORDERED_LIST:
                markdown_children.append(block_to_unordered_list_element(block))
            case BlockType.ORDERED_LIST:
                markdown_children.append(block_to_ordered_list_element(block))


    markdown_parent = ParentNode("div", markdown_children)
    return markdown_parent

