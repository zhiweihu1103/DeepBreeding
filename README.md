<div align="center">
  
# 🌾 [DeepBreeding: A Knowledge-Integrated Platform for Evidence-Traceable Crop Breeding Report Generation](https://deepbreeding.com)

</div>

## Contents

- [Overview](#overview)
- [Core Modules](#core-modules)
- [Literature Collection](#literature-collection)
- [Knowledge Graph Construction](#knowledge-graph-construction)
- [Model Evaluation](#model-evaluation)
- [Quick Start](#quick-start)
- [Citation](#citation)
- [Links](#links)

## 🌱 Overview

Crop breeding knowledge is scattered across scientific literature, public databases, and long-term breeding records, limiting rapid evidence integration for gene function, regulatory mechanisms, phenotype associations, and practical breeding recommendations.

DeepBreeding addresses this challenge by organizing breeding knowledge into reusable knowledge graphs, retrieving question-relevant evidence, distilling reasoning patterns into deployable small language models, and evaluating performance with breeding-oriented benchmark tasks.

## 🧩 Core Modules

| Module | Role | Implementation |
|---|---|---|
| ⚙️ Platform Framework | Provides the base framework for implementing the DeepBreeding platform and organizing the application workflow. | [Yuxi](https://github.com/xerrors/Yuxi) |
| 📚 Literature Collection | Retrieves and curates staple crop and minor crop literatures for knowledge graph construction. | [DeepBreeding literature crawler](https://github.com/zhiweihu1103/DeepBreeding/tree/main/breeding_literature_crawler) |
| 🧬 Knowledge Graph Construction | Converts literature and breeding records into entity-relation-evidence graphs for retrieval and traceable reasoning. | [LightRAG](https://github.com/HKUDS/LightRAG) |
| 🏋️ Model Training | Distills LLM reasoning into deployable small language models through supervised fine-tuning. | [LLaMA-Factory](https://github.com/hiyouga/LlamaFactory) |
| 📊 Model Evaluation | Evaluates breeding knowledge reasoning across standardized benchmark tasks. | [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) |

## 📚 Literature Collection

The paper systematically retrieves and curates breeding-related literature from ``PubMed``, ``bioRxiv``, and other public resources. Search terms focus on ``gene expression``, ``transcription factors``, and ``breeding-relevant`` biological evidence. The retrieval scope covers publications up to **December 1, 2025**.

| Crop Group | Species | Publications |
|---|---|---:|
| staple crops | *Oryza sativa*, *Triticum aestivum*, *Zea mays* | 41,089 |
| minor crops | *Avena sativa*, *Coix lacryma-jobi*, *Fagopyrum esculentum*, *Hordeum vulgare*, *Lens culinaris*, *Pisum sativum*, *Setaria italica*, *Sorghum bicolor*, *Vigna angularis*, *Vigna radiata*, *Vigna unguiculata* | 9,829 |

## 🧬 Knowledge Graph Construction

The automated workflow includes ``document input``, ``text chunking``, ``information extraction``, ``information merging``, ``graph structuring``, and ``graph storage``.

| Knowledge Graph | Entities | Edges |
|---|---:|---:|
| staple crop knowledge graph | 84,668 | 248,244 |
| minor crop knowledge graph | 38,252 | 116,983 |

| Source Entity Type | Staple Crop Knowledge Graph Outgoing Relations Count | Minor Crop Knowledge Graph Outgoing Relations Count |
|---|---:|---:|
| Gene | 121,767 | 51,739 |
| Species | 52,856 | 26,954 |
| Biological Process | 16,187 | 9,836 |
| Phenotype | 16,900 | 4,116 |
| Environmental Factor | 18,244 | 8,398 |
| Experiment | 12,844 | 6,674 |
| Molecular Marker | 2,930 | 4,376 |
| Breeding Method | 3,701 | 4,349 |
| Agronomic Practice | 1,868 | 337 |
| Growth Stage | 947 | 204 |

## 📊 Model Evaluation

DeepBreeding uses a breeding-oriented benchmark with **10 single-choice question-answering tasks** across four knowledge categories. The evaluation compares General LLMs, Reasoning LLMs, General SLMs, and General SLMs enhanced with DeepBreeding.

| Category | Tasks |
|---|---|
| Gene-Level Feature Identification | ``Gene Structural Domains``; ``Chromosomal Localization of Genes`` |
| Regulatory Mechanism Interpretation | ``Cis-Regulatory Elements``; ``Trans-Acting Factors``; ``Functional Validation of Regulatory Elements`` |
| Gene Function and Systems-Level Validation | ``Functional Genomics``; ``Systems Genetics``; ``Gain- and Loss-of-Function Validation`` |
| Gene-Phenotype Association Reasoning | ``Association Between Homologous Genes and Phenotypes``; ``Gene Effects and Phenotypic Associations`` |

| Model Group | Description |
|---|---|
| General LLMs | General-purpose LLM baselines without crop-breeding-specific adaptation. |
| Reasoning LLMs | LLMs with explicit or enhanced reasoning mechanisms for complex problem decomposition and multi-step analysis. |
| General SLMs | Lightweight small language models without domain-specific knowledge construction, retrieval, or distillation. |
| General SLMs + DeepBreeding | Small language models enhanced with the crop breeding knowledge graph, knowledge retrieval, and knowledge distillation. |

## 🚀 Quick Start

### 1. 📚 Literature Collection

For details, please refer to the corresponding subfolder in this repository: [`Literature Collection/`](./Literature Collection/).

### 2. 🧬 Knowledge Graph Construction

```bash
git clone https://github.com/HKUDS/LightRAG.git
```

### 3. 🏋️ Model Training

```bash
git clone https://github.com/hiyouga/LlamaFactory.git
```

### 4. 📊 Model Evaluation

```bash
git clone https://github.com/EleutherAI/lm-evaluation-harness.git
```

## 📝 Citation

If you use DeepBreeding, please cite:

```bibtex
@article{hu2026deepbreeding,
  title   = {DeepBreeding: A Knowledge-Integrated Platform for Evidence-Traceable Crop Breeding Report Generation},
  year    = {2026}
}
```

## 🔗 Links

- 🌐 [DeepBreeding Platform](https://deepbreeding.com) 
- ⚙️ [Platform Framework](https://github.com/xerrors/Yuxi) 
- 📚 [Literature Collection](https://github.com/zhiweihu1103/DeepBreeding/tree/main/breeding_literature_crawler)
- 🧬 [Knowledge Graph Construction](https://github.com/HKUDS/LightRAG)
- 🏋️ [Model Training](https://github.com/hiyouga/LlamaFactory)
- 📊 [Model Evaluation](https://github.com/EleutherAI/lm-evaluation-harness)
