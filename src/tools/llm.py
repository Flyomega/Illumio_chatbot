from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class LlmAgent:

    def __init__(self, model :str = "TheBloke/Llama-2-7b-Chat-GPTQ"):
        self.tokenizer = AutoTokenizer.from_pretrained(model, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(model,
                                                device_map="auto",
                                                trust_remote_code=False,             #A CHANGER SELON LES MODELES, POUR CELUI DE LAMA2 CA MARCHE (celui par default)
                                                revision="main")
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_paragraph(self, query: str, context: {}, histo: [(str, str)], language='fr') -> str:
        locallm = HuggingFacePipeline(pipeline=self.pipe)
        """generates the  answer"""
        template = (f"You are a conversation bot designed to answer to the query from users delimited by "
                    f"triple backticks: "
                    f"\\n ``` {query} ```\\n"
                    f"Your answer is based on the context delimited by triple backticks: "
                    f"\\n ``` {context} ```\\n"
                    f" You are consistent and avoid redundancies with the rest of the initial conversation "
                    f"delimited by triple backticks: "
                    f"\\n ``` {histo} ```\\n"
                    f"Your response shall be in {language} and shall be concise")
        prompt = PromptTemplate(input_variables=[], template=template)
        llm_chain = LLMChain(prompt=prompt,llm=locallm)
        p = llm_chain.predict()
        # print("****************")
        # print(template)
        # print("----")
        # print(p)
        return p

    def translate(self, text: str, language="en") -> str:
        locallm = HuggingFacePipeline(pipeline=self.pipe)
        """translates"""

        # languages = "`French to English" if language == "en" else "English to French"

        tempate = (f"    Your task consists in translating in English\\n"
                    f"    the following text delimited by by triple backticks: ```{text}```\n"
                    )

        prompt = PromptTemplate(input_variables=[], template=tempate)
        llm_chain = LLMChain(prompt=prompt,llm=locallm,verbose=True)
        p = llm_chain.predict()
        return p

    def generate_answer(self, query: str, answer: str, histo: str, context: str,language : str) -> str:
        """provides the final answer in {language} based on the initial query and the answer in english"""
        def _cut_unfinished_sentence(s: str):
            return '.'.join(s.split('.')[:-1])
        locallm = HuggingFacePipeline(pipeline=self.pipe)
        template = (f"Your task consists in translating the answer in {language}, if its not already the case, to the query "
                    f"delimited by triple backticks: ```{query}``` \\n"
                    f"You are given the answer in {language} delimited by triple backticks: ```{answer}```"
                    f"\\n You don't add new content to the answer but: "
                    f"\\n 1 You can use some vocabulary from the context delimited by triple backticks: "
                    f"```{context}```"
                    f"\\n 2 You are consistent and avoid redundancies with the rest of the initial"
                    f" conversation delimited by triple backticks: ```{histo}```"
                    )
        prompt = PromptTemplate(input_variables=[], template=template)
        llm_chain = LLMChain(prompt=prompt,llm=locallm,verbose=True)
        p = llm_chain.predict()
        # p = _cut_unfinished_sentence(p)
        return p
    

    def transform_parahraph_into_question(self, prompt : str, title_doc : str = '',title_para : str = '') -> str:
        self.tokenizer.pad_token = self.tokenizer.eos_token
        max_tokens = 45

        prompt_template=f'''[INST] <<SYS>>
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
        Your job is to create a question about a paragraph of a document untitled "{title_doc}".
        The paragraph title is "{title_para}".
        If you see that the question that you are creating will not respect {max_tokens} tokens, find a way to make it shorter.
        If you see that the document paragraph seems to be code flattened, try to analyze it and create a question about it.
        If you see that the paragraph is a table, try to create a question about it.
        If you can't create a question about the paragraph, just rephrase {title_para} so that it becomes a question.
        Your response shall only contains one question, shall be concise and shall respect the following format:
        "Question: <question>"
        The paragraph you need to create a question about is the following :
        <</SYS>>
        {prompt}[/INST]

        '''
        input_ids = self.tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
        output = self.model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=max_tokens,num_return_sequences=1)

        res1 = self.tokenizer.decode(output[0][input_ids.shape[-1]:], skip_special_tokens=True)
        print(res1)
        print("-"*len(res1))
        return res1
    
    def detect_language(self, text: str) -> str:
        """detects the language"""
        locallm = HuggingFacePipeline(pipeline=self.pipe)
        template = (f"Your task consists in detecting the language of the following text delimited by triple backticks: "
                    f"```{text}```"
                    f" Your answer shall be the two letters code of the language"
                    )
        prompt = PromptTemplate(input_variables=[], template=template)
        llm_chain = LLMChain(prompt=prompt,llm=locallm,verbose=True)
        p = llm_chain.predict()
        return p
