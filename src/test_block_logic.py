import unittest
from block_logic import markdown_to_blocks, block_to_block_type, BlockType

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

class TestBlockToBlockTypes(unittest.TestCase):
    def test_block_to_blocktype_heading1(self):
        block = "# This is Heading 1"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_heading2(self):
        block = "## This is Heading 2"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_heading3(self):
        block = "### This is Heading 3"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))
    
    def test_block_to_blocktype_heading4(self):
        block = "#### This is Heading 4"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))
    
    def test_block_to_blocktype_heading5(self):
        block = "##### This is Heading 5"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))
    
    def test_block_to_blocktype_heading6(self):
        block = "###### This is Heading 6"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))
    
    def test_block_to_blocktype_heading_incorrect(self):
        block = "####### This is Heading 1"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_multi_heading1(self):
        block = """
# This is Heading 1
## This is subheading
"""
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_multi_heading2(self):
        block = """# This is Heading 1
## This is subheading
##### This is a heading number 5
"""
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_multi_heading3(self):
        block = """
# This is Heading 1
## This is subheading
### H3
#### H4
##### H5
###### H6
"""
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_multi_heading_incorrect(self):
            block = """
# This is Heading 1
## This is subheading
### H3
#### H4
##### H5
###### H6
####### H7
"""
            self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_multi_heading_incorrect2(self):
        block = """# This is Heading 1
This is not a heading
## This is subheading
"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_multi_heading_incorrect3(self):
        block = """
# This is Heading 1
##This is subheading
"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_blocktype_multi_heading_incorrect4(self):
        block = """
# This is Heading 1
## This is subheading
#
"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

#QUOTE TESTS

    def test_block_to_blocktype_code1(self):
        block = """```
def foo():
    print("Foo was called")

def bar():
    print("Bar was called")
    foo()

bar()
```
"""
        self.assertEqual(block_to_block_type(block),BlockType.CODE)


    def test_block_to_blocktype_code2(self):
        block = """```
function foo() {
    console.log("Foo was called");
}

function bar() {
    console.log("Bar was called");
    foo();
}

bar();
```"""
        self.assertEqual(block_to_block_type(block),BlockType.CODE)


    def test_block_to_blocktype_code3(self):
        block = """```
#include <stdio.h>

void foo() {
    printf("Foo was called\n");
}

void bar() {
    printf("Bar was called\n");
    foo();
}

int main() {
    bar();
    return 0;
}
```"""

        self.assertEqual(block_to_block_type(block),BlockType.CODE)


    def test_block_to_blocktype_code_invalid(self):
        block = """```
#include <stdio.h>

void foo() {
    printf("Foo was called\n");
}

void bar() {
    printf("Bar was called\n");
    foo();
}

int main() {
    bar();
    return 0;
}
````"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_code_invalid2(self):
        block = """``
#include <stdio.h>

void foo() {
    printf("Foo was called\n");
}

void bar() {
    printf("Bar was called\n");
    foo();
}

int main() {
    bar();
    return 0;
}
```"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

# QUOTE TESTS

    def test_block_to_blocktypes_quote(self):
        block = """
> Quote line 1
"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    def test_block_to_blocktypes_quote2(self):
        block = """
> Quote line 1
> Quote line 2
> Quote line 3

"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_blocktypes_quote3(self):
        block = """
> Quote line 1
> line 2
> line 3
> line 4
> line 5
> line 6
> line 7
"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_blocktypes_quote_incorrect(self):
        block = """
> Quote line 1
>
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktypes_quote_incorrect2(self):
        block = """
>> Quote line 1
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktypes_quote_incorrect3(self):
        block = """
> Quote line 1
Not Quote line
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

# UNORDERED LIST TESTS

    def test_block_to_blocktypes_unordered_list(self):
        block = """
- unordered list
"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_blocktypes_unordered_list2(self):
        block = """
- unordered list
- element 2
"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_blocktypes_unordered_list3(self):
        block = """
- unordered list
- 
- element 3
"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    


    def test_block_to_blocktypes_unordered_list4(self):
        block = """
- Apples
- Bananas
- Cherries
- Dates
- Elderberries
- Figs
- Grapes
- Honeydew"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)


    def test_block_to_blocktypes_unordered_list_incorrect(self):
        block = """
-ordered list
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_blocktypes_unordered_list_incorrect2(self):
        block = """
- unordered list
-- unordered list 2
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    
    def test_block_to_blocktypes_unordered_list_incorrect3(self):
        block = """
- unordered list
--element incorrect
- element 2
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

# ORDERED LIST TESTS


    def test_block_to_blocktypes_ordered_list(self):
        block = """
1. element 1
"""
    
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    def test_block_to_blocktypes_ordered_list2(self):
        block = """
1. element 1
2. Element 2
3. element 3
4. Element 4
"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_blocktypes_ordered_list3(self):
        block = """
1. element 1
2. Element 2
3. element 3
4. Element 4
5. 
6. 
7. Element 7
8. 
9. 
10. Element 10
"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_blocktypes_ordered_list4(self):
        block = """
1. Item 1
2. Item 2
3. Item 3
4. Item 4
5. Item 5
6. Item 6
7. Item 7
8. Item 8
9. Item 9
10. Item 10
11. Item 11
12. Item 12
13. Item 13
14. Item 14
15. Item 15
16. Item 16
17. Item 17
18. Item 18
19. Item 19
20. Item 20
"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_blocktypes_ordered_list_incorrect(self):
        block = """
1. Item 1
2. Item 2
3. Item 3
4. Item 4
5. Item 5
6. Item 6
7. Item 7
8. Item 8
9. Item 9
10. Item 10
11. Item 11
12. Item 12
12. Item 12 and a half
13. Item 13
14. Item 14
15. Item 15
16. Item 16
17. Item 17
18. Item 18
19. Item 19
20. Item 20
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktypes_ordered_list_incorrect2(self):
        block = """
1. Element 1
2.
3. Element 3
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktypes_ordered_list_incorrect3(self):
        block = """
1. Element 1
2.element 2
3. Element 3
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


# NON-BLOCK TYPE

    def test_block_to_blocktype_non_blocktype(self):
        block = """
This is - a paragraph
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_non_blocktype2(self):
        block = """
This is the 1. element
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_non_blocktype3(self):
        block = """
This is a # heading
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_non_blocktype4(self):
        block = """
% means nothing
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_non_blocktype5(self):
        block = """
2. stuff
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_blocktype_non_blocktype6(self):
        block = """
Warning: This is a normal block
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

