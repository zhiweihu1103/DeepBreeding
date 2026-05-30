# Knowledge Graph Construction

## 1. Installation

### create and activate the conda environment
```bash
conda create -n deepbreeding_kgc python=3.12 -y
conda activate deepbreeding_kgc
```
### install lightrag
```
pip install "lightrag-hku[api]"
```
### configure environment
- copy `env.example` and rename it to `.env` and configure the LLM settings in `.env`:

```bash
LLM_BINDING=openai
LLM_MODEL=xxx
LLM_BINDING_HOST=xxx
LLM_BINDING_API_KEY=xxx
```

- install the embedding model with Ollama:

```bash
ollama create bge-m3
```

- configure the embedding settings in `.env`:

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

## 3. Parameter Description

| Parameter              | Description                                                                                                     | Example                       |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `root_work_dir`        | Directory used to store the generated knowledge graph, vector index, cache, and intermediate files.             | `"./deepbreeding_kgc"`        |
| `external_dataset_dir` | Path of the external text dataset used to build the knowledge graph. The file should usually be a `.txt` file.  | `"./input.txt"`               |
| `search_mode`          | Retrieval mode used by LightRAG. Available options include `naive`, `local`, `global`, and `hybrid`.            | `"hybrid"`                    |
| `llm_model`            | Name of the LLM used for entity extraction, relation extraction, and question answering.                        | `"gpt-4o-mini"`               |
| `llm_api_key`          | API key used to access the LLM service.                                                                         | `"sk-xxxx"`                   |
| `llm_api_url`          | Base URL of the OpenAI-compatible LLM API service.                                                              | `"https://api.openai.com/v1"` |
| `embedding_dim`        | Dimension of the embedding model. For `bge-m3`, the dimension is `1024`.                                        | `1024`                        |
| `embedding_max_token`  | Maximum token length accepted by the embedding model.                                                           | `8192`                        |
| `embedding_model_name` | Name of the embedding model served by Ollama.                                                                   | `"bge-m3:latest"`             |
| `embedding_model_url`  | Ollama service address for embedding generation.                                                                | `"http://localhost:11434"`    |

## 4. Knowledge Graph Files

| File                  | Description                                            |
| --------------------- | ------------------------------------------------------ |
| `edges_by_types.json` | Stores edges grouped by different edge types.          |
| `edges.json`          | Stores all edges without type-based classification.    |
| `nodes_by_types.json` | Stores entities grouped by different entity types.     |
| `nodes.json`          | Stores all entities without type-based classification. |
| `paper_abstracts.txt` | Stores all literature abstract information.            |

## 5. Knowledge Graph Download
- [Staple Crop Knowledge Graph](https://drive.google.com/drive/folders/1UIwu8zh8kVBqbex9yqlvsb0kLi-clsvH?usp=sharing)
- [Minor Crop Knowledge Graph](https://drive.google.com/drive/folders/1HxeVq4iLdriLdVILlQULnMaBxXjjSvhs?usp=sharing)
