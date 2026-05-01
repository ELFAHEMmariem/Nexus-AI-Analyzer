# 🚀 Nexus-AI-Analyzer (Multimodal RAG)

**Nexus-AI-Analyzer** est une plateforme d'intelligence artificielle avancée basée sur l'architecture **RAG (Retrieval-Augmented Generation)**. Elle permet d'interroger intelligemment des documents **PDF** et des contenus **vidéos** avec une précision contextuelle élevée.

## 💡 Concept
L'application traite les sources textuelles et audiovisuelles pour les transformer en vecteurs numériques. Grâce à cette approche, le LLM peut retrouver des informations précises dans un document de 100 pages ou dans une vidéo spécifique pour répondre aux questions sans "hallucinations".

## 🛠️ Stack Technique
* **Moteur d'IA :** LLaMA 3 via l'API **Groq** (Inférence ultra-rapide).
* **Embeddings :** Google Generative AI (Vectorisation sémantique).
* **Framework RAG :** LangChain.
* **Traitement Vidéo :** Whisper / Transcription et analyse temporelle.
* **Base de Données Vectorielle :** ChromaDB.
* **Interface :** Streamlit.

## 📂 Structure du Projet
Le code est organisé de manière modulaire :
* `app.py` : Interface utilisateur Streamlit et gestion des uploads (PDF/Vidéo).
* `core/` :
    * `processor.py` : Parsing des PDF et extraction audio/texte des vidéos.
    * `brain.py` : Orchestration de la chaîne de réponse (LLM + Contexte).
    * `vector_store.py` : Indexation et recherche sémantique.


