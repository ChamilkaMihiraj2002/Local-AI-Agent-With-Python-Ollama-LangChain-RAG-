from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Import the retriever we created in vector.py
from vector import retriever

def main():
    if not retriever:
        print("System could not start. Check vector.py logs.")
        return

    # 1. Setup LLM
    model = OllamaLLM(model="llama3.2")

    # 2. Setup Generic Prompt
    # We replaced specific references to "pizza" or "reviews" with "Context"
    template = """
    You are a helpful assistant. Use the provided context to answer the question.
    If the answer is not in the context, simply say you don't know.
    
    Context:
    {context}
    
    Question: {question}
    """
    
    prompt = ChatPromptTemplate.from_template(template)

    # 3. Build Chain
    # Helper function to join retrieved documents into a single string
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    # 4. Chat Loop
    print("\n--- RAG System Ready ---")
    print("Ask questions about the files in your 'data' folder.")
    
    while True:
        print("\n---------------------------------------------------------")
        question = input("Enter your question (or 'q' to quit): ")
        
        if question.lower() == 'q':
            print("Exiting...")
            break
        
        print("\nThinking...")
        try:
            response = chain.invoke(question)
            print("\nResponse:")
            print(response)
        except Exception as e:
            print(f"Error processing request: {e}")

if __name__ == "__main__":
    main()