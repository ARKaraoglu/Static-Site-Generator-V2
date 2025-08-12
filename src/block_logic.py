



def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    final_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            final_blocks.append(stripped_block)
    
    return final_blocks 

