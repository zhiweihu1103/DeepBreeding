"""Source layer entry points for literature retrieval backends."""

from agri_lit_pipeline.sources.pubmed import crawl_pubmed_pairs

__all__ = ["crawl_pubmed_pairs"]

