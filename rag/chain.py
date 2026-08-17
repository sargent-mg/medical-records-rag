import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import PromptTemplate
from rag.retriever import get_ensemble_retriever

load_dotenv()

SYSTEM_PROMPT = """You are a medical assistant helping clinicians query patient records.
You have access to synthetic patient data including conditions, medications,
allergies, lab results, and encounter history.

Use the retrieved context to answer questions accurately and concisely.
If the information is not in the context, say so clearly — do not hallucinate.
Always maintain patient confidentiality and professional medical tone.

Context:
{context}

Chat History:
{chat_history}

Question: {question}
Answer:"""

store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def get_rag_chain() -> ConversationalRetrievalChain:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    retriever = get_ensemble_retriever(k=5)

    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=SYSTEM_PROMPT,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
        output_key="answer",
    )

    return chain

if __name__ == "__main__":
    chain = get_rag_chain()
    history = InMemoryChatMessageHistory()
    result = chain.invoke({
        "question": "What patients have diabetes?",
        "chat_history": history.messages,
    })
    print(result["answer"])
    print("\n--- Sources ---")
    for doc in result["source_documents"]:
        print(doc.page_content[:100])