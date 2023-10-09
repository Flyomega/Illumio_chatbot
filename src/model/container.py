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
        self.containers = [self]
        for child in self.children:
            self.containers += child.containers
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

    def create_children(self, paragraphs, level, rank) -> ([], []):
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
        level = INFINITE
        child_id = 0

        while paragraphs:
            p = paragraphs.pop(0)
            if not in_children and not p.is_structure:
                attached_paragraphs.append(p)
            else:
                in_children = True
                if p.is_structure and not p.blank and p.level <= level:  # if p is higher or equal in hierarchy
                    if container_paragraphs or container_title:
                        children.append(Container(container_paragraphs, container_title, level, rank, self, child_id))
                        child_id += 1
                    container_paragraphs = []
                    container_title = p
                    level = p.level

                else:  # p is strictly lower in hierarchy
                    container_paragraphs.append(p)

        if container_paragraphs or container_title:
            children.append(Container(container_paragraphs, container_title, level, rank, self, child_id))
            child_id += 1

        return attached_paragraphs, children


    #REAL ONEEEEEEEEEEEEEEEEEEEEE

    # def create_children(self, paragraphs: [Paragraph], level: int, index: [int]):
    #     """
    #     Creates children containers and/or directly attached content and returns the list of attached content and the list of children containers.
    #     The indexes correspond to the indexes of the paragraphs in the content and also on the structure.
    #     :return: List of Content or Container
    #     """
    #     attached_paragraphs = []
    #     children = []
    #     in_children = False
    #     level = INFINITE
    #     container_paragraphs = []
    #     container_title = None

    #     while paragraphs:
    #         p = paragraphs.pop(0)

    #         if not in_children and not p.is_structure:
    #             attached_paragraphs.append(p)
    #         else:
    #             in_children = True
    #             if p.is_structure and p.level <= level:  # if p is higher in hierarchy, then the child is completed
    #                 if container_paragraphs or container_title:
    #                     if level <= len(index):
    #                         index = index[:level]
    #                         index[-1] += 1
    #                     else:
    #                         for i in range(level-len(index)):
    #                             index.append(1)
    #                     children.append(Container(container_paragraphs, container_title, level, index.copy(), self))
    #                 container_paragraphs = []
    #                 container_title = p
    #                 level = p.level
    #             else:  # p is normal text or strictly lower in hierarchy, then the child continues to grow
    #                 container_paragraphs.append(p)
    #     if container_paragraphs or container_title:
    #         if level <= len(index):
    #             index = index[:level]
    #             index[-1] += 1
    #         else:
    #             for i in range(level - len(index)):
    #                 index.append(1)
    #         children.append(Container(container_paragraphs, container_title, level, index.copy(), self))

    #     return attached_paragraphs, children



    # def create_children(self, paragraphs: [Paragraph], level: int, index: [int]):
    #     """
    #     Creates children containers and/or directly attached content and returns the list of attached content and the list of children containers.
    #     The indexes correspond to the indexes of the paragraphs in the content and also on the structure.
    #     :return: List of Content or Container
    #     """
    #     attached_paragraphs = []
    #     children = []
    #     in_children = False
    #     level = INFINITE
    #     # container_paragraphs = []
    #     # container_title = None

    #     while paragraphs:
    #         p = paragraphs.pop(0)

    #         if not in_children and p.is_structure and level != INFINITE:
    #             paragraphs.insert(0, p)
    #             children.append(Container(paragraphs, title=p, level=p.level, children=children, index=index.copy(), father=self))
    #         else:
    #             in_children = True
    #             if p.is_structure and p.level <= level:  # if p is higher in hierarchy, then the child is completed
    #                 level = p.level
    #                 if len(index) == level:
    #                     index[-1] += 1
    #                 elif len(index) < level:
    #                     if self.children != []:
    #                         index = self.children[-1].index.copy()
    #                         index[-1] += 1
    #                     else:
    #                         index.append(1)
    #                 else:
    #                     index = index[:level]
    #                     index[-1] += 1
    #                 while paragraphs:
    #                     p = paragraphs.pop(0)
    #                     if p.is_structure:
    #                         paragraphs.insert(0, p)
    #                         break
    #                     else:
    #                         attached_paragraphs.append(p)
    #                 if paragraphs and p.level > level:
    #                     in_children = False
    #                     children.append(Container(paragraphs, title=p, level=p.level, index=index.copy(), father=self))
    #                 else:
    #                     break
    #     return attached_paragraphs, children
    
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