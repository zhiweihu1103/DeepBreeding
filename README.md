<div align="center">
  
# 🌾 [DeepBreeding: A Knowledge-Integrated Platform for Evidence-Traceable Crop Breeding Report Generation](https://deepbreeding.com)

</div>

## Contents

- [Overview](#overview)
- [Core Modules](#core-modules)
- [Literature Collection](#literature-collection)
- [Knowledge Graph Construction](#knowledge-graph-construction)
- [Model Training](#model-training)
- [Model Evaluation](#model-evaluation)
- [Repository Map](#repository-map)
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

---

## 📚 Literature Collection

The paper systematically retrieves and curates breeding-related literature from PubMed, bioRxiv, and other public resources. Search terms focus on gene expression, transcription factors, and breeding-relevant biological evidence. The retrieval scope covers publications up to **December 1, 2025**.

| Crop group | Species | Publications |
|---|---|---:|
| Staple crops | *Oryza sativa*, *Triticum aestivum*, *Zea mays* | 41,089 |
| Minor cereals and related crops | *Avena sativa*, *Coix lacryma-jobi*, *Fagopyrum esculentum*, *Hordeum vulgare*, *Lens culinaris*, *Pisum sativum*, *Setaria italica*, *Sorghum bicolor*, *Vigna angularis*, *Vigna radiata*, *Vigna unguiculata* | 9,829 |

Code for literature retrieval:

```text
https://github.com/zhiweihu1103/DeepBreeding/tree/main/breeding_literature_crawler
```

---

## 🧬 Knowledge Graph Construction

DeepBreeding uses a two-stage strategy integrating automated construction and proportional manual validation. The automated workflow includes document input, text chunking, information extraction, information merging, graph structuring, and graph storage. The paper describes extraction of genetic, phenotypic, regulatory, environmental, methodological, and experimental knowledge units. Entities, relations, and evidence descriptions are retained for downstream retrieval and traceable reasoning.

| Knowledge graph | Entities | Edges |
|---|---:|---:|
| Staple crop knowledge graph | 84,668 | 248,244 |
| Minor cereal knowledge graph | 38,252 | 116,983 |

Quality control samples 5% of entities and edges across entity and relation types to inspect entity boundaries, categories, relation semantics, and evidence consistency.

### Entity-Type Relation Counts

The following statistics are aggregated from `Supplemental Tables.xlsx`. Counts represent outgoing relations grouped by source entity type.

| Source entity type | Staple crop KG outgoing relations | Minor cereal KG outgoing relations |
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

### Staple Crop KG Relation Counts by Source Type

| Source entity type | Total outgoing relations | Target relation counts |
|---|---:|---|
| Gene | 121,767 | Gene: 78,691; Species: 10,190; Biological Process: 11,201; Phenotype: 7,422; Environmental Factor: 4,943; Experiment: 6,028; Molecular Marker: 1,619; Breeding Method: 1,017; Growth Stage: 656 |
| Species | 52,856 | Gene: 29,444; Species: 8,888; Biological Process: 2,502; Phenotype: 3,144; Environmental Factor: 3,528; Experiment: 3,021; Molecular Marker: 734; Breeding Method: 635; Agronomic Practice: 786; Growth Stage: 174 |
| Biological Process | 16,187 | Gene: 10,175; Species: 1,290; Biological Process: 2,005; Phenotype: 700; Environmental Factor: 787; Experiment: 842; Molecular Marker: 140; Breeding Method: 133; Agronomic Practice: 115 |
| Phenotype | 16,900 | Gene: 9,564; Species: 1,862; Biological Process: 905; Phenotype: 1,970; Environmental Factor: 909; Experiment: 1,255; Molecular Marker: 325; Growth Stage: 110 |
| Environmental Factor | 18,244 | Gene: 10,167; Species: 2,316; Biological Process: 1,216; Phenotype: 1,487; Environmental Factor: 1,746; Experiment: 648; Molecular Marker: 157; Agronomic Practice: 382; Growth Stage: 125 |
| Experiment | 12,844 | Gene: 5,743; Species: 1,273; Biological Process: 1,013; Phenotype: 1,076; Environmental Factor: 388; Experiment: 2,556; Molecular Marker: 483; Breeding Method: 128; Growth Stage: 184 |
| Molecular Marker | 2,930 | Gene: 1,597; Species: 320; Biological Process: 104; Phenotype: 307; Environmental Factor: 47; Molecular Marker: 457; Breeding Method: 86; Agronomic Practice: 8; Growth Stage: 4 |
| Breeding Method | 3,701 | Gene: 2,219; Biological Process: 117; Phenotype: 233; Environmental Factor: 49; Experiment: 198; Molecular Marker: 163; Breeding Method: 659; Agronomic Practice: 21; Growth Stage: 42 |
| Agronomic Practice | 1,868 | Gene: 579; Species: 300; Biological Process: 164; Phenotype: 319; Environmental Factor: 236; Experiment: 97; Molecular Marker: 10; Breeding Method: 22; Agronomic Practice: 125; Growth Stage: 16 |
| Growth Stage | 947 | Species: 463; Biological Process: 74; Phenotype: 97; Environmental Factor: 62; Experiment: 8; Molecular Marker: 86; Breeding Method: 149; Agronomic Practice: 8 |

### Minor Cereal KG Relation Counts by Source Type

| Source entity type | Total outgoing relations | Target relation counts |
|---|---:|---|
| Gene | 51,739 | Gene: 29,539; Species: 4,830; Biological Process: 5,581; Phenotype: 1,956; Environmental Factor: 2,350; Experiment: 3,196; Molecular Marker: 2,242; Breeding Method: 1,731; Agronomic Practice: 114; Growth Stage: 200 |
| Species | 26,954 | Gene: 13,017; Species: 4,845; Biological Process: 1,676; Phenotype: 997; Environmental Factor: 2,028; Experiment: 1,819; Molecular Marker: 1,084; Breeding Method: 1,238; Agronomic Practice: 191; Growth Stage: 59 |
| Biological Process | 9,836 | Gene: 5,239; Species: 889; Biological Process: 1,706; Phenotype: 394; Environmental Factor: 439; Experiment: 411; Molecular Marker: 325; Breeding Method: 311; Agronomic Practice: 55; Growth Stage: 67 |
| Phenotype | 4,116 | Gene: 1,850; Species: 478; Biological Process: 355; Phenotype: 544; Environmental Factor: 170; Experiment: 256; Molecular Marker: 223; Breeding Method: 156; Agronomic Practice: 72; Growth Stage: 12 |
| Environmental Factor | 8,398 | Gene: 4,169; Species: 1,434; Biological Process: 702; Phenotype: 426; Environmental Factor: 846; Experiment: 282; Molecular Marker: 239; Breeding Method: 208; Agronomic Practice: 64; Growth Stage: 28 |
| Experiment | 6,674 | Gene: 3,063; Species: 787; Biological Process: 460; Phenotype: 227; Environmental Factor: 211; Experiment: 1,168; Molecular Marker: 354; Breeding Method: 338; Agronomic Practice: 22; Growth Stage: 44 |
| Molecular Marker | 4,376 | Gene: 1,884; Species: 472; Biological Process: 350; Phenotype: 251; Environmental Factor: 144; Experiment: 347; Molecular Marker: 713; Breeding Method: 183; Agronomic Practice: 20; Growth Stage: 12 |
| Breeding Method | 4,349 | Gene: 1,899; Species: 576; Biological Process: 329; Phenotype: 145; Environmental Factor: 125; Experiment: 411; Molecular Marker: 335; Breeding Method: 491; Agronomic Practice: 19; Growth Stage: 19 |
| Agronomic Practice | 337 | Gene: 68; Species: 60; Biological Process: 46; Phenotype: 74; Environmental Factor: 13; Experiment: 30; Molecular Marker: 12; Breeding Method: 10; Agronomic Practice: 24; Growth Stage: 0 |
| Growth Stage | 204 | Gene: 100; Species: 16; Biological Process: 33; Phenotype: 12; Environmental Factor: 8; Experiment: 8; Molecular Marker: 7; Breeding Method: 4; Growth Stage: 16 |

---

## 🏋️ Model Training

DeepBreeding trains small language models through knowledge distillation and instruction tuning. GPT-5.2 is used in the paper to generate structured training samples containing a task instruction, breeding question, retrieved evidence, reasoning process, and reference answer. Training is performed with [LLaMA-Factory](https://github.com/hiyouga/LlamaFactory) using LoRA.

| Setting | Value |
|---|---|
| Adaptation method | LoRA |
| Target modules | all linear modules |
| LoRA rank / alpha / dropout | 8 / 16 / 0 |
| Learning rate | 1.0e-4 |
| Epochs | 3 |
| Scheduler | cosine |
| Warm-up ratio | 0.1 |
| Precision | bfloat16 |

---

## 📊 Model Evaluation

DeepBreeding uses a breeding-oriented benchmark with **10 single-choice question-answering tasks** across four knowledge categories. The evaluation compares General LLMs, Reasoning LLMs, General SLMs, and General SLMs enhanced with DeepBreeding.

| Category | Tasks |
|---|---|
| Gene-Level Feature Identification | Gene Structural Domains; Chromosomal Localization of Genes |
| Regulatory Mechanism Interpretation | Cis-Regulatory Elements; Trans-Acting Factors; Functional Validation of Regulatory Elements |
| Gene Function and Systems-Level Validation | Functional Genomics; Systems Genetics; Gain- and Loss-of-Function Validation |
| Gene-Phenotype Association Reasoning | Association Between Homologous Genes and Phenotypes; Gene Effects and Phenotypic Associations |

| Model group | Description |
|---|---|
| General LLMs | General-purpose LLM baselines without crop-breeding-specific adaptation. |
| Reasoning LLMs | LLMs with explicit or enhanced reasoning mechanisms for complex problem decomposition and multi-step analysis. |
| General SLMs | Lightweight small language models without domain-specific knowledge construction, retrieval, or distillation. |
| General SLMs + DeepBreeding | Small language models enhanced with the crop breeding knowledge graph, knowledge retrieval, and knowledge distillation. |

---

## 🗂️ Repository Map

```text
DeepBreeding/
├── breeding_literature_crawler/      # Literature retrieval for KG construction
├── knowledge_graph/                  # LightRAG-based KG construction workflow
├── training/                         # LLaMA-Factory configs and training scripts
├── evaluation/                       # lm-evaluation-harness tasks and evaluation scripts
├── data/                             # KG data, benchmark data, and source data links
└── README.md
```

---

## 🚀 Quick Start

### 1. ⚙️ Platform Framework

```bash
git clone https://github.com/xerrors/Yuxi.git
```

Use Yuxi as the base framework for implementing and organizing the DeepBreeding platform.

### 2. 📚 Collect Literature

```bash
git clone https://github.com/zhiweihu1103/DeepBreeding.git
cd DeepBreeding/breeding_literature_crawler
```

Use the crawler-specific instructions to reproduce literature retrieval and abstract collection.

### 3. 🧬 Build the Knowledge Graph

```bash
git clone https://github.com/HKUDS/LightRAG.git
```

Use curated literature abstracts and breeding records as source documents, then run the LightRAG-based workflow for chunking, extraction, merging, graph structuring, and storage.

### 4. 🏋️ Train DeepBreeding Models

```bash
git clone https://github.com/hiyouga/LlamaFactory.git
```

Prepare instruction-tuning samples with retrieved evidence and reference answers, then run LoRA-based supervised fine-tuning using the hyperparameters reported above.

### 5. 📊 Evaluate Models

```bash
git clone https://github.com/EleutherAI/lm-evaluation-harness.git
```

Register the 10 DeepBreeding benchmark tasks, run inference over candidate models, and compute accuracy with unified task instructions and answer-matching rules.

---

## 📝 Citation

If you use DeepBreeding, please cite:

```bibtex
@article{hu2026deepbreeding,
  title   = {DeepBreeding: A Knowledge-Integrated Platform for Evidence-Traceable Crop Breeding Report Generation},
  author  = {Hu, Zhiwei and Yang, Yi and Guti\\'errez Basulto, V\\'ictor and Deng, Yuanpei and Yang, Senjie and Yan, Zhichao and Li, Ru and Xie, Qianqian and Pan, Jeff Z. and Gao, Jianhua and Kong, Zhaosheng},
  year    = {2026},
  note    = {Manuscript}
}
```

---

## 🔗 Links

- 🌐 Platform: https://deepbreeding.com
- ⚙️ Platform framework: https://github.com/xerrors/Yuxi
- 📚 Literature crawler: https://github.com/zhiweihu1103/DeepBreeding/tree/main/breeding_literature_crawler
- 🧬 LightRAG: https://github.com/HKUDS/LightRAG
- 🏋️ LLaMA-Factory: https://github.com/hiyouga/LlamaFactory
- 📊 lm-evaluation-harness: https://github.com/EleutherAI/lm-evaluation-harness
