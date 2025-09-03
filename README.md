# Desafio MBA Engenharia de Software com IA - Full Cycle

## Resumo

Projeto para ingestão de um PDF em um banco vetorial (Postgres + pgvector) e um fluxo de consulta que responde estritamente com base no contexto encontrado nos documentos.

## Checklist rápido

- Configurar variáveis de ambiente copiando ` .env.example` para `.env` — obrigatórios: `PDF_PATH`, `DATABASE_URL`, provedor LLM (Google ou OpenAI).
- Instalar dependências.
- Rodar `src/ingest.py` para popular o índice vetorial.
- Rodar `src/chat.py` para interagir com o sistema.

## Pré-requisitos

- Python 3.11+
- PostgreSQL com extensão `pgvector` instalada e acessível via `DATABASE_URL`.
- Credenciais válidas para o provedor de embeddings/LLM que você escolher (Google Generative AI ou OpenAI).

## Instalação

1. (Opcional) Use o virtualenv fornecido em `desafioLangChain/` ou crie um novo:

```pwsh
# Ativar virtualenv existente (se for o caso)
.\desafioLangChain\Scripts\Activate.ps1

# Ou criar/ativar um novo virtualenv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```pwsh
pip install -r requirements.txt
```

## Configuração (.env)

Copie ` .env.example` para `.env` e preencha os valores.

Principais variáveis (exemplos):

- `PDF_PATH` = caminho relativo/absoluto para o PDF a ser ingerido (ex.: `./document.pdf`).
- `DATABASE_URL` = `postgres://USER:PASS@HOST:PORT/DBNAME` (Postgres com pgvector).
- `PG_VECTOR_COLLECTION_NAME` = nome da coleção/tabela usada pelo `PGVector`.

## LLM / Embeddings

O repositório inclui suporte a duas opções (veja ` .env.example`):

- Google Generative AI: variáveis `GOOGLE_API_KEY`, `GOOGLE_EMBEDDING_MODEL`, `GOOGLE_CHAT_MODEL`.
- OpenAI (alternativa): variáveis `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL`.

Observação: o código atual (`src/search.py`) está configurado para usar Google por padrão. Para usar OpenAI, ajuste as chamadas no código ou adicione um switch que lê a variável de ambiente do provedor.

## Uso

1. Ingestão do PDF (popula o vetor DB):

```pwsh
python .\src\ingest.py
```

Comportamento:

- O script carrega o PDF apontado por `PDF_PATH`, cria chunks via `RecursiveCharacterTextSplitter`, gera embeddings e persiste documentos com `PGVector`.

2. Consultar via chat (usa o índice vetorial):

```pwsh
python .\src\chat.py
```

- Será solicitado que você digite uma pergunta; o fluxo busca documentos relevantes, monta um contexto controlado e chama o modelo de chat.

## Arquivos principais

- `src/ingest.py` : ingere e indexa o PDF no Postgres via `PGVector`.
- `src/search.py` : realiza a busca por similaridade e monta o prompt para o LLM.
- `src/chat.py` : runner simples para enviar uma pergunta e imprimir a resposta.

## Troubleshooting

- Erro: "PDF_PATH não está definido" — copie/edite `.env` e defina `PDF_PATH`.
- Erro de conexão com Postgres — verifique `DATABASE_URL`, disponibilidade do servidor e extensão `pgvector`.
- Problemas com credenciais Google/OpenAI — confirme que variáveis estão corretas e que a conta tem acesso ao(s) modelos selecionados.
