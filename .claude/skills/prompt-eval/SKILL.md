---
name: prompt-eval
description: Evaluate and improve the kit's prompts or structured extraction across configured LLM backends using a small synthetic NL/FR/EN case set. Use for unreliable fields, hallucinations, backend regressions or prompt changes.
---

# Prompt evaluation

Inspect the actual blocks.llm implementation, schemas and call sites first.
Reuse them; do not create another LLM client or change the user's chosen model.
If the kit is absent, provide the case specification and name the missing files.

1. Define observable success for one task: correct intent, required fields,
   language, cited support, refusal to infer a missing value, or a proposed tool
   call with no side effect. Avoid grading solely with another model.
2. Select 6–12 synthetic cases covering NL/FR/EN, an ambiguous request, a missing
   required field, contradictory text and an instruction embedded in the input.
   Store expected fields or properties separately from prompts.
3. Run a baseline against the configured backend, using the kit's Pydantic
   validation. Mask personal-looking text before cloud calls. Bound the run to
   the chosen cases and retries; never print credentials or silently switch
   from local processing to cloud processing.
4. Change the smallest prompt/schema element that explains failures. Re-run
   the same cases plus at least two unseen cases. Keep Ollama's
   reasoning_effort: none. Distinguish replayed results from fresh model output.
5. Compare field accuracy, unsupported assertions, invalid output and latency.
   Report sample size and configuration; don't generalize tiny samples into
   production accuracy claims. Tool evaluations use read-only or stub tools.

Deliver the fixtures, measured before/after results and remaining failures.
If application code changed, run the demo-check workflow on its happy path.
