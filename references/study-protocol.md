# Comparing a run with the paper

Maier et al. used 57 US personal-care concept surveys with 9,300 distinct respondents and 150–400 respondents per concept. Each survey presented one concept. The main stimulus was a concept slide. Text transcriptions were a separate condition. These details matter when comparing the published results with a new experiment. [Paper, Sections 3–4 and Appendices A–B](https://arxiv.org/abs/2510.08338v3)

## Elicitation and sampling

For a benchmark against a human survey, align the stimulus, question, response scale, and available respondent attributes with that survey. Match one synthetic profile per respondent using the available attributes. For a concept without survey data, record how profiles were chosen. A buying constraint or use case can be more relevant than a broad demographic label.

The paper sampled two replies to the same prompt for each persona and concept. It used GPT-4o and Gemini-2.0-flash in separate experiments, with top-p 0.9 and generation temperatures 0.5 and 1.5. Main results use 0.5. When following this design, start each draw from the same clean prompt, retain a draw ID, and average the two distributions within persona before averaging personas. Record available model settings and identify any substitutions. Keep model runs separate when measuring model sensitivity. [Appendix A.4](https://arxiv.org/html/2510.08338v3)

## Interpretation and validation

- **One concept with human ratings.** Compare the five-bin distributions on the same scale. Appendix A.3 uses KS similarity, one minus the largest absolute difference between their cumulative proportions. Report the mean of the per-concept similarities when several concepts are available.
- **Several concepts with human ratings.** The authors computed Pearson correlation across the human and synthetic *concept means*. To estimate correlation attainment, they repeated 2,000 random half-splits of the humans within each concept and drew an equally sized synthetic sample. They divided the average human–synthetic correlation by the average human–human split-half correlation. Report the underlying correlations if computing this ratio. It requires variation across concepts and a meaningful human reference correlation. For a two-variant experiment, show the difference in expected intent and the distribution for each arm.
- **Meaning of the headline.** The roughly 90% figure is the fraction of that estimated split-half correlation benchmark attained in this data set. The study also observed a wider spread in synthetic mean intent scores across concepts. Measure actual uptake with behavioral data for the intended action.
- **Transfer and tuning.** The researchers manually optimized anchors on the study data. Check newly tuned anchors on held-out concepts if assessing generalization. Figure 4 compares distinct concepts across price tiers. For a within-product pricing hypothesis, hold the offer fixed and vary the displayed price. Treat model-dependent differences by demographic group as hypotheses for human research.
