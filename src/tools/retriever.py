from src.model.container import Container
from src.model.block import Block

class Retriever:
    def __init__(self,db_client,container:Container,collection_name:str):
        self.collection = db_client.create_collection(name=collection_name)
        self.collection.add(
            documents=[block.content for block in container.blocks],
            ids=[block.index for block in container.blocks],
            metadatas=[block.to_dict() for block in container.blocks]
        )


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
        