from paragraph import Paragraph

class Container:

    def __init__(self, paragraphs : [Paragraph], level: int = 0, father=None, id_ : int = 0):
        self.level = level
        self.paragraphs = []
        self.children = []
        self.father = father
        self.id_ = id_ + 1
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