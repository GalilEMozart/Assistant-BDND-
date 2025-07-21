from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.logger import logger as log
import gc
from langchain.schema import Document
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.agents import initialize_agent, AgentType
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from llama_cpp import Llama
import src.config as config
from src.logger import logger as log
import atexit
import multiprocessing
import os

class RAG:
    """ RAG pipeline """
    
    def __init__(self):
        # Retriever setup
        self.embeddings = HuggingFaceEmbeddings(model_name=config.embedding_model_name)
        self.db_name = "db/bdnb.sqlite3"
        self.top_k = config.top_k
        
        # Verify database file exists
        if not os.path.exists(self.db_name):
            raise FileNotFoundError(f"Database file not found: {self.db_name}")
        
        # LLM setup with improved parameters
        self.llm = LlamaCpp(
            model_path=config.model_llm_path,
            n_ctx=12000,
            n_threads=8,
            n_gpu_layers=-1,
            verbose=False,
            temperature=0.1,  # Lower temperature for more consistent SQL generation
            max_tokens=2048  # Increased for longer responses
            # Note: Removed stop parameter to avoid conflicts with agent's stop sequences
        )
        
        self.init_agent()
        log.info('RAG engine initialized successfully')
    
    def retrieve(self, query: str):
        """ Retrieve context from vector database """
        try:
            return self.db.similarity_search(query, k=self.top_k)
        except Exception as e:
            log.error(f"Error during retrieval: {e}")
            return []
    
    def generate(self, context: str, question: str) -> str:
        """ Generate response from LLM with context infos """
        prompt = f"""Tu es un assistant d'analyse de données immobilières spécialisé dans les données du 12e arrondissement de Paris.
Réponds UNIQUEMENT en français et sois précis dans tes réponses.

Contexte des données disponibles:
{context}

Question: {question}

Réponse:"""
        
        try:
            output = self.llm(prompt, max_tokens=512, temperature=0.7)
            return output["choices"][0]["text"].strip()
        except Exception as e:
            log.error(f"Error during generation: {e}")
            return "Désolé, je n'ai pas pu générer une réponse."
    
    def run(self, question: str) -> str:
        """ Run query (questions) """
        try:
            if not question or question.strip() == "":
                return "Veuillez poser une question valide."
            
            log.info(f"Processing question: {question}")
            
            # Invoke the SQL agent
            result = self.agent.invoke({"input": question})
            
            # Extract the output properly
            if isinstance(result, dict):
                response = result.get('output', str(result))
            else:
                response = str(result)
            
            log.info(f"Agent response: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Erreur lors du traitement: {str(e)}"
            log.error(error_msg)
            
            # Try to provide a helpful error message
            if "parsing" in str(e).lower():
                return "Erreur de parsing. Essayez de reformuler votre question de manière plus simple."
            elif "database" in str(e).lower():
                return "Erreur de connexion à la base de données. Vérifiez que les données sont disponibles."
            else:
                return f"Une erreur s'est produite: {error_msg}"
    
    def init_agent(self) -> None:
        """ Initialize SQL agent with proper error handling """
        try:
            # Create database connection
            sql_db = SQLDatabase.from_uri(f"sqlite:///{self.db_name}")
            
            # Test the connection (using non-deprecated method)
            tables = sql_db.get_usable_table_names()
            log.info(f"Available tables: {tables}")
            
            # Create toolkit with specific tables
            toolkit = SQLDatabaseToolkit(
                db=sql_db,
                llm=self.llm,
                include_tables=[
                    "batiment_groupe",
                    "batiment_groupe_dpe_statistique_logement", 
                    "batiment_groupe_ffo_bat",
                    "batiment_groupe_synthese_propriete_usage"
                ]
            )
            
            # Create the SQL agent with simplified configuration
            self.agent = create_sql_agent(
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                toolkit=toolkit,
                llm=self.llm,
                verbose=True,
                handle_parsing_errors=True,
                max_execution_time=300,  # 5 minute timeout
                max_iterations=5  # Limit iterations to prevent infinite loops
            )
            
            log.info("SQL agent initialized successfully")
            
        except Exception as e:
            log.error(f"Error initializing agent: {e}")
            raise
    
    def test_database_connection(self):
        """ Test database connection and show available tables """
        try:
            sql_db = SQLDatabase.from_uri(f"sqlite:///{self.db_name}")
            tables = sql_db.get_usable_table_names()
            print(f"✅ Database connected successfully")
            print(f"📊 Available tables: {tables}")
            
            # Test a simple query
            result = sql_db.run("SELECT name FROM sqlite_master WHERE type='table';")
            print(f"🔍 Tables in database: {result}")
            
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def close(self):
        """Release resources properly"""
        try:
            if hasattr(self, 'llm') and self.llm:
                if hasattr(self.llm, 'release') and callable(self.llm.release):
                    self.llm.release()
                del self.llm
                
            if hasattr(self, 'db') and self.db:
                if hasattr(self.db, 'reset'):
                    self.db.reset()
                del self.db
                
            if hasattr(self, 'embeddings'):
                del self.embeddings
                
            gc.collect()
            log.info("Resources cleaned up successfully")
            
        except Exception as e:
            log.error(f"Error during cleanup: {e}")

def cleanup_resources():
    """Global cleanup function"""
    if hasattr(multiprocessing, 'resource_tracker'):
        multiprocessing.resource_tracker._resource_tracker.clear()

# Register cleanup function
atexit.register(cleanup_resources)

if __name__ == '__main__':
    try:
        # Initialize RAG pipeline
        print("🚀 Initializing RAG pipeline...")
        rag_pipeline = RAG()
        
        # Test database connection
        print("\n🔧 Testing database connection...")
        if not rag_pipeline.test_database_connection():
            print("❌ Cannot continue without database connection")
            exit(1)
        
        print("\n✅ RAG pipeline ready!")
        print("💬 You can now ask questions about buildings in the 12th arrondissement of Paris")
        print("📝 Example: 'Quel est le plus vieux bâtiment du 12e arrondissement de Paris?'")
        print("⏹️  Press Ctrl+C to quit\n")
        
        # Main interaction loop
        while True:
            try:
                query = input("Posez votre question (Ctrl+C pour quitter): ")
                
                if not query.strip():
                    print("⚠️  Veuillez poser une question.\n")
                    continue
                
                print(f"\n❓ Question : {query}")
                print("🤔 Traitement en cours...")
                
                response = rag_pipeline.run(query)
                print(f"✨ Réponse : {response}\n")
                print("-" * 80 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Arrêt du programme...")
                break
            except Exception as e:
                print(f"❌ Erreur inattendue: {e}")
                print("🔄 Continuons...\n")
                
    except Exception as e:
        print(f"💥 Erreur critique lors de l'initialisation: {e}")
        
    finally:
        # Cleanup resources
        if 'rag_pipeline' in locals():
            rag_pipeline.close()
        print("🧹 Nettoyage des ressources terminé")
