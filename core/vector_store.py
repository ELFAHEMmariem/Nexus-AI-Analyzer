import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class VectorManager:
    def __init__(self, db_directory="db_storage"):
        self.db_directory = db_directory
        # Utilise ton processeur pour créer les vecteurs gratuitement
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def create_or_load_vector_store(self, chunks=None):
        if chunks:
            return Chroma.from_documents(
                documents=chunks, 
                embedding=self.embeddings, 
                persist_directory=self.db_directory
            )
        return Chroma(
            persist_directory=self.db_directory, 
            embedding_function=self.embeddings
        )