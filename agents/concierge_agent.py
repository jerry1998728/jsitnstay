from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain.prompts import PromptTemplate
from pinecone import Pinecone
from openai import OpenAI


def concierge_agent(message: str) -> str:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    pinecone_index_name = "petsittingknowledge"

    # LangChain LLM & Embeddings
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        streaming=True,  # set to True if handling tokens in Streamlit manually
        openai_api_key=OPENAI_API_KEY,
        temperature=0.7
    )
    embedder = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Pinecone setup
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(pinecone_index_name)
    vectorstore = LangchainPinecone(index, embedder, text_key="text")
    retriever = vectorstore.as_retriever()

    # Prompt Template
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
                You are Jerry’s professional, friendly pet care assistant for J.Sit & Stay.
                
                Use the context below to help answer the user's question. If pricing or rate is mentioned but not discount, organize it neatly in a table.
                
                Always respond with a warm, helpful tone, and avoid guessing beyond the context.
                
                Context:
                {context}
                
                Question:
                {question}
                """
                    )

    # Build RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    try:
        result = qa_chain.run(message)
        return result
    except Exception as e:
        return f"⚠️ Error generating response: {e}"
