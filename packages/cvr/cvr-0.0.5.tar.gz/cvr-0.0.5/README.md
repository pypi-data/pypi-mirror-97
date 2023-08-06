# Go API for cvr.dev

![Tests](https://github.com/cvr-dev/cvr.dev-python/actions/workflows/test.yml/badge.svg?branch=main)

The official [cvr.dev](https://cvr.dev/) Python, client library.

[cvr.dev](https://cvr.dev/) is a web service that maintains an updated cache of the Danish CVR
registry.

We aim to provide a much simpler and more modern API compared to
CVR's own Elastic Search solution.
Our focus is on high availability and robustness, making it as easy and
reliable as possible to retrieve data about Danish companies from the CVR
database.

## Installation

Make sure that you have go installed, and then run the following in your
project folder:

```bash
pip install cvr
```

## Docs

The HTTP API is available at [docs.cvr.dev](https://docs.cvr.dev/).

## Usage

In the `examples/example.py` dir there's a simple example program that verifies that
your API key works and fetches different data from the server.

```python

```

## Test

## Alternatives

Alternatives to cvr.dev include:

- [Virk's official integration](https://datacvr.virk.dk/data/cvr-hj%C3%A6lp/indgange-til-cvr/system-til-system-adgang)
- [cvrapi.dk](https://cvrapi.dk)
- [risika.dk](https://risika.dk)
- [eanapi.dk](https://eanapi.dk)
