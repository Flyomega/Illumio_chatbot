class Block:
    def __init__(self, doc: str= '',title: str = '', content: str = '',
                 index: str = '', rank: int = 0, level: int = 0, distance: float = 99999):
        self.doc = doc
        self.title = title
        self.content = content
        self.index = index
        self.rank = rank
        self.level = level
        self.distance = distance

    def to_dict(self) -> {}:
        block_dict = {'doc': self.doc,
                      'title': self.title,
                      'content': self.content,
                      'index': self.index,
                      'rank': self.rank,
                      'level': self.level,
                      'distance': self.distance}
        return block_dict

    def from_dict(self, block_dict: {}):
        self.doc = block_dict['doc']
        self.title = block_dict['title']
        self.content = block_dict['content']
        self.index = block_dict['index']
        self.rank = block_dict['rank']
        self.level = block_dict['level']
        self.distance = block_dict['distance']
        return self

    @property
    def distance_str(self) -> str:
        return format(self.distance, '.2f')
