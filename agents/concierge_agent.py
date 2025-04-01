import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
import pinecone


def concierge_agent(message: str) -> str:
    # --- API Keys ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    pinecone_index_name = "petsittingknowledge"

    # --- Initialize Pinecone ---
    pinecone.init(api_key=PINECONE_API_KEY)
    index = pinecone.Index(pinecone_index_name)

    # --- LangChain Components ---
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        streaming=True,  # You can stream token-by-token
        openai_api_key=OPENAI_API_KEY,
        temperature=0.7
    )
    embedder = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = PineconeVectorStore(index_name=pinecone_index_name, embedding=embedder)
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
