import pandas as pd
import os
from langchain.llms import OpenAI
import chromadb

from config import *
from src.control.control import Controller
from src.tools.reader import get_pdf_title_styles
from src.tools.llm import LlmAgent
import src.view.view as view
from src.model.container import Container

os.environ["TOKENIZERS_PARALLELISM"] = "true"

if not "OPENAI_API_KEY" in os.environ:
    from config_key import OPENAI_API_KEY
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


all_paragraphs = get_pdf_title_styles(os.path.abspath(content_en_path))
Pdf_container = Container(all_paragraphs, title="Illumio Core REST API Developer Guide")

client_db = chromadb.Client()

llm_model = OpenAI(temperature=0)
llm = LlmAgent(llm_model)

# qna = view.run(ctrl=controller, config=view_config)

# ilumio_qna = view.run(ctrl=controller, config=view_config)

# ilumio_qna.queue().launch()
