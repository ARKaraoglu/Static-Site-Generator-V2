class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if self.props == None:
            return ""
        
        props_string = ''
        assert self.props is not None
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
        
        return props_string

    def __repr__(self):
        if self == None:
            raise Exception(f"{self} is None")

        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value!")
        elif self.tag == None:
            return f"{self.value}"
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        if isinstance(self, other) and self.tag == other.tag and self.value == other.value and self.props == other.props:
            return True
        return False

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")

        elif self.children == None:
            raise ValueError("ParentNode must have children")

        else:
            parent_string = ''

            parent_string += f'<{self.tag}{self.props_to_html()}>'
            #self.children is a list.
            for child in self.children:
                if isinstance(child, ParentNode):
                    parent_string += child.to_html()
                else:
                    parent_string += child.to_html()

            parent_string += f'</{self.tag}>'
            
            return parent_string

    def __repr__(self):
        return f'ParentNode({self.tag}, {self.children}, {self.props})'

    def __eq__(self, other):
        if isinstance(self, other) and self.tag == other.tag and self.children == other.children and self.props == other.props:
            return True
        return False

