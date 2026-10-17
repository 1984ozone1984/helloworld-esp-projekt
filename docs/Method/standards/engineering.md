# Standard — Engineering conventions (portable)

Project-agnostic build rules. Each is a single present-state rule.

- **Reuse before adding** — search for an existing helper, module, or skill before
  writing new code.
- **Smallest change that satisfies the rule** — no speculative scope, no drive-by
  refactors bundled with a fix.
- **One module per component** — never fold an interface into its only consumer.
  A component that cannot be named cannot be tested.
- **Dependencies point one way** — lower layers never import higher ones. Where
  the need seems to invert, invert it properly at the composition root rather than
  reaching upward.
- **Extract pure cores** — separate the decision from the I/O. A size check, a
  parser, a state transition, or a unit conversion should be a free function with
  no hardware, network, or filesystem dependency, so the cheapest test tier can
  reach it.
- **Verification before commit** — the firmware builds (`idf.py build` in the
  pinned container, see [`../project/build.md`](../project/build.md)) and the
  host-tier tests pass.
- **Errors fail loudly** — actionable messages, no silent catches, no swallowed
  return codes. Every `esp_err_t` is checked; an ignored error is a defect even
  when nothing breaks yet.
- **Secrets are never in code or documentation** — only their *location* is
  documented. Validate all external input. Least privilege by default.
- **Commits** — imperative subject line of at most 72 characters; the body says
  why. Never commit generated output (`build/`, `managed_components/`,
  `sdkconfig`), temporary directories, or secrets.
