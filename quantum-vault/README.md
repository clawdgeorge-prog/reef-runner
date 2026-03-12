# Quantum Vault

Quantum Vault is a mobile-first neon maze arcade game built around one clean objective loop.

## Core loop
- Collect every shard in the maze
- The portal opens when the maze is clear
- Escape to move to the next district
- Use Pulse Burst as your one simple panic button

## This polish pass
- Simplified the run even further:
  - removed mixed enemy roles in favor of one easier-to-read sentry threat
  - kept the focus on **collect everything, then escape**
  - trimmed UI wording and reduced mobile clutter
- Made the game more phone-friendly:
  - denser, clearer mobile HUD cards
  - hidden nonessential instruction panel on small screens
  - forgiving lane-follow turning remains in place
- Improved the arcade score feel:
  - shards are a flat **100 points** each
  - level clears cash out as a clean bonus from speed + level + remaining lives
  - refreshed local leaderboard storage for the simpler arcade format
- Upgraded presentation and smoothness:
  - richer animated light sweeps and scan-grid motion
  - cleaner sentry silhouettes with softer movement
  - stronger portal and background glow for a prettier read at a glance

## Controls
- **Desktop:** WASD / Arrow keys to move, Space for Pulse Burst
- **Mobile:** swipe / drag or use the D-pad, tap Burst to stun nearby sentries when charged

## Notes
- Fully self-contained; no external assets required
- Scores and leaderboard are stored in local browser storage
- Best runs come from efficient shard collection, avoiding hits, and banking the clear bonus quickly
