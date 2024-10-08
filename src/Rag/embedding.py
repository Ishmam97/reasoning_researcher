from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import Qdrant
from langchain.vectorstores import FAISS


class Embeddings:
    def get_embeddings(self,embeddings):
        try:
            self.embeddings = embeddings
            embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")

        except Exception as e:
            raise Exception(f"Cannot load embedding model : {embeddings}. Error : {e}")
    
        return embeddings
    
    def vectorization(self,text_chunks):
        load_dotenv()
        self.text_chunks = text_chunks
        vectorstore = FAISS.from_texts(
            texts = text_chunks,
            embedding = self.embeddings
        )
        return vectorstore
