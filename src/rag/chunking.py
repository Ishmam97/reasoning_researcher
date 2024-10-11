
from langchain.text_splitter import CharacterTextSplitter

class Chunking:

    def get_chunks(text):
        try:
            text_splitter = CharacterTextSplitter(
                separator="\n", 
                chunk_size=500,
                chunk_overlap=100,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
        except Exception as e:
            raise Exception(f"Error occurred while chunking text. Error: {e}")
        
        return chunks