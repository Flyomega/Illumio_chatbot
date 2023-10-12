from src.model.doc import Doc
from config import *
from src.tools.llm import LlmAgent

llmagent = LlmAgent(model="TheBloke/Llama-2-7b-Chat-GPTQ")
doc = Doc(path=content_en_path_real)
[llmagent.transform_parahraph_into_question(block.content, title_doc=doc.title,title_para=block.title) for block in doc.blocks]