# Home Assistant - Ethex Investment Platform Integration

<a href="https://www.home-assistant.io/" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/Home%20Assistant-41BDF5?style=flat-square&logo=homeassistant&logoColor=white" alt="Home Assistant"></a>
<a href="https://github.com/hacs/integration" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
[![hassfest](https://github.com/MJP-76/ha-ethex/actions/workflows/hassfest.yml/badge.svg)](https://github.com/MJP-76/ha-ethex/actions/workflows/hassfest.yml)
<a href="https://github.com/MJP-76/KirkHillWindFarm/actions/workflows/validate.yml" target="_blank" rel="noopener noreferrer"><img src="https://github.com/MJP-76/KirkHillWindFarm/actions/workflows/validate.yml/badge.svg" alt="HACS Validation"></a>
<a href="https://github.com/MJP-76/KirkHillWindFarm/actions/workflows/ci.yml" target="_blank" rel="noopener noreferrer"><img src="https://github.com/MJP-76/KirkHillWindFarm/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
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
Under active development.

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
