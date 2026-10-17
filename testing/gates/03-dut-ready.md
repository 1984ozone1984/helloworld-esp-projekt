# Gate — DUT ready (closes Phase 2, Commissioning)

**Standing exclusion.** Evidence is committed artefacts in this repository, CI results, and live testbench answers only — never memory, transcripts, `~/.claude`, or the author's account of what was done. Something not found in the repository is not there; that is a finding.

**Verdict format.** `OPEN`, or `SHUT` followed by one line per finding: the requirement row, the evidence looked for, and what was found instead. Return a verdict, never a fix — do not edit files.

## Requirements

| # | Must be true | Where to look | Evidence |
|---|---|---|---|
| 1 | Testbench record | `testing/test-plan.yaml` → `testbench` | URL answers `GET /api/info` now |
| 2 | DUT record matches the FSD's unit | `dut` block | Board XIAO ESP32S3 Sense, chip esp32s3, flash 8MB (CON-02), `slot` set |
| 3 | Forward path proven | capability `dut-on-slot` | A CI run id → flash offsets taken from that artefact's `flash_args` → `Init complete` observed, all recorded on the capability |
| 4 | Project-side capabilities resolved | test plan | None of `dut-on-slot`, `dut-console-after-reset`, `dut-user-led`, `operator` still `unproven` |
| 5 | Agenda empty of project-side items | `testing/debugging-agenda.md` | Every row closed with its measurement |

## Mechanical checks

```bash
URL=$(grep -m1 'url:' testing/test-plan.yaml | awk '{print $2}'); curl -sf -m 10 $URL/api/info
grep -n 'available: unproven' testing/test-plan.yaml && exit 1
grep -qE '^  slot: SLOT[0-9]+' testing/test-plan.yaml
```

## Judgement checks

- Is the forward-path evidence tied to a specific CI run and commit, or to a local build? Quote the run id.
- Was `dut-console-after-reset` proven over several resets, not just one? Quote the count.

## Traps

- A local build flashed by hand proves the developer's toolchain, not the CI artefact path the verify job uses.
- Console silence after a reset is a broken observer until a positive control says otherwise (P-SERIAL).
