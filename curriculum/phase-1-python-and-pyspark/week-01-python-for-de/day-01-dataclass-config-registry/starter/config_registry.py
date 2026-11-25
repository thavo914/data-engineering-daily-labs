"""Day 01 Starter: Declarative Dataclass Config Registry."""

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
        # TODO: Validate primary_key (non-empty), stream_source, and tier.
        # Raise ValueError with a descriptive message on invalid input.
        raise NotImplementedError("Implement __post_init__ validation")

    @property
    def kafka_topic(self) -> str:
        # TODO: Return "{topic_prefix}.{source_database}.{source_schema}.{name}"
        raise NotImplementedError("Implement kafka_topic property")

    @property
    def bronze_path(self) -> str:
        # TODO: Return "s3a://bronze/{db}/{schema}/{name}" in lowercase
        raise NotImplementedError("Implement bronze_path property")

    @property
    def silver_path(self) -> str:
        # TODO: Return "s3a://silver/{db}/{schema}/{name}" in lowercase
        raise NotImplementedError("Implement silver_path property")


def load_table_registry(
    yaml_content: str,
    tier_filter: Optional[List[str]] = None,
) -> List[TableConfig]:
    """Parse YAML pipeline config into validated, enabled TableConfig instances."""
    _ = yaml  # Keep import used for starter
    # TODO:
    # 1. Parse yaml_content using yaml.safe_load
    # 2. Read defaults (topic_prefix) and tables list
    # 3. Filter out tables where enabled is False
    # 4. Construct TableConfig for each enabled table
    # 5. If tier_filter is provided, filter case-insensitively by tier
    raise NotImplementedError("Implement load_table_registry")
