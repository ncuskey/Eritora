---
phase: 5
plan: 1
wave: 1
---

# Plan 5.1: Final End-to-End Verification

## Objective
Execute a comprehensive "Green Light" smoke test that aggregates all verification checks from previous phases to certify the Milestone v1.3 "Functional Parity" release.

## Context
- We have individual scripts: `reconcile_content`, `validate_source`, `verify_redirects`, `verify_search`, `audit_assets`.
- We need a single command to confirm they all pass.

## Tasks

<task type="auto">
  <name>Create Master Smoke Test</name>
  <files>scripts/final_smoke_test.py</files>
  <action>
    Create a wrapper script that runs:
    1. Content Reconciliation (Expect clean/known state)
    2. Source Validation (Expect clean/known state)
    3. Redirect Verification (Run sample)
    4. Search Verification (Run index check)
    5. Asset Audit (Run integrity check)
    
    It should output a consolidated "GO/NO-GO" report.
  </action>
  <verify>python scripts/final_smoke_test.py</verify>
  <done>Master script validates entire system state.</done>
</task>

<task type="auto">
  <name>Compile Milestone Report</name>
  <files>docs/milestone_v1.3_report.md</files>
  <action>
    Generate the final report summarizing:
    - Objectives met
    - Tests executed
    - Known issues (e.g. the 1 missing image)
    - Ready for Release verdict.
  </action>
  <verify>test -f docs/milestone_v1.3_report.md</verify>
  <done>Final report created.</done>
</task>

## Success Criteria
- [ ] `final_smoke_test.py` returns exit code 0 (PASS).
- [ ] Final Report confirms all "Must-Haves" from the Roadmap are checked off.
