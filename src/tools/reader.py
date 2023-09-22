import os
import pdfplumber as pdfp
from src.model.paragraph import Paragraph


# def get_pdf_title_styles(path):
#     paragraphs = []
#     page_number = 1
#     with open(path, 'rb') as f:
#         reader = pdfp.PDF(f)
#         skip_table_of_contents = reader.pages[9:]
#         j = 0
#         while j < len(skip_table_of_contents):
#             dictionary = skip_table_of_contents[j].extract_text_lines()
#             i = 0
#             while i < len(dictionary):
#                 if(dictionary[i]["text"].startswith("RESTAPIDeveloperGuide")): # or dictionary[i]["chars"][0]["fontname"] == "TLIFYT+Gotham-Bold-Identity-H"
#                     i+=1
#                     continue
#                 p = Paragraph(dictionary[i]["text"],"unknown",i,page_id=page_number)
#                 if dictionary[i]["chars"][0]["size"] >= 9 and dictionary[i]["chars"][0]["size"] < 12.8:
#                     p.font_style = "content"
#                 elif dictionary[i]["chars"][0]["size"] >= 12.8 and dictionary[i]["chars"][0]["size"] <= 13.5:
#                     p.font_style = "title4"
#                 elif dictionary[i]["chars"][0]["size"] > 13.5 and dictionary[i]["chars"][0]["size"] <= 15.5:
#                     p.font_style = "title3"
#                 elif dictionary[i]["chars"][0]["size"] > 15.5 and dictionary[i]["chars"][0]["size"] <= 18.5:
#                     p.font_style = "title2"
#                 elif dictionary[i]["chars"][0]["size"] > 19 and dictionary[i]["chars"][0]["size"] < 30:
#                     p.font_style = "title1"
#                 if(i != len(dictionary)-1):
#                     while(dictionary[i+1]["chars"][0]["size"] == dictionary[i]["chars"][0]["size"]):
#                         p.text += " " + dictionary[i+1]["text"]
#                         i += 1
#                         if(i == len(dictionary)-1):
#                             j+=1
#                             dictionary = skip_table_of_contents[j].extract_text_lines()
#                             i = 0
#                 else:
#                     p.text = dictionary[i]["text"]
#                 i += 1
#                 print(f'{p.page_id} : {p.font_style} ->>>>> {p.text}')
#                 paragraphs.append(p)
#             page_number += 1
#     return paragraphs


def get_pdf_title_styles(path):
    pdf_to_read = extract_all_lines_from_the_doc(path)
    paragraphs = []
    j = 0
    while j < len(pdf_to_read):
        dictionary = pdf_to_read[j]["content"]
        i = 0
        while i < len(dictionary):
            print(f"{dictionary[i]['chars'][0]} : {dictionary[i]['text']}")
            if(dictionary[i]["text"].startswith("RESTAPIDeveloperGuide")): #or dictionary[i]["chars"][0]["fontname"] == "NWDZGN+Gotham-Book-Identity-H")
                i+=1
                continue
            p = Paragraph(dictionary[i]["text"],"unknown",i,page_id=pdf_to_read[j]["page_number"])
            if dictionary[i]["chars"][0]["size"] >= 9 and dictionary[i]["chars"][0]["size"] < 11.5:
                p.font_style = "content"
            elif dictionary[i]["chars"][0]["size"] >= 11.5 and dictionary[i]["chars"][0]["size"] <= 12.7:
                p.font_style = "title5"
            elif dictionary[i]["chars"][0]["size"] >= 12.8 and dictionary[i]["chars"][0]["size"] <= 13.5:
                p.font_style = "title4"
            elif dictionary[i]["chars"][0]["size"] > 13.5 and dictionary[i]["chars"][0]["size"] <= 15.5:
                p.font_style = "title3"
            elif dictionary[i]["chars"][0]["size"] > 15.5 and dictionary[i]["chars"][0]["size"] <= 18.5:
                p.font_style = "title2"
            elif dictionary[i]["chars"][0]["size"] > 19 and dictionary[i]["chars"][0]["size"] < 30:
                p.font_style = "title1"
            if(i != len(dictionary)-1):
                while(dictionary[i+1]["chars"][0]["size"] == dictionary[i]["chars"][0]["size"]):
                    p.text += " " + dictionary[i+1]["text"]
                    i += 1
                    if(i == len(dictionary)-1):
                        if(j == len(pdf_to_read)-1):
                            break
                        else:
                            if(dictionary[i]["chars"][0]["size"] == pdf_to_read[j+1]["content"][0]["chars"][0]["size"]):
                                p.text += " " + pdf_to_read[j+1]["content"][0]["text"]
                                j+=1
                                dictionary = pdf_to_read[j]["content"]
                                i = 0
                            else:
                                break
            else:
                p.text = dictionary[i]["text"]
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
        skip_table_of_contents = reader.pages[24:25]
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