## Overview
llama_rag is a llamaindex starter project for performing retrieval augmented generation.
RAG is a technique for improving accuracy of generative AI models by fetching related 
facts from external sources and including that data in the user query prompt to the LLM.

More information found at:
https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html

In this repo, your data files are loaded from the ./data directory and prepared for indexing 
in a vector data store, persisted under ./storage.

## Getting Started

- Run the following in the terminal to create a virtual environment and install dependencies:
```
virtualenv venv
source venv/bin/activate
pip install icecream
pip install llama-index
pip install setuptools
pip install pypdf
```

- Set the OpenAI API Key as an environment variable:
```
export OPENAI_API_KEY=XXX 
``` 

- Run main.py

- (Optional) Delete ./storage folder and re-run main.py to reindex the files under ./data
