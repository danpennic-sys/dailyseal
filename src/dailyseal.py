#!/usr/bin/env python3
"""
DailySeal — Local-first daily field progress report and QuantumGuard evidence sealer.
Offline. Deterministic. Pay once.
Compatible with QuantumGuard CONTRACT-v1.
"""

import argparse
import json
import hashlib
import base64
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO = True
except ImportError:
    CRYPTO = False

CONTRACT_VERSION = "1"
ALG = "ed25519"

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_or_generate_key(key_path: str = "dailyseal_key.pem"):
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        return priv
    if not CRYPTO:
        raise SystemExit("cryptography package required for signing. pip install cryptography")
    priv = ed25519.Ed25519PrivateKey.generate()
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(key_path, "wb") as f:
        f.write(pem)
    print(f"Generated new key: {key_path}")
    return priv

def get_public_key_hex(priv):
    pub = priv.public_key()
    raw = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return raw.hex()

def sign_payload(priv, payload_hash: bytes) -> str:
    sig = priv.sign(payload_hash)
    return sig.hex()

def build_payload(report: dict) -> bytes:
    # Canonical JSON for determinism
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return canonical

def seal_report(report: dict, priv, out_path: str):
    payload = build_payload(report)
    payload_hash = hashlib.sha256(payload).digest()
    payload_hash_hex = payload_hash.hex()
    signature = sign_payload(priv, payload_hash)
    public_key = get_public_key_hex(priv)

    bundle = {
        "version": CONTRACT_VERSION,
        "payload": base64.b64encode(payload).decode("ascii"),
        "payload_hash": payload_hash_hex,
        "signature": signature,
        "public_key": public_key,
        "alg": ALG,
    }
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Sealed report written to {out_path}")
    print(f"Verify with: qg verify {out_path}")

def demo_report():
    return {
        "type": "daily_field_report",
        "job_id": "JOB-2026-042",
        "site": "Site Alpha — Springfield, MO",
        "date": "2026-11-03",
        "crew": [
            {"name": "Operator A", "hours": 8.0, "role": "Lead"},
            {"name": "Operator B", "hours": 7.5, "role": "Tech"}
        ],
        "work_completed": "Installed 12 panels. Completed conduit run to panel 3.",
        "issues": "Weather delay 45 min in morning. Resolved.",
        "media_hashes": [],
        "notes": "Client on-site at 14:00. Approved progress.",
        "sealed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": "DailySeal/0.1.0"
    }

def main():
    parser = argparse.ArgumentParser(description="DailySeal — seal daily field reports into QuantumGuard packs.")
    parser.add_argument("--demo", action="store_true", help="Run demo and seal sample report")
    parser.add_argument("--json", help="Path to JSON report file to seal")
    parser.add_argument("--out", default="sealed-daily.json", help="Output sealed bundle path")
    parser.add_argument("--key", default="dailyseal_key.pem", help="Path to Ed25519 private key PEM")
    args = parser.parse_args()

    if args.demo:
        report = demo_report()
        print("Demo report:")
        print(json.dumps(report, indent=2))
    elif args.json:
        with open(args.json) as f:
            report = json.load(f)
    else:
        parser.print_help()
        return

    priv = load_or_generate_key(args.key)
    seal_report(report, priv, args.out)

if __name__ == "__main__":
    main()
