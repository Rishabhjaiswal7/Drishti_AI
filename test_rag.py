from rag_engine import RAGEngine

print("Loading syllabus... please wait")
rag = RAGEngine()
print("✅ Syllabus loaded!")

while True:
    question = input("\nAsk a question (or type 'quit'): ")
    if question.lower() == 'quit':
        break
    answer = rag.ask(question)
    print(f"\n📖 Answer: {answer}")