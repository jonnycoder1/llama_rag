from logger import get_logger, ic, timer
logger = get_logger(__file__)
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import os.path


class IndexHelper:
    @timer
    def get_index(self):
        persist_dir = "./storage"
        if not os.path.exists(persist_dir):
            ic(persist_dir, 'index not found. creating new one')
            documents = SimpleDirectoryReader("data").load_data()
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist(persist_dir)
        else:
            ic('loading existing index from storage')
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            index = load_index_from_storage(storage_context)
        return index


class QueryHelper:
    def __init__(self, index):
        self.query_engine = index.as_query_engine()

    @timer
    def run_query(self, query):
        ic(query)
        response = self.query_engine.query(query)
        return response


if __name__ == '__main__':
    index_manager = IndexHelper()
    query_runner = QueryHelper(index_manager.get_index())
    resp = query_runner.run_query("How do I get started in AI?")
    ic(resp.response[:300])

# Expected Output:
# 2024-01-23 17:11:21,541 - logger.py - INFO - ic| main.py:17 in get_index()- 'loading existing index from storage'
# 2024-01-23 17:11:21,779 - logger.py - INFO - get_index took 0.2944 seconds
# 2024-01-23 17:11:21,824 - logger.py - INFO - ic| main.py:29 in run_query()- query: 'How do I get started in AI?'
# 2024-01-23 17:11:33,017 - logger.py - INFO - run_query took 11.1932 seconds
# 2024-01-23 17:11:33,020 - logger.py - INFO - ic| main.py:38 in <module>
#     resp.response[:300]: ('To get started in AI, it is important to work on projects that are '
#                           'responsible, ethical, and beneficial to people. Starting with small projects '
#                           'in your spare time can be a good way to learn and gradually increase your '
#                           'skills. Joining existing projects or collaborating with others who have '
#                           'ideas can ')
