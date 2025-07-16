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
        
        props_string = ""
        assert self.props is not None
        for key, value in self.props.items():
            props_string += f" {key}={value}"
        
        return props_string

    def __repr__(self):
        if self == None:
            raise Exception(f"{self} is None")

        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value)
        self.props = props


    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value!")
        elif self.tag == None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

