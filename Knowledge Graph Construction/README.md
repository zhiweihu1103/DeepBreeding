# Knowledge Graph Construction

This repository provides a simple example for building a knowledge graph with [LightRAG](https://github.com/HKUDS/LightRAG), using an OpenAI-compatible LLM API and Ollama-based `bge-m3` embeddings.

## 1. Environment

Activate the conda environment:

```bash
conda create -n mmoe python=3.7 -y
conda activate lightrag
```

## 2. Installation

Download the LightRAG source code:

```bash
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
```

Install LightRAG with API support:

```bash
pip install "lightrag-hku[api]"
```

Copy `env.example` and rename it to `.env`:

```bash
cp env.example .env
```

Configure the LLM settings in `.env`:

```bash
LLM_BINDING=openai
LLM_MODEL=xxx
LLM_BINDING_HOST=xxx
LLM_BINDING_API_KEY=xxx
```

Install the embedding model with Ollama:

```bash
ollama create bge-m3
```

Configure the embedding settings in `.env`:

```bash
EMBEDDING_BINDING=ollama
EMBEDDING_MODEL=bge-m3:latest
EMBEDDING_DIM=1024
EMBEDDING_BINDING_HOST=http://localhost:11434
```

## 3. Build Knowledge Graph

Create a Python script, for example `build_kg.py`:

```python
import os
import asyncio

from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache
from lightrag.llm.ollama import ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status

root_work_dir = "xxx"
external_dataset_dir = "xxx"
search_mode = "hybrid"  # naive, local, global, hybrid

# LLM settings
llm_model = "xxx"
llm_api_key = "xxx"
llm_api_url = "xxx"

# Embedding settings
embedding_dim = 1024
embedding_max_token = 8192
embedding_model_name = "bge-m3:latest"
embedding_model_url = "http://localhost:11434"


async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs) -> str:
    return await openai_complete_if_cache(
        llm_model,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=llm_api_key,
        base_url=llm_api_url,
        **kwargs,
    )


async def initialize_rag():
    rag = LightRAG(
        working_dir=root_work_dir,
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=embedding_dim,
            max_token_size=embedding_max_token,
            func=lambda texts: ollama_embed(
                texts,
                embed_model=embedding_model_name,
                host=embedding_model_url,
            ),
        ),
        embedding_batch_num=64,
        embedding_func_max_async=8,
        llm_model_max_async=16,
        chunk_token_size=4096,
        chunk_overlap_token_size=50,
        entity_extract_max_gleaning=1,
        embedding_cache_config={
            "enabled": True,
            "similarity_threshold": 0.90,
            "use_llm_check": False,
        },
    )

    await rag.initialize_storages()
    return rag


async def main():
    rag = None

    try:
        rag = await initialize_rag()
        await initialize_pipeline_status()

        with open(external_dataset_dir, "r", encoding="utf-8") as f:
            await rag.ainsert(f.read())

        query_param = QueryParam(
            mode=search_mode,
            user_prompt="Answer the following question only by providing the letter corresponding to the right option only.",
        )

        resp = await rag.aquery(
            '"question": "The ESP cis-element discovered in Avena sativa within the 960 bp promoter upstream region of AsGlo1 has the sequence ACATGTCATCATGT. What role does it most likely play in gene expression?", "options": {"A": "1. endosperm; 2. seed storage protein;", "B": "1. sucrose signaling; 2. starch metabolism;", "C": "1. ABA; 2. drought; 3. salt;", "D": "1. dehydration; 2. salt; 3. cold;"}',
            param=query_param,
        )

        print(resp)

    except Exception as e:
        print(e)

    finally:
        if rag:
            await rag.finalize_storages()


if __name__ == "__main__":
    if not os.path.exists(root_work_dir):
        os.mkdir(root_work_dir)

    asyncio.run(main())
    print("\nDone!")
```

## 4. Run

```bash
python build_kg.py
```
