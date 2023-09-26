from src.model.container import Container
from src.model.paragraph import Paragraph
from src.tools.reader import get_pdf_title_styles


class Doc:

    def __init__(self, path='', id_=None):

        self.title = path.split('/')[-1]
        self.id_ = id(self)
        self.path = path
        paragraphs = get_pdf_title_styles(path)
        self.container = Container(paragraphs, father=self, level=0)
        self.blocks = self.get_blocks()

    @property
    def structure(self):

        return self.container.structure

    def get_blocks(self):

        def from_list_to_str(index_list):
            index_str = str(index_list[0])
            for el in index_list[1:]:
                index_str += '.' + str(el)
            return index_str

        blocks = self.container.blocks
        for block in blocks:
            block.doc = self.title
            if block.level == 0:
                blocks.remove(block)
            block.index = from_list_to_str(block.index)
            print(block.index + ' ------> ' + block.content)
        return blocks
"""
    current_level = len(current_index)
    if 0 < block.level:
        if block.level == current_level:
            current_index[-1] += 1
        elif current_level < block.level:
            current_index.append(1)
        elif block.level < current_level:
            current_index = current_index[:block.level]
            current_index[-1] += 1
        block.index = from_list_to_str(current_index)
    else:
        block.index = "0"
"""