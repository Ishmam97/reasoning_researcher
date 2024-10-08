
from langchain.text_splitter import CharacterTextSplitter

class Chunking:
    def get_chunks(self,text):
        try:
            self.text = text
            text_splitter = CharacterTextSplitter(
                seperator = "\n",
                chunk_size = 500,
                chunk_overlap = 100,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
        except Exception as e:
            raise Exception(f"Error occured while chunking text {chunks}. Error: {e} ")
        
        return chunks
