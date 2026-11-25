"""Day 01 Solution: Declarative Dataclass Config Registry."""

from dataclasses import dataclass
from typing import List, Optional

import yaml

VALID_STREAM_SOURCES = {"kafka", "bronze"}
VALID_TIERS = {"tier1", "tier2", "tier3"}


@dataclass
class TableConfig:
    name: str
    source_database: str
    source_schema: str
    topic_prefix: str
    primary_key: List[str]
    stream_source: str = "kafka"
    tier: str = "tier2"
    enabled: bool = True
    partition_column: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.primary_key:
            raise ValueError(f"Table '{self.name}' must define at least one primary_key column.")
        if self.stream_source not in VALID_STREAM_SOURCES:
            raise ValueError(
                f"Table '{self.name}' has invalid stream_source '{self.stream_source}'. "
                f"Expected one of {sorted(VALID_STREAM_SOURCES)}."
            )
        self.tier = self.tier.lower()
        if self.tier not in VALID_TIERS:
            raise ValueError(
                f"Table '{self.name}' has invalid tier '{self.tier}'. Expected one of {sorted(VALID_TIERS)}."
            )

    @property
    def kafka_topic(self) -> str:
        return f"{self.topic_prefix}.{self.source_database}.{self.source_schema}.{self.name}"

    @property
    def bronze_path(self) -> str:
        return f"s3a://bronze/{self.source_database.lower()}/{self.source_schema.lower()}/{self.name.lower()}"

    @property
    def silver_path(self) -> str:
        return f"s3a://silver/{self.source_database.lower()}/{self.source_schema.lower()}/{self.name.lower()}"


def load_table_registry(
    yaml_content: str,
    tier_filter: Optional[List[str]] = None,
) -> List[TableConfig]:
    """Parse YAML pipeline config into validated, enabled TableConfig instances."""
    raw = yaml.safe_load(yaml_content) or {}
    default_prefix = raw.get("topic_prefix", "cdc")
    tables_raw = raw.get("tables", [])

    allowed_tiers = {t.strip().lower() for t in tier_filter} if tier_filter else None

    registry: List[TableConfig] = []
    for item in tables_raw:
        if not item.get("enabled", True):
            continue
        cfg = TableConfig(
            name=item["name"],
            source_database=item["source_database"],
            source_schema=item["source_schema"],
            topic_prefix=item.get("topic_prefix", default_prefix),
            primary_key=item.get("primary_key", []),
            stream_source=item.get("stream_source", "kafka"),
            tier=item.get("tier", "tier2"),
            enabled=True,
            partition_column=item.get("partition_column"),
        )
        if allowed_tiers is not None and cfg.tier not in allowed_tiers:
            continue
        registry.append(cfg)

    return registry
