import os
import pdfplumber as pdfp
from Ilumio_chatbot.src.model.paragraph import Paragraph

def get_pdf_title_styles(path):
    page_number = 1
    with open(path, 'rb') as f:
        reader = pdfp.PDF(f)
        for page in reader.pages:
            dictionary = page.extract_text_lines()
            for i in range(len(dictionary)):
                p = Paragraph(dictionary[i]["text"],"unknown",i,page_id=page_number)
                if dictionary[i]["chars"][0]["size"] >= 9 and dictionary[i]["chars"][0]["size"] < 12.8:
                    p.font_type = "content"
                elif dictionary[i]["chars"][0]["size"] >= 12.8 and dictionary[i]["chars"][0]["size"] <= 13.5:
                    p.font_type = "title4"
                elif dictionary[i]["chars"][0]["size"] > 13.5 and dictionary[i]["chars"][0]["size"] <= 15.5:
                    p.font_type = "title3"
                elif dictionary[i]["chars"][0]["size"] > 15.5 and dictionary[i]["chars"][0]["size"] <= 18.5:
                    p.font_type = "title2"
                elif dictionary[i]["chars"][0]["size"] > 19 and dictionary[i]["chars"][0]["size"] < 30:
                    p.font_type = "title1"
                if(i != len(dictionary)-1):
                    while(dictionary[i+1]["chars"][0]["size"] == dictionary[i]["chars"][0]["size"]):
                        p.text += " " + dictionary[i+1]["text"]
                        i += 1
                        if(i == len(dictionary)-1):
                            break
                print(f'{i} : {p.font_type} ->>>>> {p.text}')
            page_number += 1


def test_get_font_sizes_of_a_page(page : int, path):
    with open(os.path.abspath(path)) as f:
        reader = pdfp.PDF(f)
        page = reader.pages[page]
        dictionary = page.extract_text_lines()
        for i in range(len(dictionary)):
            print(f'{i} : {dictionary[i]["chars"][0]["size"]} ->>>>> {dictionary[i]["text"]}')


# path = "data/Illumio_Core_REST_API_Developer_Guide_23.3.pdf"
# get_pdf_title_styles(os.path.abspath(path))
# print("--------------------------------------------------")
# print("--------------------------------------------------")
#print(test_get_font_sizes_of_a_page(8))