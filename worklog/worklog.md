# Work Log

## Data access and audit
Dataset A was consolidated and verified at 63 sessions. Dataset B was verified at 15 sessions. Raw event streams were inspected without assuming that archive chunks correspond to business processes.

## Telemetry investigation
Compared event types, application context, browser routes, extracted text and recurring identifiers. A simple inactivity-gap boundary baseline was rejected because office telemetry contains pauses, application switching and interleaving.

## Segmentation
Selected observable workflow anchors plus temporal continuity. Dataset A ground truth was used only to measure anchor timing. Dataset B inference does not consume ground truth.

## Dataset B discovery
Extracted recurring workflow completion/status evidence and ranked workflow families by observed repetition, session reach, standardization and explicit feasibility/risk assumptions.

## Prototype
Built a deterministic expense compliance pre-check with human escalation for missing, unknown or over-threshold cases.

## Validation
Added output validation and unit tests. Local validation: 3 tests passed; B output snapshot validates 120 candidate segments across 15 sessions.

## Repository
Raw operational logs are excluded from the public repository because of size/privacy considerations. Reproducible code, derived outputs and documentation are included.

## AI assistance
Generative AI was used for code generation, debugging, analysis design and documentation drafting; data-derived claims are kept reproducible in scripts/outputs.
