import os


DATA_DIR = "../data"
CHROMA_DIR = "./chroma_store"
PROCESSED_LOG = "Processed_files.txt"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-base"
SIMILARITY_TOP_K = 4

HF_CACH_DIR = '../hf_cache_dir'
os.environ["HF_HOME"] = HF_CACH_DIR

MAX_LINE=10_000


dir_in_etl = './data/etl_input'
dir_out_etl = './data/etl_output'
seed = 42

        
data_dir = './data/etl_output'
db_dir = "./db"
embedding_model_name = 'intfloat/multilingual-e5-base'
model_llm_path = 'models_llm/mistral.gguf'
batch_size = 5_000
chunk_size = 1024
chunk_overlap = 100
hf_cache_dir = './hf_cache_dir'
embed_batch_size = 100
device = 'cuda'
top_k = 5 
CONTEXT_SIZE = 2048
