# License Decision

Status: accepted
Date: 2026-07-06
Decision ID: REL-ADR-01

## Decision

Use the MIT License for Migration Feature Factory V0.

## Rationale

- The repository is a public, Markdown-first factory scaffold.
- The intended use is broad reuse, copying, adaptation and contribution.
- A permissive license is sufficient for this V0 because the repo does not
  contain product code, client code or proprietary migration material.
- The MIT License keeps contribution and reuse expectations simple.

## Source

The license text follows the SPDX MIT License entry:

- https://spdx.org/licenses/MIT

## Consequences

- `LICENSE` is present at the repository root.
- README points users to the license.
- Public examples remain fake and generic.
- This is not legal advice; future maintainers can revisit the license if the
  repository gains different distribution or governance needs.

## Alternatives Considered

| Option | Reason Not Chosen |
| --- | --- |
| No license yet | Ambiguous reuse expectations for a public repository. |
| Apache-2.0 | More terms than needed for this documentation-first V0. |
| GPL family | Copyleft is not needed for this factory scaffold. |
