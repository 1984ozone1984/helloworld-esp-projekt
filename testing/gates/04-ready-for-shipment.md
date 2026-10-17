# Gate — Ready for shipment (closes Phase 3, Build)

**Standing exclusion.** Evidence is committed artefacts in this repository, CI results, and live testbench answers only — never memory, transcripts, `~/.claude`, or the author's account of what was done. Something not found in the repository is not there; that is a finding.

**Verdict format.** `OPEN`, or `SHUT` followed by one line per finding: the requirement row, the evidence looked for, and what was found instead. Return a verdict, never a fix — do not edit files.

## Requirements

| # | Must be true | Where to look | Evidence |
|---|---|---|---|
| 1 | Every FSD requirement is met | `testing/test-plan.yaml` × `docs/Functionality/FSD.md` | Every Must/Should/CON ID appears in some test's `verifies:`, and every such test is `successful` on the current commit |
| 2 | Prohibited outcomes were checked | test code at each `impl:` | Each test asserts its contract's Must-NOT, not only the success observation |
| 3 | Journey green | JRN-01.1 … 01.5 | `successful`, same commit |
| 4 | Reconcile empty both ways | plan `impl:` vs `tests/` | No entry with empty `impl:`; no test function that no `impl:` points at |
| 5 | Watchdog tests ran on fault images | FR-WDT-01..03 entries | Results tied to fault-heartbeat **and** fault-blink artefacts |
| 6 | User manual current | `docs/UserDocumentation/User-Manual.md` | The status line no longer says "nothing is deployable"; chapters 2 and 4 are filled |

## Mechanical checks

```bash
grep -nE 'impl: ""' testing/test-plan.yaml && exit 1
grep -nE 'status: (not done|failed)' testing/test-plan.yaml && exit 1
ctest --test-dir build-host --output-on-failure
```

## Judgement checks

- For NFR-WDT-04/05 and FR-WDT-03, quote the assertion in the test code that would fail if the device had silently rebooted.
- Are any results older than the last firmware change? Compare each result's commit with `git log -1 -- main components`.

## Traps

- A test marked successful against an earlier commit than the shipped one.
- FR-LED-03 is a May with human acceptance: check that its acceptance is recorded with a date and the commit it saw, not inferred from the LED log lines.
