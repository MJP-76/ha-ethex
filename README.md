# Home Assistant - Ethex Investment Platform Integration

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-41BDF5?style=flat-square&logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![hassfest](https://github.com/MJP-76/ha-ethex/actions/workflows/hassfest.yml/badge.svg)](https://github.com/MJP-76/ha-ethex/actions/workflows/hassfest.yml)
[![HACS Validation](https://github.com/MJP-76/ha-ethex/actions/workflows/hacs.yml/badge.svg)](https://github.com/MJP-76/ha-ethex/actions/workflows/hacs.yml)
[![CI](https://github.com/MJP-76/ha-ethex/actions/workflows/ci.yml/badge.svg)](https://github.com/MJP-76/ha-ethex/actions/workflows/ci.yml)
[![Built with GitHub Copilot](https://img.shields.io/badge/Built%20with-GitHub%20Copilot-8A2BE2.svg)](https://github.com/features/copilot)

Custom component for Home Assistant that logs into [Ethex](https://www.ethex.org.uk/) using your
username/email and password, and exposes your investment portfolio data as sensors.

This integration works by scraping the authenticated `/investor/portfolios` page since Ethex
does not offer a public API.

## Origin

This project came about from the need to track earnings from a Kirk Hill wind farm investment
in Home Assistant. It's designed to complement
[mjp-76/kirkhillwindfarm](https://github.com/mjp-76/kirkhillwindfarm), which tracks the wind
farm's generation/output data.

## Status
Stable release available (see [Releases](https://github.com/MJP-76/ha-ethex/releases)).

## Installation

### HACS (recommended)

1. In HACS, add this repository as a custom repository (category: Integration):
   `https://github.com/MJP-76/ha-ethex`
2. Search for "Ethex Investment Platform" in HACS and install it.
3. Restart Home Assistant.
4. Go to **Settings > Devices & Services > Add Integration**, search for
   "Ethex Investment Platform", and enter your Ethex credentials.

### Manual

1. Copy `custom_components/ethex` into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings > Devices & Services > Add Integration**, search for
   "Ethex Investment Platform", and enter your Ethex credentials.

## What it does

The integration logs into your Ethex account and scrapes `/investor/portfolios`
to expose the following sensors:

- **Portfolio total** — grand total across all accounts
- **Main account value**, **IFISA account value** — top-level balances
- **Main account invested**, **Main account cash balance**
- **IFISA invested**, **IFISA cash balance**
- **Current investments** — count of active holdings, with the full list of
  current/repaid/cancelled holdings as an attribute

## Notes on holdings parsing

The account used to build this integration had £0.00 balances and no
holdings, so the exact markup for a *populated* investments table could not
be captured. The holdings parser (`parser.py`) is written generically
(reading each table cell's `data-title` attribute as a key/value pair) so it
should be resilient to this, but the populated-row structure is inferred and
unverified. If your sensors don't pick up holdings correctly, please open an
issue with an example of the (anonymized) table markup.

## Dashboard

During setup, the config flow asks whether Home Assistant should
automatically create an **"Ethex Investment Platform"** Lovelace dashboard,
pre-populated with all of the sensors above (an overview card, plus a
markdown card listing current holdings). This is enabled by default, but can
be turned off at that step if you'd rather build your own dashboard by hand.
The preference can be changed later from the integration's **Configure**
options.

Note: dashboard auto-creation relies on Home Assistant's internal Lovelace
storage layout rather than a public integration API (Home Assistant doesn't
expose one), so it's best-effort — if it ever fails on a given HA version,
integration setup still completes normally and you can create the dashboard
yourself via Settings > Dashboards.

## Development

```bash
pip install -r requirements_test.txt
pytest -v
```
