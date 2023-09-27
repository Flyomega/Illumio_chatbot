import os
import pdfplumber as pdfp
from src.model.paragraph import Paragraph
import asyncio

def skip_header(dictionary):
    i = 0
    if not (dictionary[i]["chars"][0]["size"] > 19 and dictionary[i]["chars"][0]["size"] < 30):
        i+=2
    return i


def get_style_of_line(size : float):
    if size >= 9 and size < 11.5:
        return "content"
    elif size >= 11.5 and size <= 12.7:
        return "title5"
    elif size >= 12.8 and size <= 13.5:
        return "title4"
    elif size > 13.5 and size <= 15.5:
        return "title3"
    elif size > 15.5 and size <= 18.5:
        return "title2"
    elif size > 19 and size < 30:
        return "title1"
    # elif size >= 12 and size <= 14.5:
    #     return "title2"
    # elif size > 14.5 and size <= 16.5:
    #     return "title1"
    else:
        return "unknown"

def get_pdf_title_styles(path):
    pdf_to_read = extract_all_lines_from_the_doc(path)
    paragraphs = []
    j = 0
    while j < len(pdf_to_read):
        dictionary = pdf_to_read[j]["content"]
        i = skip_header(dictionary)
        while i < len(dictionary):
            #print(f"{dictionary[i]['chars'][0]} : {dictionary[i]['text']}")
            if(dictionary[i]["text"].startswith("RESTAPIDeveloperGuide")):
                i+=1
                continue
            p = Paragraph(dictionary[i]["text"],font_style=get_style_of_line(dictionary[i]["chars"][0]["size"]),id_=i,page_id=pdf_to_read[j]["page_number"])
            if(i != len(dictionary)-1):
                while(dictionary[i+1]["chars"][0]["size"] == dictionary[i]["chars"][0]["size"]):
                    p.text += " " + dictionary[i+1]["text"]
                    i += 1
                    # if(i == len(dictionary)-1):
                    #     print("PIDOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                    #     if(j == len(pdf_to_read)-1):
                    #         print("JUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")
                    #         break
                    #     else:
                    #         if(dictionary[i]["chars"][0]["size"] == pdf_to_read[j+1]["content"][0]["chars"][0]["size"]):
                    #             print("MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                    #             j += 1
                    #             p.text += " " + pdf_to_read[j]["content"][0]["text"]
                    #             dictionary = pdf_to_read[j]["content"]
                    #             i = 0
                    #         else:
                    #             print("RRIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIZ")
                    #             break
            else:
                p.text = dictionary[i]["text"]
            #print(f"{dictionary[i]['chars'][0]} : {dictionary[i]['text']}")
            i += 1
            # print(f'{p.page_id} : {p.font_style} ->>>>> {p.text}')
            paragraphs.append(p)
        j += 1
    return paragraphs


def test_get_font_sizes_of_a_page(page : int, path):
    with open(os.path.abspath(path)) as f:
        reader = pdfp.PDF(f)
        page = reader.pages[page]
        dictionary = page.extract_text_lines()
        for i in range(len(dictionary)):
            print(f'{i} : {dictionary[i]["chars"][0]["size"]} ->>>>> {dictionary[i]["text"]}')


def extract_all_lines_from_the_doc(path):
    lines_of_doc = []
    with open(path, 'rb') as f:
        reader = pdfp.PDF(f)
        skip_table_of_contents = reader.pages[8:]
        j = 0
        while j < len(skip_table_of_contents):
            lines_of_doc.append({"page_number": j+9, "content": skip_table_of_contents[j].extract_text_lines()})
            j += 1
    return lines_of_doc




# path = "data/Illumio_Core_REST_API_Developer_Guide_23.3.pdf"
# get_pdf_title_styles(os.path.abspath(path))
# print("--------------------------------------------------")
# print("--------------------------------------------------")
#print(test_get_font_sizes_of_a_page(8))