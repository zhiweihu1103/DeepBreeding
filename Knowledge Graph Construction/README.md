# Knowledge Graph Construction

## 1. Installation

### create and activate the conda environment
```bash
conda create -n mmoe python=3.12 -y
conda activate deepbreeding_kgc
```
### install lightrag
```
pip install "lightrag-hku[api]"
```
### configure environment
- Copy `env.example` and rename it to `.env` and configure the LLM settings in `.env`:

```bash
LLM_BINDING=openai
LLM_MODEL=xxx
LLM_BINDING_HOST=xxx
LLM_BINDING_API_KEY=xxx
```

- Install the embedding model with Ollama:

```bash
ollama create bge-m3
```

- Configure the embedding settings in `.env`:

```bash
EMBEDDING_BINDING=ollama
EMBEDDING_MODEL=bge-m3:latest
EMBEDDING_DIM=1024
EMBEDDING_BINDING_HOST=http://localhost:11434
```

## 2. Build Knowledge Graph

```bash
python build_kg.py
```
