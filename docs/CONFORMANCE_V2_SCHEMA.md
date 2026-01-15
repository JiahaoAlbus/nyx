# Conformance v2 Report Schema

The conformance runner writes a JSON report that is stable for audit use.

## Top-Level Fields
- rules: array of rule metadata
- results: array of runtime or scan outcomes
- attack_cards: array of failure cards with minimal evidence

## Rule Object
- rule_id: string
- adversary_class: string[]
- attack_vector: string
- surface: string
- severity: string
- rationale: string
- detection: string
- repro_command: string

## Result Object
- rule_id: string
- passed: boolean
- evidence: string|null

## Attack Card Object
- rule_id: string
- adversary_class: string[]
- surface: string
- attack_vector: string
- repro_command: string
- evidence: string|null

## Runner Command
```bash
PYTHONPATH="packages/conformance-v1/src" \
  python -m conformance_v1.runner --out /tmp/nyx_conformance_v2_report.json
```
