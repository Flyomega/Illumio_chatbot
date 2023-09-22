class Block:
    def __init__(self, title: str = '', content: str = '',
                 index: str = '', rank: int = 0, level: int = 0, distance: float = 99999):
        self.title = title
        self.content = content
        self.index = index
        self.rank = rank
        self.level = level
        self.distance = distance

    def to_dict(self) -> {}:
        block_dict = {'title': self.title,
                      'content': self.content,
                      'index': self.index,
                      'rank': self.rank,
                      'level': self.level,
                      'distance': self.distance}
        return block_dict

    def from_dict(self, block_dict: {}):
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
