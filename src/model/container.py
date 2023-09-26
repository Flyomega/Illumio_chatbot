from .paragraph import Paragraph
from .block import Block

INFINITE = 99999

class Container:

    def __init__(self, paragraphs : [Paragraph], title : Paragraph=None, level: int = 0, index: [int] = None , father=None, id_ = 0):
        if index is None:
            index = []
        self.level = level
        self.title = title
        self.paragraphs = []
        self.children = []
        self.index = index
        self.father = father
        self.id_ = int(str(1) + str(father.id_) + str(id_))
        if paragraphs:
            self.paragraphs, self.children = self.create_children(paragraphs, level, index)
        self.blocks = self.get_blocks()


    def get_blocks(self):
        block = Block(level=self.level, index=self.index)
        if self.title:
            block.title = self.title.text
        for p in self.paragraphs:
            block.content += p.text
        blocks = [block] if block.content else []
        for child in self.children:
            blocks += child.blocks
        return blocks

    def create_children(self, paragraphs: [Paragraph], level: int, index: [int]):
        """
        Creates children containers and/or directly attached content and returns the list of attached content and the list of children containers.
        The indexes correspond to the indexes of the paragraphs in the content and also on the structure.
        :return: List of Content or Container
        """
        attached_paragraphs = []
        children = []
        in_children = False

        container_title = None
        level = INFINITE

        while paragraphs:
            p = paragraphs.pop(0)
            if not in_children and not p.is_structure:
                attached_paragraphs.append(p)
            else:
                in_children = True
                if p.is_structure:  # if p is higher in hierarchy, then the child is completed
                    if p.level < level:
                        level = p.level
                        container_title = p
                        self.index.append(1)
                    elif p.level == level:
                        self.index[-1] += 1
                    else:
                        self.index = index[:p.level]
                        self.index[-1] += 1
                        level = p.level
                        container_title = p
                else:
                    paragraphs.insert(0, p)
                    break
        
        if container_title:
            attached_paragraphs.append(paragraphs.pop(0))

        return attached_paragraphs, children
    
    
    @property
    def structure(self):

        self_structure = {str(self.id_): {
            'index': str(self.id_),
            'canMove': True,
            'isFolder': True,
            'children': [p.id_ for p in self.paragraphs] + [child.id_ for child in self.children],
            'canRename': True,
            'data': {},
            'level': self.level,
            'rank': self.rank,
            'title': self.title.text if self.title else 'root'
        }}
        paragraphs_structure = [p.structure for p in self.paragraphs]
        structure = [self_structure] + paragraphs_structure
        for child in self.children:
            structure += child.structure
        return structure
    