import os
from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.dataset_schema import SingleTurnSample, EvaluationDataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from rag.chain import get_rag_chain
from evaluation.eval_dataset import EVAL_DATASET

load_dotenv()

def run_evaluation():
    print("Loading RAG chain...")
    chain = get_rag_chain()
    history = InMemoryChatMessageHistory()

    samples = []

    print(f"Running {len(EVAL_DATASET)} evaluation queries...")
    for i, item in enumerate(EVAL_DATASET):
        print(f"  [{i+1}/{len(EVAL_DATASET)}] {item['question'][:60]}...")
        result = chain.invoke({
            "question": item["question"],
            "chat_history": history.messages,
        })

        answer = result["answer"]
        source_docs = result.get("source_documents", [])
        contexts = [doc.page_content for doc in source_docs]

        sample = SingleTurnSample(
            user_input=item["question"],
            response=answer,
            retrieved_contexts=contexts,
            reference=item["ground_truth"],
        )
        samples.append(sample)

    dataset = EvaluationDataset(samples=samples)

    print("\nRunning RAGAS evaluation...")
    llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini", temperature=0))
    embeddings = LangchainEmbeddingsWrapper(
        OpenAIEmbeddings(model="text-embedding-3-small")
    )

    results = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=llm,
        embeddings=embeddings,
    )

    print("\n=== RAGAS Evaluation Results ===")
    print(results)

    df = results.to_pandas()
    print("\nPer-question breakdown:")
    print(df[["user_input", "faithfulness", "answer_relevancy",
              "context_precision", "context_recall"]].to_string())

    # Save to CSV
    df.to_csv("evaluation/ragas_results.csv", index=False)
    print("\nResults saved to evaluation/ragas_results.csv")

        # Save aggregated results to PostgreSQL
    from sqlalchemy import create_engine, text
    import numpy as np
    db_url = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}"
        f"/{os.getenv('POSTGRES_DB')}"
    )
    engine = create_engine(db_url)
    df = results.to_pandas()
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS eval_results (
                id SERIAL PRIMARY KEY,
                metric VARCHAR(100),
                value FLOAT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        for metric in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
            value = float(df[metric].mean())
            conn.execute(
                text("INSERT INTO eval_results (metric, value) VALUES (:metric, :value)"),
                {"metric": metric, "value": value},
            )
    print("Evaluation results saved to PostgreSQL")

    return results

if __name__ == "__main__":
    run_evaluation()