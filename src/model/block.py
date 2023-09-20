class Block:
    def __init__(self, doc: str = '', title: str = '', content: str = '', content_fr: str = '',
                 index: str = '', rank: int = 0, level: int = 0, distance: float = 99999):
        self.doc = doc
        self.title = title
        self.title_fr = ""
        self.content = content
        self.content_fr = content_fr
        self.specials = []
        self.index = index
        self.rank = rank
        self.level = level
        self.distance = distance

    def to_dict(self) -> {}:
        block_dict = {'doc': self.doc,
                      'title': self.title,
                      'title_fr': self.title_fr,
                      'content': self.content,
                      'content_fr': self.content_fr,
                      'index': self.index,
                      'rank': self.rank,
                      'level': self.level,
                      'distance': self.distance}
        for i, s in enumerate(self.specials):
            special_key = 'special_'+str(i)
            block_dict[special_key] = s
        block_dict['specials_len'] = len(self.specials)
        return block_dict

    def from_dict(self, block_dict: {}):
        self.doc = block_dict['doc']
        self.title = block_dict['title']
        self.title_fr = block_dict['title_fr']
        self.content = block_dict['content']
        self.content_fr = block_dict['content_fr']
        self.index = block_dict['index']
        self.rank = block_dict['rank']
        self.level = block_dict['level']
        self.distance = block_dict['distance']
        self.specials = []
        for i in range(block_dict['specials_len']):
            special_key = 'special_' + str(i)
            self.specials.append(block_dict[special_key])
        return self

    @property
    def distance_str(self) -> str:
        return format(self.distance, '.2f')
