# 00_CONTEXT_README — 07_Hardware_Health
> 📌 Pinned context file. Read this first when entering this folder.

## Role
Hardware inventory system. Tracks all devices in the YNAI5 ecosystem with standardized machine manifests.

## What Belongs Here
- `generate_manifest.py` — run this on any new machine to auto-detect and log hardware
- `inventory/` subfolder — one JSON file per device, named `<hostname>_<date>.json`

## How to Add a New Device
```bash
# On any machine (Windows/Linux/macOS):
python generate_manifest.py --save --upload
# → Detects hardware, saves to inventory/<hostname>_<date>.json, pushes to Drive
```

## Schema
```json
{
  "device_name": "...",
  "os": "...",
  "cpu": "...",
  "ram_gb": 0,
  "gpu": "...",
  "storage_gb": 0,
  "disk_free_gb": 0,
  "hostname": "...",
  "platform": "...",
  "timestamp": "...",
  "manifest_version": "1.0.0"
}
```

## Current Inventory
| Device | OS | CPU | RAM | GPU | Storage |
|--------|-----|-----|-----|-----|---------|
| SOLOL | Windows 11 | AMD Ryzen 5 5500U | 7.3 GB | AMD Radeon(TM) Graphics | 237.4 GB |

## Agent Notes
- **Claude:** When Shami mentions a new machine, run `generate_manifest.py --save --upload` immediately.
- **Constraint reminder:** SOLOL has 8GB RAM and integrated GPU only — no local AI video generation.
- **GCP VM:** Not listed here (cloud VM, not physical hardware). See `01_Infrastructure_GCP` instead.
