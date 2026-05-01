import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class AIAgent:
    def __init__(self, vector_db):
        # Utilisation du modèle actif Llama 3.1
        self.llm = ChatGroq(
            temperature=0, 
            model_name="llama-3.1-8b-instant", 
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.retriever = vector_db.as_retriever()
        self.prompt = ChatPromptTemplate.from_template(
            "Réponds uniquement en te basant sur le contexte suivant :\n{context}\n\nQuestion : {question}"
        )

    def ask_question(self, question):
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        # On utilise .invoke() pour les deux appels
        answer = rag_chain.invoke(question)
        docs = self.retriever.invoke(question)
        
        return answer, docs