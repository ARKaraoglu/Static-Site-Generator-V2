from textnode import TextType, TextNode
from file_logic import copy_static_to_public 

class Main():

    node = TextNode("dummy node", TextType.TEXT, "/")
    node2 = TextNode("dummy node", TextType.TEXT, "/") 

    print(node.__eq__(node2))
    print(node.__repr__())


    copy_static_to_public("/home/ahmet/bootdotdev/static-site-generator-v2/static", "/home/ahmet/bootdotdev/static-site-generator-v2/public")
