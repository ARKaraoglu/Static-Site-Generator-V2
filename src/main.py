from textnode import TextType
from textnode import TextNode


class Main():

    node = TextNode("dummy node", TextType.TEXT, "/")
    node2 = TextNode("dummy node", TextType.TEXT, "/") 

    print(node.__eq__(node2))
    print(node.__repr__())

