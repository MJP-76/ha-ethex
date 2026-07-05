"""Tests for custom_components.ethex.parser.

`parser.py` and `const.py` are loaded directly from file (rather than via
`from custom_components.ethex import ...`) so these tests don't require the
`homeassistant` package to be installed just to satisfy the imports in the
component's `__init__.py` while importing the package chain.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

COMPONENT_DIR = Path(__file__).parent.parent / "custom_components" / "ethex"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


const = _load_module("ethex_const", COMPONENT_DIR / "const.py")
parser = _load_module("ethex_parser", COMPONENT_DIR / "parser.py")

HOLDING_TABS = const.HOLDING_TABS
parse_account_detail = parser.parse_account_detail
parse_holdings = parser.parse_holdings
parse_summary = parser.parse_summary


def _load(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


@pytest.fixture
def empty_html() -> str:
    return _load("portfolio_empty.html")


@pytest.fixture
def populated_html() -> str:
    return _load("portfolio_populated.html")


class TestParseSummaryEmpty:
    def test_summary_values(self, empty_html: str) -> None:
        summary = parse_summary(empty_html)
        assert summary.main_account_value == 0.0
        assert summary.ifisa_account_value == 0.0
        assert summary.portfolio_total == 0.0


class TestParseSummaryPopulated:
    def test_summary_values(self, populated_html: str) -> None:
        summary = parse_summary(populated_html)
        assert summary.main_account_value == 1250.50
        assert summary.ifisa_account_value == 500.00
        assert summary.portfolio_total == 1750.50


class TestParseAccountDetailEmpty:
    def test_detail_values(self, empty_html: str) -> None:
        detail = parse_account_detail(empty_html)
        assert detail.total == 0.0
        assert detail.invested == 0.0
        assert detail.cash_balance == 0.0


class TestParseAccountDetailPopulated:
    def test_detail_values(self, populated_html: str) -> None:
        detail = parse_account_detail(populated_html)
        assert detail.total == 1250.50
        assert detail.invested == 1000.00
        assert detail.cash_balance == 250.50


class TestParseHoldingsEmpty:
    def test_no_holdings(self, empty_html: str) -> None:
        holdings = parse_holdings(empty_html, HOLDING_TABS)
        assert holdings == []


class TestParseHoldingsPopulated:
    def test_current_holdings(self, populated_html: str) -> None:
        holdings = parse_holdings(populated_html, HOLDING_TABS)
        current = [h for h in holdings if h.status == "current"]
        assert len(current) == 2
        assert current[0].name == "Green Windfarm Bond"
        assert current[0].fields["Original Investment"] == "£500.00"
        assert current[0].fields["Current Investment"] == "£500.00"
        assert current[0].fields["Order status"] == "Active"
        assert current[1].name == "Solar Community Bond"

    def test_other_tabs_still_empty(self, populated_html: str) -> None:
        holdings = parse_holdings(populated_html, HOLDING_TABS)
        assert [h for h in holdings if h.status == "repaid"] == []
        assert [h for h in holdings if h.status == "cancelled_or_refunded"] == []
