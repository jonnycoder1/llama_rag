from logger import logger, timer
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import os.path


class IndexHelper:
    @timer
    def get_index(self):
        persist_dir = "./storage"
        if not os.path.exists(persist_dir):
            ic('index not found. creating new one', persist_dir)
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
    logger.info("Starting main")
    index_manager = IndexHelper()
    query_runner = QueryHelper(index_manager.get_index())
    resp = query_runner.run_query("How do I get started in AI?")
    ic(resp.response[:200])


# Expected Output:
# ----------------
# 2024-01-24 08:24:44,266 - INFO - Starting main
# 2024-01-23 18:50:51,251 - INFO - ic| main.py:12 in get_index()
#     'index not found. creating new one': 'index not found. creating new one'
#     persist_dir: './storage'
# 2024-01-23 18:50:52,347 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
# 2024-01-23 18:50:52,617 - INFO - get_index took 1.4230 seconds
# 2024-01-23 18:50:52,697 - INFO - ic| main.py:29 in run_query()- query: 'How do I get started in AI?'
# 2024-01-23 18:50:52,830 - INFO - HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
# 2024-01-23 18:51:02,279 - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
# 2024-01-23 18:51:02,289 - INFO - run_query took 9.5922 seconds
# 2024-01-23 18:51:02,293 - INFO - ic| main.py:38 in <module>
#     resp.response[:200]: ('To get started in AI, it is important to work on projects that are '
#                           'responsible, ethical, and beneficial to people. Starting with small projects '
#                           'in your spare time can help you learn and gradually incr')
