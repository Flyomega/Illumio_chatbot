from paragraph import Paragraph
from block import Block

class Container:

    def __init__(self, paragraphs : [Paragraph], title : Paragraph=None, level: int = 0, father=None, id_ : int = 0):
        self.level = level
        self.paragraphs = []
        self.title = title
        self.children = []
        self.father = father
        self.id_ = int(str(1) + str(father.id_) + str(id_))
        if paragraphs:
            self.paragraphs, self.children = self.create_children(paragraphs, level)
        self.blocks = self.get_blocks()


    def create_children(self, paragraphs, level):
        attached_paragraphs = []
        container_paragraphs = []
        container_title = None
        children = []
        in_children = False
        child_id = 0
        for p in paragraphs:
            if p.level == level + 1:
                in_children = True
                child_id += 1
                children.append(Container(paragraphs, level + 1, father=self, id_=child_id))
            elif in_children:
                break
            elif p.level == level:
                container_title = p
            elif p.level == level + 2:
                attached_paragraphs.append(p)
            elif p.level == level + 3:
                container_paragraphs.append(p)
        return attached_paragraphs, container_paragraphs, container_title, children
    
    def get_blocks(self):
        block = Block(level=self.level)
        if self.title:
            block.title = self.title.text
        for p in self.paragraphs:
            if not p.blank:
                block.content += p.text
        blocks = [block] if block.content or block.specials else []
        for child in self.children:
            blocks += child.blocks
        return blocks