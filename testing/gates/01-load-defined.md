# Gate — Load defined (closes Phase 0, Definition)

**Standing exclusion.** Evidence is committed artefacts in this repository, CI results, and live testbench answers only — never memory, transcripts, `~/.claude`, or the author's account of what was done. Something not found in the repository is not there; that is a finding.

**Verdict format.** `OPEN`, or `SHUT` followed by one line per finding: the requirement row, the evidence looked for, and what was found instead. Return a verdict, never a fix — do not edit files.

## Requirements

| # | Must be true | Where to look | Evidence |
|---|---|---|---|
| 1 | Every Must/Should requirement and every CON-xx carries a verification contract with a "Must NOT happen" outcome | `docs/Functionality/FSD.md` | A compact row `\| <ID> \|` with a non-empty Must-NOT column, or an `id: <ID>` YAML block with `prohibited_outcomes` |
| 2 | Every requirement is provenance-tagged | same | `[user]`, `[derived]`, `[pack:esp32]` or `[tooling]` on each FR/NFR/CON line |
| 3 | State model has a complete transition table | FSD §2.3 | LIFE-T1..T9 plus a completeness statement |
| 4 | Security profile precedes the security requirement | FSD §14 | Profile P-BENCH-ISOLATED stated before NFR-SEC-01 |
| 5 | No unresolved proposals or assumptions | FSD | No `(proposed)`, `(assumed)`, `{{`, `TODO`; `open_decisions: []` |
| 6 | Three planes committed | `docs/00-Overview.md`, `docs/Method/`, `docs/UserDocumentation/User-Manual.md` | Tracked by git |
| 7 | Phases sequence correctly | FSD §3 | Every Phase-2 exit criterion is observable through what Phase 1 delivers |

## Mechanical checks

```bash
F=docs/Functionality/FSD.md
git ls-files --error-unmatch docs/00-Overview.md docs/Method/AI-Workflow.md docs/UserDocumentation/User-Manual.md $F
grep -nE '\(proposed\)|\(assumed\)|\{\{|TODO|TBD' $F && exit 1
grep -q '^open_decisions: \[\]' $F
for id in $(grep -oE '\*\*(FR|NFR)-[A-Z]+-[0-9]+\*\* \[(Must|Should)\]' $F | grep -oE '(FR|NFR)-[A-Z]+-[0-9]+') CON-01 CON-02 CON-03 CON-04 CON-05; do
  grep -qE "^\| $id[ (]|^id: $id\$" $F || echo "NO CONTRACT: $id"; done
```

## Judgement checks

- Pick five contracts at random. Could a competent stranger build a rig from each one without reading any code? Quote the stimulus and the observation.
- For FR-WDT-01 and NFR-WDT-05, would a device that silently reboots pass? Quote the prohibited outcome that stops it.
- Does every number the build reads (flash size, partitions, console, LED pin, IDF version) appear in FSD §2.2? Quote each one.

## Traps

- The LED pin and polarity changed from a DevKitC-1 draft to the XIAO (GPIO21, active-low). Check that no GPIO48, WS2812 or led_strip text remains in any plane.
- A requirement that has a contract only in prose ("verified transitively") and no Must-NOT column.
