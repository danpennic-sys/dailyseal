# DailySeal

**Local-first daily field progress report and QuantumGuard evidence sealer for field operators.**

Offline. Deterministic. Pay once. Compatible with QuantumGuard CONTRACT-v1, FieldSeal, JobSeal, MediaSeal, VeriQuote, and the Operator Pages suite.

## Why DailySeal?

Field operators lose money and time when clients dispute daily progress, crew hours, or "what was done on that day."  
DailySeal captures a structured daily report (crew, hours, work completed, issues, notes, optional media hashes) and seals it into a client-verifiable QuantumGuard evidence bundle.

- No SaaS. No subscription. Runs completely offline after key setup.
- Clients (or their auditors) verify the pack with the free QuantumGuard verifier (`qg verify`).
- Pairs with FieldSeal / JobSeal for deeper job context, MediaSeal for photo evidence, and Chaser for invoicing.
- Deterministic: same inputs → same sealed pack.

## Quick Start

```bash
# Recommended for real Ed25519 signatures
pip install cryptography

python3 src/dailyseal.py --demo
python3 src/dailyseal.py --json samples/daily-001.json --out sealed-daily.json
```

Verify the output with the QuantumGuard CLI (from the quantumguard repo):

```bash
qg verify sealed-daily.json
```

Expected verdict: **PASS**.

## What you can sell

| SKU       | Price | Includes                                      |
|-----------|-------|-----------------------------------------------|
| Operator  | $49   | CLI + sample templates + key setup guide + 1-year email support |
| Command   | $149  | + batch mode + HTML logger + reseller rights for client packs |
| Agency    | $399  | + white-label + multi-site key management + design partner onboarding |

Purchase / access: danpennic@gmail.com  
Or use the Operator Pages Stripe checkout flow.

Source remains free under Apache-2.0 OR MIT. Commercial Operator Pack sold separately.

## Stack Fit

- Python CLI (same family as FieldSeal, VeriQuote, JobSeal, MediaSeal)
- Emits QuantumGuard CONTRACT-v1 bundles (Ed25519, deterministic canonical JSON)
- Local key storage (PEM)
- Designed to drop into the Operator Pages field stack
- Ready for future HTML/JS logger and Chaser CSV export

## License

Apache-2.0 OR MIT
