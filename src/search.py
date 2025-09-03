from langchain_core.runnables import RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
import os
from dotenv import load_dotenv
load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

#@tool("contexto")
def contexto(question_prompt: dict) -> dict:
    """Busca documentos relevantes no banco de dados vetorial."""
    question = question_prompt.get("pergunta")
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    
    pgvector = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    busca = pgvector.similarity_search_with_score(question, k=10)

    if not busca:
        return "Não foram encontrados documentos relevantes."

    resultados = "\n\n".join([f"Resultado {i} (Score: {score}):\n{doc.page_content}\nMetadata: {doc.metadata}" for i, (doc, score) in enumerate(busca, start=1)])

    return {"contexto": resultados, "pergunta": question}

def search_prompt(question=None):
    
    if not question:
        print("A pergunta do usuário não foi fornecida.")
        return None

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", disable_streaming=True)

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    contexto_runnable = RunnableLambda(contexto)

    chain = contexto_runnable | prompt | llm
    return chain.invoke({"pergunta": question})
