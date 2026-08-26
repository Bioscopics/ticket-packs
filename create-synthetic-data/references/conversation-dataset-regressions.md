# Conversation Dataset Regressions

Use this reference only for datasets that contain multi-turn chats, semantic language labels, or controlled temporal expressions. Keep the checks proportional: run them on every affected unit in a corpus; a small one-off conversation needs only the relevant checks.

## Label-First Planning

For conversation/eval datasets with a desired system output or held-out labels:

- Work backward from the required output, label, and adjudication rule before selecting topics or drafting text. Keep the generation brief separate from model-visible conversation content.
- Track topic, subject, persona, evidence explicitness, linguistic messiness, and inference difficulty as hidden generation and QA metadata when they help coverage or review. Do not narrate those axes, label names, or evaluation intent in the conversation.
- Assign harder evidence deliberately. Preserve a natural minority of direct statements; use paraphrase, practical consequences, or distributed cues for harder items only when the full visible conversation still uniquely determines the target label.

## Natural-Evidence Gate

- Require users to pursue an ordinary task, question, update, blocker, or result. Reject turns that exhaustively restate old value, new value, state, and outcome only to make extraction easy.
- Make later-session openers self-contained enough to identify the task or result without absent turns. Do not turn fresh-session intelligibility into a mandatory full recap.
- Vary fragments, typos, repairs, punctuation, and other mannerisms by persona and use them sparsely. Many conversations may need none; never apply one corpus-wide noise quota or signature error.
- Keep assistant replies ordinary, locally responsive, and compatible with the next turn. Do not have the assistant solicit a state recap, explain hidden labels, or add evidence the user did not provide.

## Blind Adjudication

- Blind-review every pilot item using only the visible conversation and evaluation question. Withhold labels, hidden metadata, rationales, and target difficulty until the reviewer records the adjudication and decisive cues.
- For a full corpus, blind-review every high-inference-difficulty item and a proportionate stratified sample of the remaining items. Scale sampling and second review to corpus size, stakes, and ambiguity risk.
- Repair and re-review any disagreement, unclear evidence, or evaluator-cooperative narration. Correct labels and naturalness are separate acceptance checks.

## Fresh-Session Openers

When a conversation has separately dated or session-grouped segments, treat each segment as a fresh conversation unless the delivered artifact includes the preceding assistant turns.

- For every later-session opener, make a fresh-start projection: remove all prior-session turns and any absent assistant prompt.
- The opener must establish its topic plus current intent, plan, status, or outcome on its own. It may mention a prior plan, but it must supply the referent rather than merely acknowledge or answer an unseen turn.
- Check every affected opener, not only a sample. Preserve natural brevity after the topic is re-established.

## Semantic-Label Adjudication

For labels that encode stance, hedge strength, confidence, commitment, intent, sentiment, or a related semantic factor:

- Judge the whole labeled sentence or turn, including negation, qualification, concession, and the closing clause; do not assign from a trigger word alone.
- Reject or repair text whose final cue reverses or materially weakens the stated label. If the label contract permits relabeling, make the label match the full utterance; otherwise rewrite the utterance while preserving the required factor.
- Record the checks performed and inspect every controlled label value after generation or repair. Use an independent reviewer for ambiguous or high-stakes distinctions.

## Temporal Expression Realism

For dates, deadlines, or planned actions expressed in natural language:

- Measure relevant temporal surface forms from real examples when available, such as relative, calendar-date, weekday, and event-anchored expressions. Plan a context-appropriate mix; do not impose fixed ratios without calibration.
- Choose exact calendar dates when a real-world anchor makes them useful, such as an appointment, ticket, filing deadline, coordinated handoff, or quoted record. Otherwise use the natural form for the persona, task, and surrounding timeline.
- Resolve every relative expression against the message timestamp and case timeline. Check that it neither contradicts known outcomes nor creates an impossible ordering.
- After generation, count expression categories and review any mechanically dominant construction against the profile and plan. Variation must come from context, not random substitutions.

## Regression Receipt

In the QA report, state the session-boundary rule, opener count checked, semantic-label values checked, temporal-expression categories observed, timeline check result, and any calibrated exception. For applicable eval data, also record blind pilot results, high-difficulty review coverage, remaining-sample method, and repairs. A structured corpus may record the same fields in JSON. Do not add a universal validator unless the dataset schema is stable enough to make the checks deterministic.
