"""Configuration loading utilities for the pipeline."""

from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "configs"


def load_yaml(filename: str) -> dict:
    """Load one YAML configuration file from `configs/`."""

    path = CONFIG_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_all_configs() -> dict:
    """Load the four configuration files used by the main workflow."""

    crops_cfg = load_yaml("crops.yaml")
    tech_cfg = load_yaml("technologies.yaml")
    sources_cfg = load_yaml("sources.yaml")
    pipeline_cfg = load_yaml("pipeline.yaml")
    return {
        "crops": crops_cfg,
        "technologies": tech_cfg,
        "sources": sources_cfg,
        "pipeline": pipeline_cfg,
    }


def get_all_crops(cfg: dict) -> list[str]:
    """Return the crop list used by the main retrieval workflow."""

    crops = cfg["crops"]["crops"]
    return crops["staple"] + crops["minor"]


def get_technologies(cfg: dict) -> list[str]:
    """Return the breeding technology keywords used by the main workflow."""

    return cfg["technologies"]["technologies"]["breeding_core"]
