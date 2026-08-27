# On-Prem and Security Contract

The integration must work without hosted vendor runtime services. The
`distylai-mrkr` package is required; any particular application, agent, or
storage framework and public search are optional.

## Package delivery

- Mirror the approved `distylai-mrkr` wheel and transitive dependencies into
  the customer's private package registry, or provide an integrity-checked
  offline wheel bundle through the approved software-delivery process.
- Pin and lock according to the customer's dependency policy.
- Verify distribution name, imported public API, wheel hash/signature, Python
  compatibility, and license/security approval during deployment.
- Run `scripts/check_compatibility.py` against the installed environment and
  approved wheel; treat `assets/compatibility.json` as the tested packet receipt.
- Never download code or models dynamically from the application process.

## Egress modes

Define one deployment mode explicitly:

| Mode | Documents | Web/internal retrieval | Vision/OCR |
| --- | --- | --- | --- |
| Air-gapped | local/customer stores only | internal provider only | local/disabled |
| Restricted | customer stores | allowlisted proxy/provider | approved endpoint |
| Connected | customer stores | approved public + internal | approved provider |

`vision="auto"` may select a provider when credentials exist. Do not rely on
implicit environment behavior for on-prem deployments; configure or disable
external vision extraction explicitly.

## Secrets and data handling

- Keep search, object-store, model, and vision credentials in the host's
  existing secret manager/config system.
- Do not place secrets, signed URLs, private storage paths, or ACL metadata in
  model-visible context or client citation bundles.
- Apply existing classification, residency, encryption, retention, deletion,
  DLP, and audit policies to source text, extracted text, match hints, model
  output, and citation metadata.
- Record whether model and retrieval providers receive customer source text.
- Use customer-controlled resolver routes for protected evidence.

## Tenant and request isolation

- Scope provider packets and citation bundles to one authorized invocation or
  durable result record.
- Recheck authorization when a citation is opened; do not rely only on the ACL
  at generation time.
- Use bounded extraction/search concurrency, file counts, file sizes, timeouts,
  and cancellation inherited from the host application.
- Sanitize filenames and reject symlinks/path traversal when local staging is
  required.

## Deployment proof

Before calling the packet on-prem ready, prove:

- install from the private/offline source on a clean environment;
- startup with public network access disabled;
- deterministic document citation flow without external credentials;
- the configured behavior when OCR/vision or public web search is unavailable;
- no telemetry or external calls beyond the approved allowlist;
- citation source access under allowed, denied, revoked, and cross-tenant users;
- backup/restore or record migration preserves citation bundles and source
  version identifiers.
