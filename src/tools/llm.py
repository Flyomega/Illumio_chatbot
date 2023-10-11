from transformers import AutoModelForCausalLM, AutoTokenizer

class LlmAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate_paragraph(self, query: str, context: {}, histo: [(str, str)], language='fr') -> str:
        """generates the  answer"""
        template = (f"You are a conversation bot designed to answer to the query from users delimited by "
                    f"triple backticks: "
                    f"\\n ``` {query} ```\\n"
                    f"Your answer is based on the context delimited by triple backticks: "
                    f"\\n ``` {context} ```\\n"
                    f"You are consistent and avoid redundancies with the rest of the initial conversation in French"
                    f"delimited by triple backticks: "
                    f"\\n ``` {histo} ```\\n"
                    f"Your response shall be in {language} and shall be concise"
                    f"In case the provided context is not relevant to answer to the question, just return that you "
                    f"don't know the answer ")

        p = self.llm(template)
        print("****************")
        print(template)
        print("----")
        print(p)
        return p

    def translate(self, text: str, language="en") -> str:
        """translates"""

        languages = "`French to English" if language == "en" else "English to French"

        template = (f"    Your task consists in translating {languages}\\n"
                    f"    the following text delimited by by triple backticks: ```{text}```\n"
                    )

        p = self.llm(template)
        return p

    def generate_answer(self, query: str, answer_en: str, histo: str, context: str) -> str:
        """provides the final answer in French based on the initial query and the answer in english"""

        def _cut_unfinished_sentence(s: str):
            return '.'.join(s.split('.')[:-1])

        template = (f"Your task consists in translating the answer in French to the query "
                    f"delimited by triple backticks: ```{query}``` \\n"
                    f"You are given the answer in english delimited by triple backticks: ```{answer_en}```"
                    f"\\n You don't add new content to the answer in English but: "
                    f"\\n 1 You can use some vocabulary from the context in English delimited by triple backticks: "
                    f"```{context}```"
                    f"\\n 2 You are consistent and avoid redundancies with the rest of the initial"
                    f" conversation in English delimited by triple backticks: ```{histo}```"
                    )

        p = self.llm(template)
        # p = _cut_unfinished_sentence(p)
        return p


def transform_parahraph_into_question(prompt : str, title_doc : str = '',title_para : str = '', model_name : str = "TheBloke/Llama-2-13b-Chat-GPTQ") -> str:
    model_name_or_path = model_name
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                device_map="cuda",
                                                trust_remote_code=False,
                                                revision="main")

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token
    max_tokens = 45

    prompt_template=f'''[INST] <<SYS>>
    You are a helpful assistant.
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

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=max_tokens,num_return_sequences=1)

    res1 = tokenizer.decode(output[0][input_ids.shape[-1]:], skip_special_tokens=True)

    print(res1)
    print("-"*len(res1))
    return res1