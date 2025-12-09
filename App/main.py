from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
    You are an expert in aswering questions about a pizza restaurant

    Here are some relevent reviews: {reviews}
    
    Here is a question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


while True:
    print("\n\n------------------------------------------------------------------------------------\n ")
    question = input("Enter your question about the pizza restaurant (or 'q' to quit): ")
    print("\n\n ")
    if question.lower() == 'q':
        break
    
    reviews = retriever.invoke(question)
    results = chain.invoke({
        "reviews": reviews,
        "question": question
    })

    print(results)