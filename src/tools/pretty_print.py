from src.model.paragraph import Paragraph
from src.model.container import Container


#function that pretty prints the paragraphs
def pretty_printer_paragraphs(paragraphs):
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

def pretty_print_container_structure(container):
    if container.title:
        print(f"{'-'*container.level} {container.title.text}")
    for p in container.paragraphs:
        print(f"{'-'*container.level} {p.text}")
    for c in container.children:
        pretty_print_container_structure(c)