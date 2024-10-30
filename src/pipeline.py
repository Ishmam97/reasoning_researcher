import os
from utils.parser import parsers
from rag.chunking import Chunking
from rag.embedding import Embeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

class RAGPipeline:
    def __init__(self, selected_file, embedding_model, vector_store):
        self.selected_file = selected_file
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.llm = self.configure_llm()
        self.prompt = self.load_prompt_template()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def configure_llm(self):
        return ChatOpenAI(model="gpt-4o-mini", max_tokens=4096, temperature=0.1)

    def load_prompt_template(self):
        with open('prompts/pipeline_prompt.txt', 'r') as file:
            prompt_template = file.read()
        return PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    def extract_content(self):
        if self.selected_file.endswith('.pdf'):
            return parsers.pdf_extract_content([self.selected_file])
        elif self.selected_file.endswith('.docx'):
            return parsers.doc_extract_content([self.selected_file])
        else:
            raise ValueError("Unsupported file type. Please select a PDF or DOCX file.")

    def process_file(self):
        file_text = self.extract_content()
        if not file_text.strip():
            raise ValueError("No text extracted from the selected file.")
        
        text_chunks = Chunking.get_chunks(file_text)
        embeddings = Embeddings.get_embeddings(self.embedding_model)
        vectorstore = Embeddings.vectorization(self.vector_store, text_chunks, embeddings)
        
        return vectorstore

    def create_conversational_chain(self):
        vectorstore = self.process_file()
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(),
            memory=self.memory,
            verbose=True,
            combine_docs_chain_kwargs={"prompt": self.prompt},
        )

def get_user_selection(prompt, options):
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    selection = int(input(prompt)) - 1
    return options[selection]

def main():
    input_folder = "inputs/"
    available_files = [f for f in os.listdir(input_folder) if f.endswith(('.pdf', '.docx'))]

    if not available_files:
        print("No PDF or DOCX files found in the folder.")
        return

    selected_file = os.path.join(input_folder, get_user_selection("Select a file by number: ", available_files))
    
    available_embeddings = Embeddings.get_available_embeddings()
    embedding_model = get_user_selection("Select an embedding model by number: ", available_embeddings)

    available_vectorstores = Embeddings.get_available_vectorstores()
    vector_store = get_user_selection("Select a vector storage type by number: ", available_vectorstores)

    query = input("\nWhat do you need to know about this research paper: ")
    pipeline = RAGPipeline(selected_file, embedding_model, vector_store)
    conversation_chain = pipeline.create_conversational_chain()
    response = conversation_chain({"question": query})

    print("\nSummary:\n", response['answer'])

if __name__ == "__main__":
    main()
