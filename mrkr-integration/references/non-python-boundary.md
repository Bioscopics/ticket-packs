# Non-Python Host Boundary

`distylai-mrkr` 0.1.7 is a Python package requiring Python 3.12 or newer. Do not
port its markerization or extraction logic into TypeScript, Java, Go, or another
language merely to avoid a Python boundary.

Use this decision order:

1. **Existing Python backend or worker:** integrate the package there and keep
   the current API/UI workflow unchanged.
2. **Existing approved Python extension/process boundary:** expose a narrow
   host-owned packet/finalize contract through that boundary. Preserve request
   identity, timeouts, cancellation, auth context, and deployment ownership.
3. **No approved Python runtime:** stop and report the compatibility gap. A new
   sidecar/service is an architectural and operational change requiring explicit
   approval, security review, deployment ownership, and latency/reliability
   evaluation.

Do not silently add a subprocess, sidecar, remote DistylAI service, or public
network dependency. The reference Python module is library code, not a service
contract. If a separately approved service is created, keep its API minimal:

- packetize authorized source bytes/text;
- return model-visible citable text and an opaque packet handle;
- finalize designated output against the same tenant-scoped packet;
- return sanitized text and verified bundle;
- never expose resolver secrets or permit caller-supplied marker IDs.

The service must be deployable inside the customer's trust boundary and must
not change the product's agent/workflow semantics.
