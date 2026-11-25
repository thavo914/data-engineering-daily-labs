"""Tests for Day 01: Declarative Dataclass Config Registry."""

import importlib.util
import os
from pathlib import Path

import pytest

DAY_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = "solution" if os.getenv("USE_SOLUTION") == "1" else "starter"
MODULE_PATH = DAY_DIR / TARGET_DIR / "config_registry.py"

spec = importlib.util.spec_from_file_location("day01_config_registry", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

TableConfig = mod.TableConfig
load_table_registry = mod.load_table_registry

SAMPLE_YAML = """
topic_prefix: prod_cdc
tables:
  - name: Orders
    source_database: CommerceDB
    source_schema: sales
    primary_key: ["order_id"]
    stream_source: kafka
    tier: tier1
    partition_column: business_date
    enabled: true
  - name: RoomTypes
    source_database: HotelDB
    source_schema: core
    primary_key: ["room_type_id"]
    stream_source: bronze
    tier: tier2
    enabled: true
  - name: LegacyAudit
    source_database: CommerceDB
    source_schema: dbo
    primary_key: ["audit_id"]
    tier: tier3
    enabled: false
"""


def test_computed_properties() -> None:
    cfg = TableConfig(
        name="Orders",
        source_database="CommerceDB",
        source_schema="sales",
        topic_prefix="prod_cdc",
        primary_key=["order_id"],
    )
    assert cfg.kafka_topic == "prod_cdc.CommerceDB.sales.Orders"
    assert cfg.bronze_path == "s3a://bronze/commercedb/sales/orders"
    assert cfg.silver_path == "s3a://silver/commercedb/sales/orders"


def test_validation_rejects_empty_pk() -> None:
    with pytest.raises(ValueError, match="primary_key"):
        TableConfig(
            name="BadTable",
            source_database="CommerceDB",
            source_schema="sales",
            topic_prefix="prod_cdc",
            primary_key=[],
        )


def test_validation_rejects_invalid_stream_source() -> None:
    with pytest.raises(ValueError, match="stream_source"):
        TableConfig(
            name="BadTable",
            source_database="CommerceDB",
            source_schema="sales",
            topic_prefix="prod_cdc",
            primary_key=["id"],
            stream_source="jdbc",
        )


def test_load_registry_filters_disabled_and_tiers() -> None:
    all_enabled = load_table_registry(SAMPLE_YAML)
    assert [t.name for t in all_enabled] == ["Orders", "RoomTypes"]

    tier1_only = load_table_registry(SAMPLE_YAML, tier_filter=["TIER1"])
    assert [t.name for t in tier1_only] == ["Orders"]
    assert tier1_only[0].kafka_topic == "prod_cdc.CommerceDB.sales.Orders"
