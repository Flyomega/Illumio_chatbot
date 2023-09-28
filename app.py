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
from src.model.doc import Doc
from src.tools.test_read import pdf_manager

os.environ["TOKENIZERS_PARALLELISM"] = "true"

if not "OPENAI_API_KEY" in os.environ:
    from config_key import OPENAI_API_KEY
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

#check if the database is empty
# pdf_manager(pdf_path=content_en_path_real)
# pretty_printer_paragraphs(doc.container.paragraphs)
# pretty_print_container_structure(doc.container)

if not os.path.exists("Ilumio_chatbot/database/"):
    os.makedirs("Ilumio_chatbot/database/")

client_db = chromadb.PersistentClient(path="Ilumio_chatbot/database/")

try: 
    client_db.get_collection(name="illumio_database")
    retriever = Retriever(client_db, None, "illumio_database")
except:
    print("Database is empty")
    doc = Doc(path=content_en_path_real)
    retriever = Retriever(client_db,doc.container,"illumio_database")

llm_model = OpenAI(temperature=0)
llm = LlmAgent(llm_model)

chat = Chatbot(llm_agent=llm, retriever=retriever)

ilumio_qna = view.run(ctrl=chat, config=view_config)

ilumio_qna.queue().launch()
