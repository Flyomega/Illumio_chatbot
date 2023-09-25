from src.model.container import Container
from src.model.block import Block

class Retriever:
    def __init__(self,db_client,container:Container,collection_name:str):
        self.collection = db_client.create_collection(name=collection_name)
        blocks_good_format: [Block] = self.get_blocks(container)
        self.collection.add(
            documents=[block.content for block in blocks_good_format],
            ids=[block.index for block in blocks_good_format],
            metadatas=[block.to_dict() for block in blocks_good_format]
        )


    def get_blocks(self,c:Container):

        def from_list_to_str(index_list):
            index_str = str(index_list[0])
            for el in index_list[1:]:
                index_str += '.' + str(el)
            return index_str

        blocks = c.blocks
        for block in blocks:
            if block.level == 0:
                blocks.remove(block)
            block.index = from_list_to_str(block.index)
        return blocks


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
        