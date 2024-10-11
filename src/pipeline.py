import os
from utils.parser import parsers
from rag.chunking import Chunking
from rag.embedding import Embeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def rag_pipeline(selected_file, embedding_model, vector_store):
    # Extract content from file
    if selected_file.endswith('.pdf'):
        file_text = parsers.pdf_extract_content([selected_file])
    elif selected_file.endswith('.docx'):
        file_text = parsers.doc_extract_content([selected_file])
    else:
        raise ValueError("Unsupported file type. Please select a PDF or DOCX file.")

    if not file_text.strip():
        raise ValueError("No text extracted from the selected file.")

    # Chunking, embedding, and vector store
    text_chunks = Chunking.get_chunks(file_text)
    embeddings = Embeddings.get_embeddings(embedding_model)
    vectorstore = Embeddings.vectorization(vector_store, text_chunks, embeddings)

    # Configure LLM and conversation chain
    llm = ChatOpenAI(model="gpt-4", max_tokens=4096, temperature=0.1)

    # Load prompt template from file
    with open('prompts/pipeline_prompt.txt', 'r') as file:
        prompt_template = file.read()
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

if __name__ == "__main__":
    input_folder = "/Users/aatif/reasoning_researcher/inputs"
    available_files = [f for f in os.listdir(input_folder) if f.endswith(('.pdf', '.docx'))]

    if not available_files:
        print("No PDF or DOCX files found in the folder.")
    else:
        for idx, file in enumerate(available_files, 1):
            print(f"{idx}. {file}")

        selected_file = os.path.join(input_folder, available_files[int(input("Select a file by number: ")) - 1])
        
        available_embeddings = Embeddings.get_available_embeddings()
        for idx, emb in enumerate(available_embeddings, 1):
            print(f"{idx}. {emb}")
        embedding_model = available_embeddings[int(input("Select an embedding model by number: ")) - 1]

        available_vectorstores = Embeddings.get_available_vectorstores()
        for idx, store in enumerate(available_vectorstores, 1):
            print(f"{idx}. {store}")
        vector_store = available_vectorstores[int(input("Select a vector storage type by number: ")) - 1]

        query = input("\nWhat do you need to know about this research paper: ")
        conversation_chain = rag_pipeline(selected_file, embedding_model, vector_store)
        response = conversation_chain({"question": query})

        print("\nSummary:\n", response['answer'])
        