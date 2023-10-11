from src.model.container import Container
from src.model.block import Block
from src.model.doc import Doc
from src.tools.llm import transform_parahraph_into_question

class Retriever:
    def __init__(self,db_client,doc : Doc = None, collection_name:str = "illumio_database"):
        if doc != None:
            self.collection = db_client.create_collection(name=collection_name)
            blocks_good_format: [Block] = doc.blocks
            self.collection.add(
                documents=[transform_parahraph_into_question(block.content,title_doc=doc.title,title_para=block.title) for block in blocks_good_format],
                ids=[block.index for block in blocks_good_format],
                metadatas=[block.to_dict() for block in blocks_good_format]
            )
        else:
            self.collection = db_client.get_collection(name=collection_name)



    def similarity_search(self, query: str) -> {}:
        res = self.collection.query(query_texts=query)
        block_dict_sources = res['metadatas'][0]
        distances = res['distances'][0]
        blocks = []
        for bd, d in zip(block_dict_sources, distances):
            b = Block().from_dict(bd)
            b.distance = d
            blocks.append(b)
        return blocks
        