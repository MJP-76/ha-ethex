# Home Assistant - Ethex Integration

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

## Development

```bash
pip install -r requirements_test.txt
pytest -v
```
