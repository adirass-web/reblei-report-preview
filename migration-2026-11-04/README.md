# Local migration archive
inventory.json records the final included files, exact-duplicate destinations, verified cache reconstruction paths, SHA256, sizes, and original filesystem timestamps. inventory-initial-observation.json is an earlier metadata observation, superseded by the final inventory.
local-support/ preserves unique historical local work in its original workspace layout. It is an archive, not the active report or executable workflow. Old scripts may contain obsolete absolute paths and branch names; do not run them without reviewing their intended inputs/outputs.
pre-migration-snapshots/ preserves the former README and checksum manifest before migration routing and resealing.
Current research is in the parent directory. Original source bytes were not rewritten. Browser captures and work logs remain diagnostics or leads, not promoted official evidence.
Git does not preserve source file mtimes; use the nanosecond/UTC timestamp metadata in the inventory when needed.
