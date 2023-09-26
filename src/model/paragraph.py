import string

INFINITE = 10000

class Paragraph:
    def __init__(self, text : str, font_style : str, id_ : int, page_id : int):
        self.font_style = font_style
        self.id_ = int(str(2)+str(page_id)+str(id_))
        self.page_id = page_id
        self.level = int(font_style[-1]) if 'title' in font_style else INFINITE
        self.is_structure = self.level < INFINITE
        self.text = text

    @property
    def blank(self):
        """
        checks if the paragraph is blank: i.e. it brings some signal (it may otherwise be ignored)
        """
        text = self.text.replace('\n', '')
        return set(text).isdisjoint(string.ascii_letters)