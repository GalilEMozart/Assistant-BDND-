from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.logger import logger as log
import gc


#from langchain.vectorstores import Chroma
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from llama_cpp import Llama

import src.config as config
from src.logger import logger as log

import atexit
import multiprocessing

class RAG:
    """ RAG pipeline """
    
    def __init__(
        self
    ):
        # Retriever setup
        self.embeddings = HuggingFaceEmbeddings(model_name=config.embedding_model_name)
        self.db = Chroma(
            persist_directory=config.db_dir,
            embedding_function=self.embeddings
        )
        
        self.top_k = config.top_k

        # LLM setup
        self.llm = Llama(
            model_path=config.model_llm_path,
            n_ctx=2048,
            n_threads=8,
            n_gpu_layers=-1,
            verbose=False
        )

        log.info('rag engine initialiser ')

    def retrieve(self, query: str):
        """ classe that retriever context """    
        return self.db.similarity_search(query, k=self.top_k)

    def generate(self, context: str, question: str) -> str:
        """ Generate response from llm with context infos """
        
        prompt = f"""
        Tu es un assistant d'analyse de données immobilières. Fournis UNIQUEMENT les réponses exactes demandées, et repond en francais.

        Contexte:
        {context}

        Question: {question}
        """
        

        output = self.llm(prompt, max_tokens=512, temperature=0.7)
        return output["choices"][0]["text"].strip()

    def run(self, question: str) -> str:
        """ run query (questions)"""
        
        docs = self.retrieve(question)
        context = "\n\n".join(doc.page_content for doc in docs)
        res = self.generate(context, question)

        log.info(question)
        log.info(context)
        log.info(res)

        return res

    def close(self):
        """libere les ressources"""

        if hasattr(self.llm, 'release') and callable(self.llm.release):
            self.llm.release()
        del self.llm

        if hasattr(self.db, 'reset'):
            self.db.reset()
        del self.db

        del self.embeddings

        gc.collect()

def cleanup_resources():
    if hasattr(multiprocessing, 'resource_tracker'):
        multiprocessing.resource_tracker._resource_tracker.clear()

atexit.register(cleanup_resources)


if __name__=='__main__':

    Rag_pipeline = RAG()

    while True:
        try:
            query = input("Posez votre question (Ctrl+C pour quitter): ")
            print(f"\nQuestion : {query}\n")
            response = Rag_pipeline.run(query)
            print(f"Réponse : {response}\n")
        except KeyboardInterrupt:
            print("\nArrêt du programme...")
            break
