import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Qdrant
from langchain_community.vectorstores import Chroma
load_dotenv()

class Embeddings:

    @staticmethod
    def get_available_embeddings():
        return ['small', 'large']

    @staticmethod
    def get_available_vectorstores():
        return ['faiss', 'qdrant', 'chroma']

    @staticmethod
    def get_embeddings(select_embedding):
        if select_embedding.lower() == 'small':
            try:
                embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            except Exception as e:
                raise Exception(f"Cannot load small embedding model. Error: {e}")
        
        elif select_embedding.lower() == 'large':
            try:
                embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
            except Exception as e:
                raise Exception(f"Cannot load large embedding model. Error: {e}")
        else:
            raise ValueError("Unsupported embedding. Choose 'small' or 'large'.")
        
        return embeddings
    
    @staticmethod
    def vectorization(store_select, text_chunks, embeddings):
        if store_select.lower() == 'faiss':
            try:
                vectorstore = FAISS.from_texts(
                    texts=text_chunks,
                    embedding=embeddings
                )
            except Exception as e:
                raise Exception(f"Cannot load FAISS vectorstore. Error: {e}")
        
        elif store_select.lower() == 'qdrant':
            try:
                vectorstore = Qdrant.from_texts(
                    texts=text_chunks,
                    url=os.getenv("QDRANT_URL"),
                    api_key=os.getenv("QDRANT_API_KEY"),
                    collection_name=os.getenv("COLLECTION_NAME"),
                    embedding=embeddings
                )
            except Exception as e:
                raise Exception(f"Cannot load Qdrant vectorstore. Error: {e}")
            
        elif store_select.lower() == 'chroma':
            try:
                vectorstore = Chroma.from_texts(
                    texts=text_chunks,
                    embedding=embeddings
                )
            except Exception as e:
                raise Exception(f"Cannot load Chroma vectorstore. Error: {e}")
        
        else:
            raise ValueError("Unsupported vector store type. Choose 'faiss', 'qdrant', or 'chroma'.")
        
        return vectorstore
