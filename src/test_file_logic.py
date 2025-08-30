import unittest
from file_logic import extract_title

class TestFileLogic(unittest.TestCase):
    def test_extract_title(self):
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

        title = extract_title(markdown)
        self.assertEqual(title, "Main Heading")

    def test_extract_title2(self):
        markdown = """
# Adventure in the Woods

The **forest** was quiet, except for the _rustle of leaves_ underfoot.
A sudden `crack` of a branch made us stop.

## Observations

- Tall trees with **thick trunks**
- Moss-covered rocks
- A stream with _crystal clear_ water

> "The woods are lovely, dark and deep," someone whispered.

```python
print("Exploring the woods...")
```
"""

        title = extract_title(markdown)
        self.assertEqual(title, "Adventure in the Woods")
    
    def test_extract_title3(self):
        markdown = """
# Cooking Notes

This paragraph has a [link to a recipe](https://example.com/recipe).
I also took a picture: ![Food](https://via.placeholder.com/80)

## Ingredients List

1. **Flour** – 2 cups
2. _Sugar_ – 1 cup
3. `Butter` – 200g
4. Eggs – 3 large

> Cooking is like **magic**, but tastier!

```bash
echo "Baking in progress..."
```"""

        title = extract_title(markdown)
        self.assertEqual(title, "Cooking Notes")
if __name__ == "__main__":
   unittest.main() 
