# Synthetic Customer Panel

Interview simulated customers about websites, physical products, services, and pricing with Claude, Codex, or another agent. Give it the material a customer would see, the audience you care about, and the decision you want to make. It collects first-person answers and turns recurring reactions into hypotheses you can test with people.

The skill adapts the Semantic Similarity Rating (SSR) method from Maier et al. at PyMC Labs and Colgate-Palmolive. Simulated customers describe their purchase intent in their own words. The scorer compares each answer with reference statements representing five levels of intent. [Read the paper, *LLMs Reproduce Human Purchase Intent via Semantic Similarity Elicitation of Likert Ratings*](https://arxiv.org/abs/2510.08338v3).

The interview protocol follows the open Agent Skills format. Use the model available in your agent. We used **Astra 6.2 Extra High** (`gpt-6.2-astra` with `xhigh` reasoning effort) to review and refine the workflow against the paper. [Agent Skills specification](https://agentskills.io/specification)

## Install

**Claude chat.** Download [synthetic-customer-panel.zip](https://github.com/elliptic1/synthetic-customer-panel/releases/latest/download/synthetic-customer-panel.zip), upload it under **Customize → Skills**, and enable it. [Claude’s upload guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

**Claude Code.** Clone into your personal skills directory and invoke `/synthetic-customer-panel` with your research question. [Claude Code skills guide](https://code.claude.com/docs/en/skills)

```sh
git clone https://github.com/elliptic1/synthetic-customer-panel.git ~/.claude/skills/synthetic-customer-panel
```

**Codex.** Clone into your personal skills directory and invoke `$synthetic-customer-panel` with the same question. [Codex skills guide](https://developers.openai.com/codex/skills/)

```sh
git clone https://github.com/elliptic1/synthetic-customer-panel.git ~/.agents/skills/synthetic-customer-panel
```

**Other agents.** For an Agent Skills client, place the extracted `synthetic-customer-panel/` folder in its skills directory. For a file-reading agent, point it at `synthetic-customer-panel/SKILL.md`. In a text-only chat, paste [the instructions](SKILL.md) and the material to evaluate, then ask for a qualitative panel. A single agent can interview the personas in sequence.

## Try it

> Use the Synthetic Customer Panel skill to compare two offers for a neighborhood pottery workshop. Each costs $60 for a two-hour class with materials included. Offer A says cancellations are refundable up to 48 hours before class. Offer B says cancellations are refundable up to 24 hours before class. Interview prospective first-time attendees about whether they would book. Tell me what influenced their decision and how I could test it with real visitors.

Qualitative interviews require only text generation. Optional numerical scoring uses Python with NumPy and either local BGE embeddings or vectors you supply. The bundled six sets of English reference statements cover purchase intent. For other outcomes, such as requesting a quote, write reference statements for that action. See the [scoring guide](references/scoring.md).

## Interpreting results

The report distinguishes the number of agents, simulated personas, and responses. SSR maps each answer to a distribution on a five-point intent scale. A variant’s mean summarizes simulated stated intent. Measure actual bookings, purchases, or other outcomes to validate a proposed change. See the [study protocol](references/study-protocol.md).

Released under the [MIT License](LICENSE).
