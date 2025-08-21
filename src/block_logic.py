from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code" 
    QUOTE = "quote" 
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    #WARNING: Have to make an exception to code block for code block can have more than 1 new line between lines
    first_line = markdown.split("\n", 1)[0]
    first_word = first_line.split(" ", 1)[0]
    if first_word == "```":
        block = markdown
        return [block]

    split_blocks = markdown.split("\n\n")
    final_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            final_blocks.append(stripped_block)
    
    return final_blocks 

def block_to_block_type(block, function_debug = None):
    split_lines = block.split("\n")
    filtered_lines = []

    for line in split_lines:
        if line != "":
            filtered_lines.append(line)

    if function_debug != None:
        print(f"block: {block}\n filtered lines: {filtered_lines}")
    
    first_line = filtered_lines[0]
    if '# ' in first_line:
        for line in filtered_lines:
            if '# ' not in line:
                return BlockType.PARAGRAPH

            first_word = line.split(" ", 1)[0]
            h_marker = first_word.count("#")
            if h_marker != len(first_word) or h_marker > 6 or h_marker == 0:
                return BlockType.PARAGRAPH
        return BlockType.HEADING

    if "```" in first_line:
        last_line = filtered_lines[len(filtered_lines) - 1]
        if last_line == "```":
            if function_debug != None:
                print("in here")
            return BlockType.CODE


    if "> " in first_line:
        for line in filtered_lines:
            if "> " not in line:
                return BlockType.PARAGRAPH
            first_word = line.split(" ", 1)[0]
            if ">" != first_word:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE


    if "- " in first_line:
        for line in filtered_lines:
            if "- " not in line:
                return BlockType.PARAGRAPH

            first_word = line.split(" ", 1)[0]
            if function_debug != None:
                print(line, first_word)

            if first_word != "-":
               return BlockType.PARAGRAPH

        return BlockType.UNORDERED_LIST

    if "1. " in first_line:
        ol_counter = 1
        for line in filtered_lines:
            if f"{ol_counter}. " not in line:
                return BlockType.PARAGRAPH

            if line.split(". ", 1)[0] != f"{ol_counter}":
                return BlockType.PARAGRAPH
            ol_counter += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    

    

    


    

