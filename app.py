import pandas as pd
import os
import time
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

# start_time = time.time()

# doc = Doc(path=content_en_path_real)
# print("--- %s seconds ---" % (time.time() - start_time))
# check if the database is empty
# pdf_manager(pdf_path=content_en_path_real)
# pretty_printer_paragraphs(doc.container.paragraphs)
# pretty_print_container_structure(doc.container)

if not os.path.exists("database/"):
    os.makedirs("database/")

client_db = chromadb.PersistentClient(path="database/")

try: 
    client_db.get_collection(name="illumio_database")
    llm = LlmAgent(model="TheBloke/Llama-2-7b-Chat-GPTQ")
    retriever = Retriever(client_db, None, "illumio_database", llmagent=llm)
except:
    print("Database is empty")
    doc = Doc(path=content_en_path_real)
    llm = LlmAgent(model="TheBloke/Llama-2-7b-Chat-GPTQ")
    retriever = Retriever(client_db,doc.container,"illumio_database",llmagent=llm)


chat = Chatbot(llm_agent=llm, retriever=retriever)

ilumio_qna = view.run(ctrl=chat, config=view_config)

ilumio_qna.queue().launch()
