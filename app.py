import pandas as pd
import os
from langchain.llms import OpenAI
import chromadb

from config import *
from src.tools.reader import get_pdf_title_styles
from src.tools.llm import LlmAgent
import src.view.view as view
from src.tools.pretty_print import pretty_print_container_structure, pretty_printer_paragraphs
from src.model.container import Container
from src.control.control import Chatbot
from src.tools.retriever import Retriever

os.environ["TOKENIZERS_PARALLELISM"] = "true"

if not "OPENAI_API_KEY" in os.environ:
    from config_key import OPENAI_API_KEY
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


all_paragraphs = get_pdf_title_styles(os.path.abspath(content_en_path_real))
# pretty_printer_paragraphs(all_paragraphs)
Pdf_container = Container(all_paragraphs)
# pretty_print_container_structure(Pdf_container)


client_db = chromadb.Client()

retriever = Retriever(client_db,Pdf_container,"test")

llm_model = OpenAI(temperature=0)
llm = LlmAgent(llm_model)

chat = Chatbot(llm_agent=llm, retriever=retriever)

ilumio_qna = view.run(ctrl=chat, config=view_config)

ilumio_qna.queue().launch()
