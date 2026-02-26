from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import Ollama  # Free local LLM

class RAGEngine:
    def __init__(self, pdf_folder="syllabus/"):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = None
        self.qa_chain = None
        self.load_syllabus(pdf_folder)

    def load_syllabus(self, folder):
        import os
        documents = []
        for file in os.listdir(folder):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(folder, file))
                documents.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)

        self.db = FAISS.from_documents(chunks, self.embeddings)

        # Use Ollama (free) — run: ollama pull llama3.2
        llm = Ollama(model="llama3.2")

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.db.as_retriever(search_kwargs={"k": 3}),
            chain_type="stuff"
        )

    def ask(self, question: str) -> str:
        result = self.qa_chain.run(question)
        return result