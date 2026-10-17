# Gate — Shipped

**Standing exclusion.** Evidence is committed artefacts in this repository, CI results, and live testbench answers only — never memory, transcripts, `~/.claude`, or the author's account of what was done. Something not found in the repository is not there; that is a finding.

**Verdict format.** `OPEN`, or `SHUT` followed by one line per finding: the requirement row, the evidence looked for, and what was found instead. Return a verdict, never a fix — do not edit files.

## Requirements

| # | Must be true | Where to look | Evidence |
|---|---|---|---|
| 1 | Release published from a tagged commit | GitHub Releases | A release `vX.Y.Z` whose assets came from the `build.yml` run for that tag |
| 2 | Rebuilt in the pinned container | that run's log | `espressif/idf:v6.0.2`; `idf.py --version` shows v6.0.2 |
| 3 | Journey green on the released bytes | the `verify` job of the same run | Succeeded; `release` ran after it |
| 4 | The image says what it is | release asset | Banner `version=vX.Y.Z` with no `-dirty` or `-g` suffix (FR-BOOT-02); `fault: stalling` absent from the .bin (FR-BUILD-01) |

## Mechanical checks

```bash
T=$(git describe --tags --abbrev=0)
gh release view $T
gh run list --workflow build.yml --branch $T --json conclusion,databaseId -L 1
gh release download $T -p 'firmware_*.bin' -D /tmp/rel && ! grep -q 'fault: stalling' /tmp/rel/firmware_*.bin
```

## Traps

- A release created by hand, or by a run whose verify job was skipped.
