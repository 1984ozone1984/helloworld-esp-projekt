# Gate — AI harnessed (closes Phase 1, Harness)

**Standing exclusion.** Evidence is committed artefacts in this repository, CI results, and live testbench answers only — never memory, transcripts, `~/.claude`, or the author's account of what was done. Something not found in the repository is not there; that is a finding.

**Verdict format.** `OPEN`, or `SHUT` followed by one line per finding: the requirement row, the evidence looked for, and what was found instead. Return a verdict, never a fix — do not edit files.

## Requirements

| # | Must be true | Where to look | Evidence |
|---|---|---|---|
| 1 | Test plan exists with bench capabilities `available: yes` and project-side ones `unproven` | `testing/test-plan.yaml` | `bench-*` = yes; `dut-on-slot`, `dut-console-after-reset`, `dut-user-led`, `operator` = unproven |
| 2 | Journey seeded, one test per step | same | JRN-01.1 … JRN-01.5, `shape: workflow`, `kind: standard`, `wave: 1`, each with `verifies:` naming FSD IDs that exist |
| 3 | Debugging agenda matches the unproven capabilities one to one | `testing/debugging-agenda.md` | Four rows, each naming its capability |
| 4 | Testing standard is one file with rules + shared procedures | `docs/Method/standards/testing.md` | Contains "Rules that hold for every run" and P-SERIAL |
| 5 | Firmware contains only what the FSD asks for | `main/`, `components/` (absent is fine), `CMakeLists.txt` | No WiFi, BLE, UDP-log, OTA, NVS, HTTP or MQTT code or REQUIRES (the FSD forbids radios: NFR-SEC-01, non-goals) |
| 6 | Skeleton builds and emits one marker | `main/app_main.c` | Logs `Init complete`; implements no FSD requirement |
| 7 | CI: build on push, release on tag, verify job gating release | `.github/workflows/build.yml` | `verify` job on `[self-hosted, testbench]`; `release` needs `verify` |
| 8 | CI has run green once on main | GitHub | Command below |
| 9 | Devcontainer with toolchain and runner installed, registration awaiting the owner | `.devcontainer/` | Dockerfile FROM `espressif/idf:v6.0.2`; `runner/register.sh` present; runner not auto-registered |
| 10 | DUT untouched in Phase 1 | test plan | `dut.slot: null`; no capability carrying evidence that could only come from the board |

## Mechanical checks

```bash
test -f testing/test-plan.yaml && test -f testing/debugging-agenda.md
ls .github/workflows/build.yml .github/workflows/ci.yml
test -n "$(git ls-files .claude/skills/build/SKILL.md)"
grep -q 'runs-on: \[self-hosted, testbench\]' .github/workflows/build.yml
grep -A2 '^  release:' .github/workflows/build.yml | grep -q verify
gh run list -L 5 --branch main --json name,conclusion   # both workflows success at least once
grep -rnE 'esp_wifi|esp_bt|nimble|udp_log|esp_ota|nvs_flash|esp_http|mqtt' main $(ls -d components 2>/dev/null) && exit 1
grep -q 'Init complete' main/app_main.c
```

## Judgement checks

- Open a fresh `/build` session with only the repo. Can it state the project's position (phase, wave, the next act) without asking anything? Quote what it said.
- Does every `verifies:` ID in the plan exist in the FSD? List any that do not.

## Traps

- Harness's "UDP logging always" conflicts with this FSD's no-radio non-goal. Its absence is correct here; its presence is the finding.
- A `.gitignore` pattern for firmware output (`build/`) that also swallows `.claude/skills/build/`. Check `git ls-files .claude/skills/build` is non-empty.
- `tests/host` holds only a tier-runs smoke test. A host test asserting product behaviour belongs to /build's waves, not Phase 1.
