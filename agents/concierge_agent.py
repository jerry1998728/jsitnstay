import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from pinecone import Pinecone

def concierge_agent(message: str) -> str:
    # --- API Keys ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = "petsittingknowledge"

    # --- Initialize Pinecone (v3 syntax) ---
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)

    # --- LangChain Components ---
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        streaming=True,  # Token streaming enabled
        openai_api_key=OPENAI_API_KEY,
        temperature=0.7
    )
    embedder = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # ✅ Use correct VectorStore wrapper
    vectorstore = LangchainPinecone(index, embedder, text_key="text")
    retriever = vectorstore.as_retriever()

    # --- Prompt Template ---
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
            You are Jerry’s professional, friendly pet care assistant for J.Sit & Stay.

            Use the context below to help answer the user's question. 
            If pricing or rate is mentioned but not discount, organize it neatly in a table.
            Always respond with a warm, helpful tone, and avoid guessing beyond the context.

            Context:
            {context}

            Question:
            {question}
        """
    )

    # --- RAG Chain ---
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    # --- Generate Answer ---
    try:
        result = qa_chain.run(message)
        return result
    except Exception as e:
        return f"⚠️ Error generating response: {e}"
