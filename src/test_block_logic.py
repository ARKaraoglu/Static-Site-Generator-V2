import unittest
from block_logic import markdown_to_blocks

class TestBlockLogic(unittest.TestCase):
    def test_block_logic1(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        
        self.assertListEqual(blocks, ["This is **bolded** paragraph", "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", "- This is a list\n- with items"])

    def test_block_logic2(self):
        markdown = """
This is **bold** text in a paragraph.

This is another paragraph with _italic_ text and `inline code` here.
This is the same paragraph on a new line.

- First list item
- Second list item
- Third list item

![Mountain View](https://example.com/mountain.jpg)

Here’s a paragraph with a [link](https://example.com) inside.

> This is a blockquote with **bold** and _italic_ text.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, ["This is **bold** text in a paragraph.", "This is another paragraph with _italic_ text and `inline code` here.\nThis is the same paragraph on a new line.", "- First list item\n- Second list item\n- Third list item", "![Mountain View](https://example.com/mountain.jpg)", "Here’s a paragraph with a [link](https://example.com) inside.", "> This is a blockquote with **bold** and _italic_ text."])

    def test_block_logic3(self):
        markdown = """
The **morning light** spilled over the _valley_, touching the peaks with gold.


I adjusted the `brightness` setting to capture the perfect shot.


Moments later, a _bird_ landed nearby and the **leaves** rustled gently.



- Gather supplies
- Check the `map`

- Begin the hike



![Desert Dunes](https://example.com/desert.jpg)



Travel stories are collected [here](https://example.com/travel-journal).
> Nature has a way of making **time** feel _slower_.
"""

        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, ["The **morning light** spilled over the _valley_, touching the peaks with gold.","I adjusted the `brightness` setting to capture the perfect shot.","Moments later, a _bird_ landed nearby and the **leaves** rustled gently.","- Gather supplies\n- Check the `map`","- Begin the hike","![Desert Dunes](https://example.com/desert.jpg)","Travel stories are collected [here](https://example.com/travel-journal).\n> Nature has a way of making **time** feel _slower_."])



































