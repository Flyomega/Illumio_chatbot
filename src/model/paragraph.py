class Paragraph:
    def __init__(self, text : str, font_type : str, id_ : int, page_id : int):
        self.text = text
        self.font_type = font_type
        self.id_ = int(str(2)+str(page_id)+str(id_))
        self.page_id = page_id

