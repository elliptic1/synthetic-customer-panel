# Synthetic Customer Panel

A Codex skill for interviewing simulated customers about websites, physical products, services, and pricing. Give it the material a customer would see, the audience you care about, and the decision you want to make. It collects first-person answers and turns recurring reactions into hypotheses you can test with people.

## Install

Clone the repository into your personal skills directory, then start a new Codex session. For example, on macOS or Linux:

```sh
mkdir -p ~/.agents/skills
git clone https://github.com/elliptic1/synthetic-customer-panel.git ~/.agents/skills/synthetic-customer-panel
```

## Try it

> Use $synthetic-customer-panel to compare two offers for a neighborhood pottery workshop. Each costs $60 for a two-hour class with materials included. Offer A says cancellations are refundable up to 48 hours before class. Offer B says cancellations are refundable up to 24 hours before class. Interview prospective first-time attendees about whether they would book. Tell me what influenced their decision and how I could test it with real visitors.

The qualitative panel uses the agent’s interview tools. Optional numerical scoring uses Python with NumPy and either local BGE embeddings or vectors you supply. The bundled six sets of English reference statements cover purchase intent. For other outcomes, such as requesting a quote, write reference statements for that action. See the [scoring guide](references/scoring.md).

## Interpreting results

The report distinguishes the number of agents, simulated personas, and responses. Semantic Similarity Rating (SSR) maps each answer to a distribution on a five-point intent scale. A variant’s mean summarizes simulated stated intent. Measure actual bookings, purchases, or other outcomes to validate a proposed change. See the [study protocol](references/study-protocol.md) and the [research paper](https://arxiv.org/abs/2510.08338v3).

Released under the [MIT License](LICENSE).
