# Information Diffusion Model

AI-assisted event-study scaffold for measuring how information propagates into prices.

## Idea

1. Use an AI parser to turn headlines / transcripts / releases into **timestamped structured events**.
2. Align those events with market microstructure or price-event timestamps.
3. Fit a mutually exciting process: `news → price`, `price → price`, and optionally `news → news`.
4. Compare kernel strengths and half-lives across event types, assets and regimes.

The included script implements the event schema, exponential excitation kernel and a simple intensity calculator. For real estimation, use a tested point-process package such as `tick` or implement a proper likelihood optimizer with validation.

## What AI actually does here

AI is useful for event extraction and categorization, not for magically creating causality. It can classify a release into fields such as:

```json
{"timestamp":"...","entity":"...","event_type":"earnings","direction":"positive","surprise":0.7}
```

The statistical layer still needs explicit timestamps, estimators and out-of-sample checks.

## Suggested upstream reference

- `X-DataInitiative/tick` — BSD-3-Clause — Hawkes / point-process tooling.

Preserve upstream attribution if code is copied or adapted.
