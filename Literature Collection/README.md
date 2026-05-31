# Literature Collection

`Literature Collection` 是 `DeepBreeding` 中用于农业育种文献检索与预处理的轻量模块，保留了当前稳定可用的检索、过滤、清洗、去重与统计流程，便于在项目内部继续维护和使用。

## 模块功能

- 支持 PubMed 检索
- 支持 arXiv 检索
- 支持 bioRxiv / medRxiv / chemRxiv 本地 dump 检索
- 根据作物与技术配置自动生成查询词组合
- 为命中文献补充 `retrieval_word` 标记
- 进行清洗与 DOI/标题去重
- 生成原始结果库存报告（raw inventory report）

## 不包含的内容

- 不包含 raw dumps
- 不包含 cleaned corpus
- 不包含 private datasets
- 不包含生成后的 JSONL outputs
- 不包含 virtual environment

## 环境准备

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 配置文件

- `configs/crops.yaml`：作物词表配置
- `configs/technologies.yaml`：技术词表配置
- `configs/sources.yaml`：数据源与检索相关配置
- `configs/pipeline.yaml`：清洗、输出路径等流程配置

## 运行方式

```powershell
python scripts/run_pubmed.py
python scripts/run_arxiv.py
python scripts/download_biorxiv_dump.py
python scripts/run_biorxiv_local.py
python scripts/run_cleaning.py
python scripts/run_report.py
```

- `PubMed` 和 `arXiv` 检索依赖网络。
- `xRxiv` dump 下载依赖网络以及 `paperscraper` 上游可用性。
- `bioRxiv / medRxiv / chemRxiv` 本地检索需要先准备本地 dumps。

## bioRxiv / xRxiv 相关性过滤

默认配置保留 `enable_relevance_filter: true`。这并不保证得到完全“干净”的语料，只是用于减少明显跨领域无关噪声。如果需要更粗粒度的召回，可在 `configs/sources.yaml` 中将 `enable_relevance_filter` 设置为 `false`。关闭过滤后通常会提高 recall，但也会明显增加噪声。

## 去重说明

原始结果是 query-hit records，不是唯一论文列表。同一篇论文可能同时被多个作物词、技术词或不同来源命中。清洗阶段优先使用 DOI 去重，在 DOI 缺失时回退到规范化标题。`duplicates_merged` 表示被合并的重复命中记录数，并不表示存在同等数量的“完全不同重复论文”。

## 最小校验

```powershell
python -m compileall -q src scripts
python -c "import yaml, pathlib; files=list(pathlib.Path('configs').glob('*.yaml')); [yaml.safe_load(p.read_text(encoding='utf-8')) for p in files]; print('YAML OK')"
```

## 数据使用说明

本模块运行产生的数据输出应保留在本地，不应提交 raw data、cleaned data、private data、generated JSONL 或虚拟环境文件到版本库。
