from src.model.paragraph import Paragraph


#function that pretty prints the paragraphs
def pretty_printer(paragraphs):
    for p in paragraphs:
        if (p.font_style == "title1"):
            print(f"Titre 1 {p.text}")
        elif (p.font_style == "title2"):
            print(f"---> Titre 2 {p.text}")
        elif (p.font_style == "title3"):
            print(f"-------> Titre 3 {p.text}")
        # elif (p.font_style == "title4"):
        #     print(f"-----------> Titre 4 {p.text}")
        # elif (p.font_style == "content"):
        #     print(f"---------------> {p.text}")