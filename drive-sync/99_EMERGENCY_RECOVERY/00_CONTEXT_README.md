# 00_CONTEXT_README — 99_EMERGENCY_RECOVERY
> 📌 Pinned context file. Read this first when entering this folder.
> ⚠️ COLD STORAGE — Only write here for critical, recovery-essential data.

## Role
Emergency cold storage for critical system backups, recovery keys, and snapshots needed to rebuild the YNAI5 ecosystem from scratch.

## What Belongs Here
- API key backups (encrypted — never store plaintext keys)
- System state snapshots before major changes
- rclone config backup
- SSH key fingerprints (public keys only — never private keys)
- Critical environment variable templates (.env.example files)
- VM reconstruction notes (what to run if the VM needs to be rebuilt from zero)

## What Does NOT Belong Here
- Regular backups → use the SYNC folder for those
- Active files → they belong in their taxonomy folders
- Personal documents → `04_Personal_Archive`

## Write Rules
- ⚠️ **Only Claude or Shami** may write to this folder
- ⚠️ **No agent autonomously writes here** — always requires explicit instruction
- ⚠️ **Never store plaintext API keys or private SSH keys**
- ⚠️ **Label everything with date:** `YYYY-MM-DD-description.md`

## Current Contents
*Empty — ready for critical backups.*

## Recovery Sequence (if rebuilding from zero)
1. SSH to new GCP VM
2. Run `vm-bootstrap.sh` from `01_Infrastructure_GCP`
3. Configure rclone with `gdrive:` remote
4. Mount Drive: `rclone mount gdrive:/YNAI5_AI_CORE /mnt/gdrive`
5. Restore `.env` from this folder
6. Restart all services: `systemctl start ynai5-dashboard ynai5-chat ynai5-drive`
