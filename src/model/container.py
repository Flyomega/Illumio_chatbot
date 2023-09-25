from .paragraph import Paragraph
from .block import Block

INFINITE = 99999

class Container:

    def __init__(self, paragraphs : [Paragraph], title : Paragraph=None, level: int = 0, index: [int] = None , father=None, id_ = 0):
        if index is None:
            index = []
        self.level = level
        self.paragraphs = []
        self.title = title
        self.index = index
        self.children = []
        self.father = father
        if(father == None):
            self.id_ = id_ + 1
        else:
            self.id_ = int(str(1) + str(father.id_) + str(id_))
        if paragraphs:
            self.paragraphs, self.children = self.create_children(paragraphs, level,index)
        self.blocks = self.get_blocks()


    def get_blocks(self):
        block = Block(level=self.level, index=self.index)
        if self.title:
            block.title = self.title.text
        for p in self.paragraphs:
            if not p.blank:
                block.content += p.text
        blocks = [block] if block.content else []
        for child in self.children:
            blocks += child.blocks
        return blocks

    def create_children(self, paragraphs: Paragraph, level: int, index: [int]) -> ([Paragraph], []):
        """
        creates children containers or directly attached content
        and returns the list of containers and contents of level+1
        :return:
        [Content or Container]
        """
        attached_paragraphs = []
        container_paragraphs = []
        container_title = None
        children = []
        in_children = False
        child_id = 0
        level = INFINITE

        while paragraphs:
            p = paragraphs.pop(0)
            if not in_children and not p.is_structure:
                attached_paragraphs.append(p)
            else:
                in_children = True
                if p.is_structure and p.level <= level:  # if p is higher in hierarchy, then the child is completed
                    if container_paragraphs or container_title:
                        if level <= len(index):
                            index = index[:level]
                            index[-1] += 1
                        else:
                            for i in range(level-len(index)):
                                index.append(1)
                        children.append(Container(container_paragraphs, container_title, level, index, self, child_id))
                        child_id += 1
                    container_paragraphs = []
                    container_title = p
                    level = p.level
                else:  # p is normal text or strictly lower in hierarchy, then the child continues to grow
                    container_paragraphs.append(p)

        if container_paragraphs or container_title:
            if level <= len(index):
                index = index[:level]
                index[-1] += 1
            else:
                for i in range(level - len(index)):
                    index.append(1)
            children.append(Container(container_paragraphs, container_title, level, index, self, child_id))
            child_id += 1

        return attached_paragraphs, children
    