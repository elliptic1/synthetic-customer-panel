#!/usr/bin/env python3
"""Score intent responses against five-point semantic anchors."""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def bge_vectors(texts, model, tokenizer_path):
    import onnxruntime as ort
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    tokenizer.enable_padding()
    tokenizer.enable_truncation(max_length=512)
    session = ort.InferenceSession(str(model), providers=["CPUExecutionProvider"])
    batches = []
    for start in range(0, len(texts), 32):
        encoded = tokenizer.encode_batch(texts[start:start + 32])
        inputs = {
            name: np.asarray([getattr(item, attribute) for item in encoded], dtype=np.int64)
            for name, attribute in (
                ("input_ids", "ids"),
                ("attention_mask", "attention_mask"),
                ("token_type_ids", "type_ids"),
            )
        }
        result = session.run(None, {item.name: inputs[item.name] for item in session.get_inputs()})[0]
        batches.append(result[:, 0, :])
    return np.concatenate(batches)


def score_distributions(vectors, count, num_sets):
    if vectors.ndim != 2 or vectors.shape[1] == 0 or not np.isfinite(vectors).all():
        raise ValueError("Expected finite embedding vectors of equal nonzero dimension.")
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    if not np.isfinite(norms).all() or (norms == 0).any():
        raise ValueError("Every embedding must have a finite, nonzero norm.")
    unit = vectors / norms
    similarities = (unit[:count] @ unit[count:].T).reshape(count, num_sets, 5)
    weights = similarities - similarities.min(axis=2, keepdims=True)
    totals = weights.sum(axis=2, keepdims=True)
    flat = np.argwhere(totals[:, :, 0] == 0)
    if len(flat):
        response, group = flat[0] + 1
        raise ValueError(f"Response {response}, anchor set {group}: all similarities tie; SSR is undefined.")
    return weights / totals


def summarize(by_set, rows, persona_column):
    by_persona = defaultdict(list)
    for index, (pmfs, row) in enumerate(zip(by_set, rows)):
        persona = row[persona_column] if persona_column else index
        by_persona[persona].append(pmfs)
    panel = np.mean([np.mean(draws, axis=0) for draws in by_persona.values()], axis=0)
    distribution = panel.mean(axis=0)
    ratings = np.arange(1, 6)
    summary = {
        "responses": len(rows), "distribution": distribution.tolist(),
        "mean": float(distribution @ ratings), "anchor_set_means": (panel @ ratings).tolist(),
    }
    if persona_column:
        summary["personas"] = len(by_persona)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path, help="UTF-8 CSV with an intent_excerpt column")
    parser.add_argument("anchors", type=Path, help="JSON list of sets, each with 5 strings ordered low to high")
    parser.add_argument("output", type=Path, help="New per-response CSV output path")
    backend = parser.add_mutually_exclusive_group(required=True)
    backend.add_argument("--model", type=Path, help="BGE Small English ONNX model")
    backend.add_argument("--embeddings", type=Path, help="JSON with model and vectors keyed by verbatim text")
    parser.add_argument("--tokenizer", type=Path, help="BGE tokenizer.json, required with --model")
    parser.add_argument("--group-by", metavar="COLUMN", help="Summarize each variant or concept separately")
    parser.add_argument("--persona-column", metavar="COLUMN", help="Average repeated draws within each persona")
    args = parser.parse_args()
    if bool(args.model) != bool(args.tokenizer):
        parser.error("--tokenizer must be supplied with --model only.")

    with args.responses.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        columns = reader.fieldnames or []
        rows = list(reader)
    if not rows:
        parser.error("Provide at least one response.")
    for column in filter(None, ["intent_excerpt", args.group_by, args.persona_column]):
        if column not in columns or any(not (row.get(column) or "").strip() for row in rows):
            parser.error(f"Each row needs a nonempty value in {column}.")

    anchors = json.loads(args.anchors.read_text(encoding="utf-8"))
    if not isinstance(anchors, list) or not anchors or any(
        not isinstance(group, list) or len(group) != 5
        or any(not isinstance(item, str) or not item.strip() for item in group) or len(set(group)) != 5
        for group in anchors
    ):
        parser.error("Each anchor set needs five distinct, nonempty strings in ascending order.")

    texts = [row["intent_excerpt"] for row in rows] + [item for group in anchors for item in group]
    if args.embeddings:
        cache = json.loads(args.embeddings.read_text(encoding="utf-8"))
        if not isinstance(cache, dict) or not isinstance(cache.get("vectors"), dict):
            parser.error("Expected an embeddings JSON object with model and vectors fields.")
        model = cache.get("model")
        if not isinstance(model, str) or not model.strip():
            parser.error("Identify the embedding model in the model field.")
        try:
            vectors = np.asarray([cache["vectors"][text] for text in texts], dtype=float)
        except (KeyError, TypeError, ValueError) as exc:
            parser.error(f"Incomplete or malformed embeddings cache: {exc}")
    else:
        vectors = bge_vectors(texts, args.model, args.tokenizer)
        model = str(args.model)

    try:
        by_set = score_distributions(vectors, len(rows), len(anchors))
    except ValueError as exc:
        parser.error(str(exc))
    if args.group_by:
        groups = defaultdict(list)
        for index, row in enumerate(rows):
            groups[row[args.group_by]].append(index)
        result = {"group_by": args.group_by, "groups": {
            name: summarize(by_set[indices], [rows[i] for i in indices], args.persona_column)
            for name, indices in groups.items()
        }}
    else:
        result = summarize(by_set, rows, args.persona_column)

    ratings = np.arange(1, 6)
    score_columns = [f"ssr_weight_{rating}" for rating in ratings] + ["ssr_mean"]
    if set(score_columns).intersection(columns):
        parser.error("Input already has SSR score columns.")
    with args.output.open("x", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(columns + score_columns)
        for row, distribution in zip(rows, by_set.mean(axis=1)):
            writer.writerow([*(row.get(col) for col in columns), *distribution, distribution @ ratings])
    result["embedding_model"] = model
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
