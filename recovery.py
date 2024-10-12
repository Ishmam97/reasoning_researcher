import os
from utils.parser import parsers
from rag.chunking import Chunking
from rag.embedding import Embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def rag_pipeline(input_folder, select_embedding='small', store_select='qdrant'):
    pdf_files = []
    doc_files = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
            elif file.endswith('.docx'):
                doc_files.append(os.path.join(root, file))

    pdf_text = parsers.pdf_extract_content(pdf_files)
    doc_text = parsers.doc_extract_content(doc_files)

    if not pdf_text and not doc_text:
        raise ValueError("No text extracted from the provided files.")
    
    # Step 2: Adaptive Chunking with Overlaps
    pdf_chunks = Chunking.get_chunks(pdf_text)  # 20% overlap between chunks for better context
    text_chunks = pdf_chunks

    # Improved Embedding Selection
    embeddings = Embeddings.get_embeddings(select_embedding)
    vectorstore = Embeddings.vectorization(store_select, text_chunks, embeddings)

    # Configuring LLM with System Prompt for Higher Quality Outputs
    llm = ChatOpenAI(
        model="gpt-4",
        max_tokens=4096,
        temperature=0.1
    )

    # Create a retriever from the vectorstore
    prompt_template = """
    You are a respectful and honest assistant. You have to answer the user's questions using only the context
    provided to you. If you don't know the answer, just say you don't know. Don't try to make up an answer.\n\n
    Context:\n {context}\n
    Question: \n{question}\n

    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Memory for conversational context
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Conversational retrieval chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    return conversation_chain


if __name__ == "__main__":
    input_folder = "/Users/aatif/reasoning_researcher/inputs"
    query = input("What do you need to know about this research paper: ")

    # Initialize the RAG pipeline and get the conversation chain
    conversation_chain = rag_pipeline(input_folder)

    # Run the conversation chain with the given query
    response = conversation_chain({"question": query})

    print("Summary:\n", response['answer'])
