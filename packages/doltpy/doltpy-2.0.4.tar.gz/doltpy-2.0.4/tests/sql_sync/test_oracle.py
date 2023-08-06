import pytest
from .helpers.tools import validate_get_target_writer, validate_drop_primary_keys
from doltpy.sql.sync.oracle import get_target_writer


def test_write_to_table(oracle_with_table):
    engine, table = oracle_with_table
    validate_get_target_writer(engine, table, get_target_writer)


def test_drop_primary_keys(oracle_with_table):
    engine, table = oracle_with_table
    validate_drop_primary_keys(engine, table)
