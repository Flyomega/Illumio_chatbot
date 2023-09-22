import pandas as pd

from src.tools.retriever import Retriever
from src.tools.llm import LlmAgent
from src.model.block import Block


class Chatbot:
    def __init__(self, llm_agent, retriever):
        self.retriever = retriever
        self.llm = llm_agent

    def get_response(self, query, histo):
        histo_conversation, histo_queries = self._get_histo(histo)
        queries = histo_queries
        block_sources = self.retriever.similarity_search(query=queries)
        block_sources = self._select_best_sources(block_sources)
        sources_contents = [s.content for s in block_sources]
        context = '\n'.join(sources_contents)
        answer = self.llm.generate_paragraph(query=queries, histo=histo_conversation, context=context, language='en')
        answer = self.llm.generate_answer(answer_en=answer, query=query, histo=histo_conversation, context=context)
        answer = self._clean_answer(answer)
        return answer, block_sources

    

    @staticmethod
    def _select_best_sources(sources: [Block], delta_1_2=0.15, delta_1_n=0.3, absolute=1.2, alpha=0.9) -> [Block]:
        """
        Select the best sources: not far from the very best, not far from the last selected, and not too bad per se
        """
        best_sources = []
        for idx, s in enumerate(sources):
            if idx == 0 \
                    or (s.distance - sources[idx - 1].distance < delta_1_2
                        and s.distance - sources[0].distance < delta_1_n) \
                    or s.distance < absolute:
                best_sources.append(s)
                delta_1_2 *= alpha
                delta_1_n *= alpha
                absolute *= alpha
            else:
                break
        return best_sources
    

    @staticmethod
    def _get_histo(histo: [(str, str)]) -> (str, str):
        histo_conversation = ""
        histo_queries = ""

        for (query, answer) in histo[-5:]:
            histo_conversation += f'user: {query} \n bot: {answer}\n'
            histo_queries += query + '\n'
        return histo_conversation[:-1], histo_queries
    

    @staticmethod
    def _clean_answer(answer: str) -> str:
        answer = answer.strip('bot:')
        while answer and answer[-1] in {"'", '"', " ", "`"}:
            answer = answer[:-1]
        while answer and answer[0] in {"'", '"', " ", "`"}:
            answer = answer[1:]
        answer = answer.strip('bot:')
        if answer:
            if answer[-1] != ".":
                answer += "."
        return answer