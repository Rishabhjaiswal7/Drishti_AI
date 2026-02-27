from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

class RAGEngine:
    def __init__(self, pdf_folder="syllabus/"):
        print("Loading embeddings model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.retriever = None
        self.chain = None
        self.load_syllabus(pdf_folder)

    def load_syllabus(self, folder):
        documents = []

        if not os.path.exists(folder):
            print(f"❌ Folder '{folder}' not found!")
            return

        for file in os.listdir(folder):
            if file.endswith(".pdf"):
                print(f"📄 Loading: {file}")
                loader = PyPDFLoader(os.path.join(folder, file))
                documents.extend(loader.load())

        if not documents:
            print("❌ No PDFs found in syllabus/ folder!")
            return

        print(f"✅ Loaded {len(documents)} pages")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")

        db = FAISS.from_documents(chunks, self.embeddings)
        self.retriever = db.as_retriever(search_kwargs={"k": 3})
        print("✅ Vector database ready")

        llm = Ollama(model="llama3.2")

        prompt = PromptTemplate.from_template("""
You are DRISHTI-AI, a helpful education assistant for visually impaired students.
Answer the question based only on the following context from the syllabus.
Keep your answer clear and simple.

Context: {context}

Question: {question}

Answer:""")

        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        print("✅ AI model connected and ready!")

    def ask(self, question: str) -> str:
        if not self.chain:
            return "System not ready. Please check your syllabus folder."
        return self.chain.invoke(question)