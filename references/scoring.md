# Scoring intent

Save a CSV with one row per draw and a column named `intent_excerpt`. Each value is the complete brief answer to the intent question. Include persona, draw, variant, and cohort identifiers when applicable. The scorer copies the input columns into a new CSV and adds five weights and their weighted mean. Its JSON summary goes to standard output.

## Choose anchors and an encoder

The [bundled English anchors](../assets/purchase-anchors.json) are six newly authored sets for a generic purchase decision. Appendix C.1 describes the study’s six sets without listing their 30 statements. The linked public implementation demonstrates the interface with agreement examples. Keep a copy of the exact anchor file for each run. For other actions or languages, prepare parallel sets covering the same action at five increasing levels. Use generic phrasing so mentioning a product feature cannot by itself drive a high rating. [Paper and appendices](https://arxiv.org/abs/2510.08338v3) · [Authors’ code at the reviewed revision](https://github.com/pymc-labs/semantic-similarity-rating/tree/86dcd2597c7824e4fd6546b884c5500c43a4b022)

Use the same model, revision, and encoding settings for every answer and anchor. Record those choices. For the offline English adaptation, install numpy, onnxruntime, and tokenizers in a virtual environment and obtain the matching tokenizer.json and onnx/model.onnx from [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5). From the skill directory, for example:

```sh
python scripts/score_ssr.py responses.csv assets/purchase-anchors.json scored.csv \
    --model /path/to/model.onnx --tokenizer /path/to/tokenizer.json \
    --group-by variant --persona-column persona_id > summary.json
```

The paper used OpenAI’s `text-embedding-3-small`. To use vectors already obtained from this or another suitable encoder, supply a UTF-8 JSON object with a string `model` field and a `vectors` dictionary mapping each exact intent answer and anchor string to its numeric vector. The cached-vector path requires numpy and runs offline.

```sh
python scripts/score_ssr.py responses.csv anchors.json scored.csv \
    --embeddings embeddings.json --group-by variant --persona-column persona_id
```

Both grouping flags are optional. Use a new output path for each run. Retain the per-draw CSV and, for repeated or grouped designs, read the corresponding persona-weighted or variant-level summary in the JSON.

## Read the output

For each response and anchor set, the scorer computes five cosine similarities, subtracts their minimum, then divides by the sum of the shifted similarities. This implements Appendix A.4.3 with ε = 0 and SSR temperature T = 1. Each set contributes equally. Identical similarities make the denominator zero. Inspect the affected input and anchor set if the scorer flags a tie.

In each reported group, `distribution` contains the average weights for ratings 1 through 5. The `mean` is the sum of each rating times its weight. With a persona column, repeated draws receive equal weight within each persona, then personas receive equal weight. Report any further weighting by real audience shares separately. The ordered `anchor_set_means` allow a variant comparison using each prespecified anchor set in turn. If the preferred variant flips, report the sensitivity alongside the pooled difference. Weights in the upper bins describe modeled intent. Measure conversion using the corresponding observed action.
