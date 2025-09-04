from textnode import TextType, TextNode
from file_logic import copy_static_to_dest , generate_page, generate_pages_recursively
import sys

class Main():

    # node = TextNode("dummy node", TextType.TEXT, "/")
    # node2 = TextNode("dummy node", TextType.TEXT, "/") 
    #
    # print(node.__eq__(node2))
    # print(node.__repr__())
    basepath = sys.argv[0]
    if basepath == None:
        basepath = "/"

    #copy_static_to_public("/home/ahmet/bootdotdev/static-site-generator-v2/static", "/home/ahmet/bootdotdev/static-site-generator-v2/public")
    copy_static_to_dest("static", "docs")
    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    generate_pages_recursively("content", "template.html", "docs", basepath)
