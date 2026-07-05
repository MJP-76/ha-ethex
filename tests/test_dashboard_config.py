"""Tests for custom_components.ethex.dashboard_config.

Loaded directly from file (see test_parser.py for rationale) so these tests
don't require the `homeassistant` package to be installed.
"""
import importlib.util
import sys
from pathlib import Path

COMPONENT_DIR = Path(__file__).parent.parent / "custom_components" / "ethex"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


dashboard_config = _load_module("ethex_dashboard_config", COMPONENT_DIR / "dashboard_config.py")

build_dashboard_config = dashboard_config.build_dashboard_config
DASHBOARD_TITLE = dashboard_config.DASHBOARD_TITLE


def test_overview_card_lists_non_holdings_entities_sorted():
    entities = [
        "sensor.ethex_portfolio_total",
        "sensor.ethex_ifisa_cash_balance",
        "sensor.ethex_current_investments",
        "sensor.ethex_main_account_value",
    ]
    config = build_dashboard_config(entities)

    view = config["views"][0]
    assert view["title"] == DASHBOARD_TITLE

    entities_card = next(c for c in view["cards"] if c["type"] == "entities")
    assert entities_card["entities"] == [
        "sensor.ethex_ifisa_cash_balance",
        "sensor.ethex_main_account_value",
        "sensor.ethex_portfolio_total",
    ]
    assert "sensor.ethex_current_investments" not in entities_card["entities"]


def test_holdings_card_present_when_holdings_sensor_exists():
    entities = ["sensor.ethex_portfolio_total", "sensor.ethex_current_investments"]
    config = build_dashboard_config(entities)

    view = config["views"][0]
    markdown_cards = [c for c in view["cards"] if c["type"] == "markdown"]
    assert len(markdown_cards) == 1
    assert "sensor.ethex_current_investments" in markdown_cards[0]["content"]
    assert markdown_cards[0]["title"] == "Current investments"


def test_no_holdings_card_when_no_holdings_sensor():
    entities = ["sensor.ethex_portfolio_total"]
    config = build_dashboard_config(entities)

    view = config["views"][0]
    assert not [c for c in view["cards"] if c["type"] == "markdown"]


def test_empty_entities_produces_view_with_no_cards():
    config = build_dashboard_config([])
    view = config["views"][0]
    assert view["cards"] == []
