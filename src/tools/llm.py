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

