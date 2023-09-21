import pandas as pd
import os
from langchain.llms import OpenAI
import chromadb

from config import *
from src.control.control import Controller
from src.tools.reader import Retriever
from src.tools.llm import LlmAgent
from src.model.doc import Doc
import src.view.view as view

os.environ["TOKENIZERS_PARALLELISM"] = "true"

if not "OPENAI_API_KEY" in os.environ:
    from config_key import OPENAI_API_KEY
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


client_db = chromadb.Client()

llm_model = OpenAI(temperature=0)
llm = LlmAgent(llm_model)

# qna = view.run(ctrl=controller, config=view_config)

qna.queue().launch()
