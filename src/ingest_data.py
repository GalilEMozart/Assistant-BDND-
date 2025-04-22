import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from tqdm import tqdm
import pandas as pd


#from langchain_chroma import Chroma
#from langchain.vectorstores import Chroma
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma


from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from src.logger import logger as log
import src.config as config

class Ingestor:
    """
    Classe permettamt d'ingerer les donnees dans une base de donnees vectorielle avec un traitement en batch
    """
    def __init__(self,
                 data_dir:str,
                 db_dir:str,
                 embedding_model_name:str,
                 batch_size:int,
                 chunk_size:int,
                 chunk_overlap:int,
                 hf_cache_dir:str, 
                 embed_batch_size:int
                 ):
        


        self.data_dir = data_dir
        self.db_dir = db_dir
        self.embedding_model_name = embedding_model_name
        self.batch_size = batch_size
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.hf_cache_dir = hf_cache_dir
        self.embed_batch_size = embed_batch_size

        os.environ["HF_HOME"] = self.hf_cache_dir

        self.embedding_model = None
        self.db = None
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap
        )

    def load_embedding_model(self) -> None:
        """ load embedding model """

        log.info('load model for ingestion ... ')
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': config.device}
        )
        
    
    def init_db(self) -> None:
        """ init db """

        log.info('Initialisation model pour ingestion ... ')
        if self.embedding_model == None:
            return None
        
        self.db = Chroma(
            persist_directory = self.db_dir,
            embedding_function = self.embedding_model
        )


    def ingest_data_dir(self):
        """ ingest data in batch """
        

        log.info('Ingestion de donnees en batch ... ')

        log.info('Ingest des donnees text pour chaque batiment...')
        
        list_files = {
            
            "batiment_description_dataset.csv": ['Description_btm', 'Ingestion des description batiments'],
            "stats_commune.csv" : ['stat', 'Ingestion des stats commune'],
            'stats_departement.csv': ['stat', 'Ingestion des stats departement'],
            'stats_dpe.csv': ['stat', 'Ingestion des stats dpe'],
            'stats_niveau_bt.csv': ['stat', 'Ingestion des stats niveau batiment'], 
            'stats_usage.csv': ['stat', 'Ingestion des stats usage des batiments']
        }
        
        for file, (col, info) in list_files.items():
            self.ingestion_file_batch(file, col, info)

        log.info("Ingestion terminee ")
        
        del self.db
        
        

    def ingestion_file_batch(self, file_name, col_name:str, log_info='')->None:

        log.info(log_info)
        for batch in tqdm(pd.read_csv(os.path.join(self.data_dir,file_name), chunksize=self.batch_size)):
                    
            docs = [
                Document(page_content=row[col_name])
                for _, row in batch.iterrows()
            ]

            split_docs = self.splitter.split_documents(docs)

            for i in range(0, len(split_docs), self.embed_batch_size):
                doc_batch = split_docs[i:i+self.embed_batch_size]
                self.db.add_documents(doc_batch)

            log.info(f"ingestion batch - {i}")
            #self.db.persist()


    def main_ingestor(self) -> None:
        
        self.load_embedding_model()
        self.init_db()
        self.ingest_data_dir()
            


if __name__ == "__main__":
    
    log.info('Debut ingestion des donnees ... ')
    ingestor = Ingestor(
        
        config.data_dir,
        config.db_dir,
        config.embedding_model_name,
        config.batch_size,
        config.chunk_size,
        config.chunk_overlap,
        config.hf_cache_dir,
        config.embed_batch_size
    
    )

    ingestor.main_ingestor()

