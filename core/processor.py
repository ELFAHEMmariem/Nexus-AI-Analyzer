import os
import requests
import whisper
import yt_dlp
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    UnstructuredImageLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        # On charge le modèle Whisper (le modèle "base" est rapide et efficace)
        self.audio_model = whisper.load_model("base")

    def process_file(self, file_path):
        # --- 1. DÉTECTION YOUTUBE ---
        if "youtube.com" in file_path or "youtu.be" in file_path:
            return self._handle_youtube_audio(file_path)

        # --- 2. GESTION DES FICHIERS LOCAUX ---
        ext = os.path.splitext(file_path)[-1].lower()
        try:
            if ext == '.pdf':
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif ext in ['.png', '.jpg', '.jpeg']:
                loader = UnstructuredImageLoader(file_path)
                documents = loader.load()
            else:
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()

            return self.text_splitter.split_documents(documents)
        except Exception as e:
            raise Exception(f"Erreur format {ext} : {str(e)}")

    def _handle_youtube_audio(self, url):
        """
        Télécharge l'audio de la vidéo et utilise Whisper pour 'écouter' le contenu.
        """
        temp_audio = "temp_audio.mp3"
        try:
            # 1. Configuration du téléchargement audio (yt-dlp)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'temp_audio', # Le fichier sera temp_audio.mp3
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # 2. Transcription par l'IA Whisper (Elle écoute la vidéo)
            result = self.audio_model.transcribe(temp_audio)
            full_text = result['text']

            # 3. Nettoyage et création du document
            metadata = {"source": url, "type": "video_transcription"}
            doc = Document(page_content=full_text, metadata=metadata)

            return self.text_splitter.split_documents([doc])

        except Exception as e:
            raise Exception(f"Échec de l'écoute vidéo (Whisper) : {str(e)}")
        finally:
            # Suppression du fichier audio temporaire
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
            # Parfois yt-dlp ajoute l'extension après
            if os.path.exists("temp_audio.mp3"):
                os.remove("temp_audio.mp3")