---
name: synthetic-customer-panel
description: Run multi-agent synthetic customer interviews on websites, products, services, or offers. Use free-text reactions to identify friction, compare variants or prices, and score simulated intent with Semantic Similarity Rating (SSR).
---

# Synthetic Customer Panel

Identify the decision the user wants to make, the audience, and the action that would signal interest. Select one action per question, such as booking a service, requesting a quote, or buying a product. Capture the material each persona will evaluate once per variant. This may be a public page, a concept description, packaging artwork, or an offer. Record its source or version, date, terms shown, and the text or visuals respondents received. Base visual observations on material the agents actually saw.

## Run the panel

1. Choose personas before collecting answers. Use known audience traits and shares when available. For an exploratory panel, about 24 personas across three agents is a useful starting point. Include people with different needs and alternatives, leaving each persona’s opinion open. For study-style sampling, repeats, or comparison to human data, use [the study protocol](references/study-protocol.md).
2. Assign independent agents and give each a persona profile, the frozen stimulus, and the same intent question. Use a fresh context per persona and variant when feasible. Keep the owner’s preferred result, other variants, previous interviews, scoring anchors, and prior findings out of the respondent context. If an agent generates several personas in one batch, disclose the batching. Record actual counts of agents, unique personas, and responses.
3. Ask a neutral question about a single action. For example, “Given this offer, how likely would you be to [take the specified action]? Reply briefly in your own words.” Save the complete first answer as `intent_excerpt`, including hesitation, conditions, and negation. Then ask what caught their attention, what they would do next, or what influenced their answer. Keep follow-ups available for qualitative analysis.
4. For an A/B or price comparison, vary only the intended stimulus detail, keep the question and scoring setup fixed, and use balanced arms or the same profiles in fresh contexts. Retain the assigned variant and persona ID with each response. Report any deliberate oversampling and any weighting by known audience shares.

## Score and report

Use [the scoring guide](references/scoring.md) when numerical intent is part of the request. The scorer accepts the local BGE encoder or vectors prepared with another embedding model, and can aggregate repeat answers by persona within each variant. Use the [starter purchase anchors](assets/purchase-anchors.json) for an exploratory English purchase question. Define action- and language-appropriate anchors before scoring other outcomes and reuse them across the comparison. If embeddings are unavailable, report qualitative findings and identify any manual coding.

Lead with the decision the panel informs. Tie each proposed change to a stimulus detail, a recurring reaction, and a measurable test. Quote simulated respondents verbatim. Count recurring themes directly from the texts and give the persona denominator. For scored work, report the five **average SSR weights** and the **expected 1–5 intent score** for each variant. A single answer can contribute weight to all five bins. When a small difference drives a decision, check whether its direction holds across anchor sets and reasonable generation repeats.

Preserve the stimulus, profiles and assignment, verbatim answers, anchors, model identifiers and available generation settings with scored outputs so the result can be audited. Label invented audience composition and model-based estimates. Use matched human ratings to assess agreement, or observed events such as completed purchases or bookings to test a conversion hypothesis.
